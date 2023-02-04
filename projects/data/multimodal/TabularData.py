from __future__ import annotations

from dataclasses import field

import pandas as pd
from sklearn.model_selection import train_test_split

from projects.data.BaseData import BaseData


class TabularData(BaseData):
    def __init__(self) -> None:
        super().__init__()
        self.data: pd.DataFrame = pd.DataFrame()
        self.input_columns: [str] = []
        self.target_columns: [str] = None
        self.target_numbers: int = field(default=0)

    def load(self, data_or_path: [str | pd.DataFrame], **kwargs):
        if type(data_or_path) == str:
            if data_or_path.endswith('.csv'):
                self.read_from_csv(data_or_path, **kwargs)
            elif data_or_path.endswith('.html'):
                self.read_from_html(data_or_path, **kwargs)
            elif data_or_path.endswith('.json'):
                self.read_from_json(data_or_path, **kwargs)
            elif data_or_path.endswith('.xlsx'):
                self.read_from_excel(data_or_path, **kwargs)
            else:
                raise Exception('Unknown file type')
        if type(data_or_path) == pd.DataFrame:
            self.data = data_or_path

        return self

    def save(self, path, **kwargs):
        if path.endswith('.csv'):
            self.save_to_csv(path, **kwargs)
        elif path.endswith('.html'):
            self.save_to_html(path, **kwargs)
        elif path.endswith('.json'):
            self.save_to_json(path, **kwargs)
        elif path.endswith('.xlsx'):
            self.save_to_excel(path, **kwargs)
        else:
            raise Exception('Unknown file type')
        return self

    def get_train_test(self, split_ratio=0.2, **kwargs):
        X = self.data[self.input_columns]
        y = self.data[self.target_columns]
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=split_ratio,
                                                            **kwargs)
        if self.target_numbers == 1:
            return x_train.values, x_test.values, \
                   y_train.values.reshape(-1, 1), y_test.values.reshape(-1, 1)
        return x_train.values, x_test.values, y_train.values, y_test.values

    def set_input_target(self, input_columns, target_columns):
        self.input_columns = input_columns
        if type(target_columns) == list:
            if len(target_columns) == 1:
                self.target_columns = target_columns[0]
                self.target_numbers = 1
            else:
                self.target_columns = target_columns
                self.target_numbers = len(target_columns)
        else:
            self.target_columns = target_columns
            self.target_numbers = 1
        return self

    def read_from_html(self, path, **kwargs):
        self.data = pd.read_html(path, **kwargs)

    def read_from_csv(self, path, **kwargs):
        self.data = pd.read_csv(path, **kwargs)

    def read_from_excel(self, path, **kwargs):
        self.data = pd.read_excel(path, **kwargs)

    def read_from_json(self, path, **kwargs):
        self.data = pd.read_json(path, **kwargs)

    def save_to_csv(self, path, **kwargs):
        self.data.to_csv(path, **kwargs)

    def save_to_excel(self, path, **kwargs):
        self.data.to_excel(path, **kwargs)

    def save_to_json(self, path, **kwargs):
        self.data.to_json(path, **kwargs)

    def save_to_html(self, path, **kwargs):
        self.data.to_html(path, **kwargs)

    def save_to_pickle(self, path, **kwargs):
        self.data.to_pickle(path, **kwargs)
