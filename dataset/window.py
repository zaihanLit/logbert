import os
import re
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
from abc import ABCMeta, abstractmethod


class WindowFactory:
    def create_window(self, window_type):
        if window_type == "session":
            return SessionWindow()
        elif window_type == "sliding":
            return SlidingWindow()
        else:
            raise NotImplementedError


class Window(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def generate_sequence(self, df, **param):
        """

        :param df: dataframe
        :param param:
        :return: dataframe
        """
        raise NotImplementedError


class SessionWindow(Window):
    def generate_sequence(self, df, **param):
        return self.session_window(df, **param)

    def session_window(self, df, id_regex, label_dict):
        data_dict = defaultdict(list)
        for idx, row in tqdm(df.iterrows()):
            blkId_list = re.findall(id_regex, row['Content'])
            blkId_set = set(blkId_list)
            for blk_Id in blkId_set:
                data_dict[blk_Id].append([row["EventId"]])

        data_df = pd.DataFrame(list(data_dict.items()), columns=['SessionId', 'EventId'])
        data_df["Label"] = data_df["SessionId"].apply(lambda x: label_dict.get(x, 0))
        return data_df


# see https://pinjiahe.github.io/papers/ISSRE16.pdf
class SlidingWindow(Window):
    def generate_sequence(self, df, **param):
        return self.sliding_window(df, **param)

    def sliding_window(self, df, window_size, step_size):
        """
        :param df: dataframe columns=[timestamp, label, eventid, time duration]
        :param window_size: seconds,
        :param step_size: seconds
        :return: dataframe columns=[eventids, time durations, label]
        """
        log_size = df.shape[0]
        label_data, time_data = df.iloc[:, 1], df.iloc[:, 0]
        logkey_data, deltaT_data = df.iloc[:, 2], df.iloc[:, 3]
        new_data = []
        start_end_index_pair = set()

        start_time = time_data[0]
        end_time = start_time + window_size
        start_index = 0
        end_index = 0

        # get the first start, end index, end time
        for cur_time in time_data:
            if cur_time < end_time:
                end_index += 1
            else:
                break

        start_end_index_pair.add(tuple([start_index, end_index]))

        # move the start and end index until next sliding window
        num_session = 1
        while end_index < log_size:
            start_time = start_time + step_size
            end_time = start_time + window_size
            for i in range(start_index, log_size):
                if time_data[i] < start_time:
                    i += 1
                else:
                    break
            for j in range(end_index, log_size):
                if time_data[j] < end_time:
                    j += 1
                else:
                    break
            start_index = i
            end_index = j

            # when start_index == end_index, there is no value in the window
            if start_index != end_index:
                start_end_index_pair.add(tuple([start_index, end_index]))

            num_session += 1
            if num_session % 1000 == 0:
                print("process {} time window".format(num_session), end='\r')

        for (start_index, end_index) in start_end_index_pair:
            dt = deltaT_data[start_index: end_index].values
            dt[0] = 0
            new_data.append([
                time_data[start_index: end_index].values,
                max(label_data[start_index:end_index]),
                logkey_data[start_index: end_index].values,
                dt
            ])

        assert len(start_end_index_pair) == len(new_data)
        print('\nThere are %d instances (sliding windows) in this dataset' % len(start_end_index_pair))

        return pd.DataFrame(new_data, columns=df.columns)


class FixedWindow(Window):
    def generate_sequence(self, df, **param):
        return self.fix_window(df, **param)

    def fix_window(self, df, features, index, label, window_size="T"):
        """
        :param df: structured data after parsing
        features: datetime, eventid
        label: 1 anomaly/alert, 0 not anomaly
        :param window_size: offset datetime https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
        :return:
        """
        df = df[features + [label]]
        agg_dict = {label: 'max'}
        for f in features:
            agg_dict[f] = FixedWindow._custom_resampler

        seq_df = df.set_index(index).resample(window_size).agg(agg_dict).reset_index()
        return seq_df

    @staticmethod
    def _custom_resampler(array_like):
        return list(array_like)



