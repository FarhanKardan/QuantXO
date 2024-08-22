import pandas as pd
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
            self.data = df
        else:
            pass
        return df

    def daterange(self, start_date, end_date):
        days = int((end_date - start_date).days)
        for n in range(days):
            date = start_date + timedelta(n)
            file_path = self.dir_path + str(date.date()) + ".csv.gz"
            print("read the data from:", file_path)
            df = self.data_reader_from_file(path=file_path)
            self.data = self.data._append(df, ignore_index=False)
        return self.data
