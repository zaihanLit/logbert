import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from dataset.window import WindowFactory
from common import Utils


# In the first column of the log, "-" indicates non-alert messages while others are alert messages.
def _count_anomaly(log_path):
    total_size = 0
    normal_size = 0
    with open(log_path, errors='ignore') as f:
        for line in f:
            total_size += 1
            if line.split(' ')[0] == '-':
                normal_size += 1
    print("\ntotal size {}, abnormal size {}".format(total_size, total_size - normal_size))


def split_train_test(data_dir, output_dir, log_file, dataset_name, window_type, window_size, step_size, train_size):


    ##################
    # Transformation #
    ##################
    print("\nLoading", f'{output_dir}{log_file}_structured.csv')
    df = pd.read_csv(f'{output_dir}{log_file}_structured.csv')

    window = WindowFactory().create_window(window_type)

    # data preprocess
    if 'bgl' in dataset_name or 'tbird' in dataset_name:
        _count_anomaly(data_dir + log_file)

        if 'bgl' in dataset_name:
            df["datetime"] = pd.to_datetime(df['Time'], format='%Y-%m-%d-%H.%M.%S.%f')
        else:
            df['datetime'] = pd.to_datetime(df["Date"] + "-" + df["Time"], format='%Y.%m.%d-%H:%M:%S')

        df["Label"] = df["Label"].apply(lambda x: int(x != "-"))
        df['timestamp'] = df["datetime"].values.astype(np.int64) // 10 ** 9
        df['deltaT'] = df['datetime'].diff() / np.timedelta64(1, 's')
        df['deltaT'].fillna(0)

        window_df = window.generate_sequence(df[["timestamp", "Label", "EventId", "deltaT"]],
                                             window_size=float(window_size) * 60,
                                             step_size=float(step_size) * 60
                                             )

    elif 'hdfs' in dataset_name:
        id_regex = r'(blk_-?\d+)'
        label_dict = {}
        blk_label_file = os.path.join(data_dir, "anomaly_label.csv")
        blk_df = pd.read_csv(blk_label_file)
        for _, row in tqdm(blk_df.iterrows()):
            label_dict[row["BlockId"]] = 1 if row["Label"] == "Anomaly" else 0

        window_df = window.generate_sequence(df, id_regex=id_regex, label_dict=label_dict)

    else:
        raise NotImplementedError

    if not os.path.exists(output_dir):
        print(f"creating {output_dir}")
        os.mkdir(output_dir)

    #########
    # Train #
    #########
    df_normal = window_df[window_df["Label"] == 0]
    # shuffle normal data
    df_normal = df_normal.sample(frac=1).reset_index(drop=True)
    normal_len = len(df_normal)
    train_len = int(normal_len * train_size) if isinstance(train_size, float) else train_size

    train = df_normal[:train_len]
    Utils.file_generator(os.path.join(output_dir, 'train'), train, ["EventId"])
    print("training size {}".format(train_len))

    ###############
    # Test Normal #
    ###############
    test_normal = df_normal[train_len:]
    Utils.file_generator(os.path.join(output_dir, 'test_normal'), test_normal, ["EventId"])
    print("test normal size {}".format(normal_len - train_len))

    # del df_normal
    # del train
    # del test_normal
    # gc.collect()

    #################
    # Test Abnormal #
    #################
    df_abnormal = window_df[window_df["Label"] == 1]
    Utils.file_generator(os.path.join(output_dir, 'test_abnormal'), df_abnormal, ["EventId"])
    print('test abnormal size {}'.format(len(df_abnormal)))

def split_train_test_aiia(data_dir, output_dir, log_file, dataset_name, window_type, window_size, step_size, train_size):


    ##################
    # Transformation #
    ##################
    print("\nLoading", f'{output_dir}{log_file}_structured.csv')
    df = pd.read_csv(f'{output_dir}{log_file}_structured.csv')

    window = WindowFactory().create_window(window_type)

    window_df = window.generate_sequence(df[["LineId", "EventId"]], window_size=window_size, step_size=step_size)

    if not os.path.exists(output_dir):
        print(f"creating {output_dir}")
        os.mkdir(output_dir)

    #########
    # Train #
    #########
    df_normal = window_df
    # shuffle normal data
    df_normal = df_normal.sample(frac=1).reset_index(drop=True)
    normal_len = len(df_normal)
    train_len = int(normal_len * train_size) if isinstance(train_size, float) else train_size

    train = df_normal[:train_len]
    Utils.file_generator(os.path.join(output_dir, 'train'), train, ["eventids"])
    print("training size {}".format(train_len))

    ###############
    # Test Normal #
    ###############
    test_normal = df_normal[train_len:]
    Utils.file_generator(os.path.join(output_dir, 'test_normal'), test_normal, ["eventids"])
    print("test normal size {}".format(normal_len - train_len))

def generate_test_set_aiia(output_dir, log_file, window_type, window_size, step_size):


    ##################
    # Transformation #
    ##################
    print("\nLoading", f'{output_dir}{log_file}_structured.csv')
    df = pd.read_csv(f'{output_dir}{log_file}_structured.csv')

    window = WindowFactory().create_window(window_type)

    window_df = window.generate_sequence(df[["LineId", "EventId"]], window_size=window_size, step_size=step_size)

    if not os.path.exists(output_dir):
        print(f"creating {output_dir}")
        os.mkdir(output_dir)

    ############
    # Test Set #
    ############
    test_set = window_df

    Utils.file_generator(os.path.join(output_dir, log_file+'.test'), test_set, ["eventids"])
    print("test set size {}".format(test_set))


