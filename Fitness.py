from typing import List
import matplotlib.pyplot as plt
import matplotlib as mpl

from Patient import Patient


class Fitness:
    """
    Class to represent fitness related functions.
    """

    def __init__(self):
        self.current_time = 0
        self.used_time = 0
        self.wasted_time = 0

    def get_fitness(self, schedule: List[Patient]):
        """
        Method to get the fitness score of a scheduled list of patients.
        """

        for i in range(len(schedule) - 1):
            patient = schedule[i]
            if patient.attends:
                self.used_time += patient.appointment_duration
                self.wasted_time += max(0, patient.start_time - self.current_time)
                self.current_time = max(self.current_time, patient.start_time) + patient.appointment_duration

        return self.used_time / (self.wasted_time + self.used_time)

    def create_graph(self, path_to_save, title):
        """
        Method to create a graph based on the wasted time and used time.
        :param path_to_save: path to save the file to.
        :return: path to graph on local file system.
        """
        mpl.use('TkAgg')
        x_values = ["Utilized Time", "Wasted Time"]
        y_values = [self.used_time, self.wasted_time]
        plt.bar(x_values, y_values, width=0.5, color=["green", "red"])
        for i, value in enumerate(y_values):
            plt.text(i, value, str(value), ha="center")
        plt.ylabel("Mins")
        plt.title(title)

        plt.savefig(path_to_save)
        plt.clf()

