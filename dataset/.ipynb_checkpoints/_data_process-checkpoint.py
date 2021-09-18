import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from logdeep import sliding_window, session_window

# tqdm.pandas()
# pd.options.mode.chained_assignment = None  # default='warn'


# In the first column of the log, "-" indicates non-alert messages while others are alert messages.
def _count_anomaly(log_path):
    total_size = 0
    normal_size = 0
    with open(log_path, errors='ignore') as f:
        for line in f:
            total_size += 1
            if line.split('')[0] == '-':
                normal_size += 1
    print("total size {}, abnormal size {}".format(total_size, total_size - normal_size))



def _file_generator(filename, df, features):
    with open(filename, 'w') as f:
        for _, row in df.iterrows():
            for val in zip(*row[features]):
                f.write(','.join([str(v) for v in val]) + ' ')
            f.write('\n')


def process_dataset(data_dir, output_dir, log_file, dataset_name, window_type, window_size, step_size, train_size):
    """
    creating log sequences by sliding window
    :param data_dir:
    :param output_dir:
    :param log_file:
    :param window_size:
    :param step_size:
    :param train_size:
    :return:
    """
    ########
    # count anomaly
    ########
    # _count_anomaly(data_dir + log_file)

    ##################
    # Transformation #
    ##################
    print("Loading", f'{output_dir}{log_file}_structured.csv')
    df = pd.read_csv(f'{output_dir}{log_file}_structured.csv')

    # build log sequences
    if window_type == "sliding":
        # data preprocess
        if 'bgl' in dataset_name:
            df["datetime"] = pd.to_datetime(df['Time'], format='%Y-%m-%d-%H.%M.%S.%f')
        else:
            df['datetime'] = pd.to_datetime(df["Date"] + " " + df['Time'], format='%Y-%m-%d %H:%M:%S')

        df["Label"] = df["Label"].apply(lambda x: int(x != "-"))
        df['timestamp'] = df["datetime"].values.astype(np.int64) // 10 ** 9
        df['deltaT'] = df['datetime'].diff() / np.timedelta64(1, 's')
        df['deltaT'].fillna(0)
        window_df = sliding_window(df[["timestamp", "Label", "EventId", "deltaT"]],
                                   para={"window_size": float(window_size)*60, "step_size": float(step_size) * 60})

    elif window_type == "session":
        # only for hdfs
        id_regex = r'(blk_-?\d+)'
        label_dict = {}
        blk_label_file = os.path.join(data_dir, "anomaly_label.csv")
        blk_df = pd.read_csv(blk_label_file)
        for _, row in tqdm(blk_df.iterrows()):
            label_dict[row["BlockId"]] = 1 if row["Label"] == "Anomaly" else 0

        window_df = session_window(df, id_regex, label_dict)

    else:
        raise NotImplementedError(f"{window_type} is not implemented")

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
    _file_generator(os.path.join(output_dir,'train'), train, ["EventId"])
    print("training size {}".format(train_len))


    ###############
    # Test Normal #
    ###############
    test_normal = df_normal[train_len:]
    _file_generator(os.path.join(output_dir, 'test_normal'), test_normal, ["EventId"])
    print("test normal size {}".format(normal_len - train_len))

    # del df_normal
    # del train
    # del test_normal
    # gc.collect()

    #################
    # Test Abnormal #
    #################
    df_abnormal = window_df[window_df["Label"] == 1]
    _file_generator(os.path.join(output_dir,'test_abnormal'), df_abnormal, ["EventId"])
    print('test abnormal size {}'.format(len(df_abnormal)))

