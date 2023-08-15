import names
import pandas as pd


class Patient:
    def __init__(self, appointment_duration, name=None):
        self.__appointment_duration = appointment_duration
        self.__attends = None
        self.meta_data = None
        self.predicted_attendance = None
        self.__assign_meta_data()

        self.__start_time = 0
        if name is None:
            name = names.get_full_name()

        self.name = name

    @property
    def appointment_duration(self):
        return self.__appointment_duration

    @appointment_duration.setter
    def appointment_duration(self, appointment_duration):
        self.__appointment_duration = appointment_duration

    @property
    def attends(self):
        return self.__attends

    @attends.setter
    def attends(self, attends):
        self.__attends = attends

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time

    def __str__(self):
        return self.name

    def __assign_meta_data(self):
        df = pd.read_csv('data/test_data.csv')
        row = df.sample(replace=False)
        self.__attends = bool(row["Label"].to_numpy()[0] != 1.0)
        meta_data = row.iloc[:, :-1]
        self.meta_data = meta_data.to_numpy()

