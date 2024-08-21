import pandas as pd
import numpy as np
from datetime import timedelta
import os
from datetime import datetime

class DataReader(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.data = None

    def data_reader_from_file(self, path):
        df = pd.read_csv(path, compression="gzip")
        if self.data is None:
            print("data is not here")
            self.data = df
        else:
            pass
        return df

    def daterange(self, start_date, end_date):
        days = int((end_date - start_date).days)
        for n in range(days):
            date = start_date + timedelta(n)
            file_path = self.dir_path + str(date.date()) + ".csv.gz"
            print(file_path)
            df = self.data_reader_from_file(path=file_path)
            self.data = self.data._append(df, ignore_index=False)
        return self.data




# /Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT2023-01-01.csv.gz
# /Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT2024-08-09.csv.gz",

if __name__ == "__main__":
    reader = DataReader(dir_path="/Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT")
    df = reader.daterange(datetime(2024, 8,1),datetime(2024, 8, 4))
    print(df.shape)

# 2024-08-09.csv.gz