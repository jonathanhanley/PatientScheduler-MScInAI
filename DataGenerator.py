import random
from Patient import Patient


class DataGenerator:
    """
    Class to generate data for testing purposes.
    """
    def __init__(self, population_size, probability_of_attending, durations, duration_weights):
        """
        :param population_size: Number of patients to create.
        :param probability_of_attending: The percentage chance of the patient attending their appointment.
        :param durations: List of Tuples. Each tuple represents a time range. (start_time, end_time)
        :param duration_weights: Weight to assign to each tuple of time range.
        """
        self.__population_size = population_size
        self.__probability_of_attending = probability_of_attending
        self.__durations = durations
        self.__duration_weights = duration_weights

    def get_patients(self):
        """
        Method to create all the patients.
        :return: List of patients.
        """
        patients = []

        for _ in range(self.__population_size):
            patients.append(
                Patient(
                    self.__get_appointment_duration()
                )
            )
        return patients

    def __get_appointment_duration(self):
        """
        Method to get an appointment duration based on the weights passed when creating an instance of DataGenerator.
        :return: INT representing the duration of an appointment.
        """
        appointment_range = random.choices(self.__durations, self.__duration_weights)[0]
        return random.randint(appointment_range[0], appointment_range[1])

    def __get_attends(self):
        """
        Method to get if a patient attends their appointment or not based on the probability passed when creating an
        instance of DataGenerator.
        :return:
        """
        return random.random() < self.__probability_of_attending
