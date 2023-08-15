import random
from typing import List
import tqdm

from AttendencePredictor import get_predictor
from DataGenerator import DataGenerator
from MutationOperator import MutationOperator
from Patient import Patient
from SelectionOperator import SelectionOperator


class Schedule:
    """
    Class to represent a schedule of patients.
    """
    def __init__(self, patient_schedule, classifier, appointment_duration=20, overlap=0.1):
        """
        :param patient_schedule: List<Patient>. Represents the ordering of a schedule of patients.
        :param appointment_duration: Int. Represents the assigned duration of each appointment.
        """
        self.appointment_duration = appointment_duration
        self.overlap = overlap
        self.schedule = patient_schedule
        self.classifier = classifier
        self.__assign_times()
        self.fitness = 0

    def set_fitness(self, fitness):
        """
        Method to set the fitness the schedule
        :param fitness: Int. Represents the fitness score of the schedule.
        :return: None
        """
        self.fitness = fitness

    def has_no_duplicates(self):
        patients_schedules = self.schedule
        return len(patients_schedules) == len(set(patients_schedules))

    def __len__(self):
        return len(self.schedule)

    def __getitem__(self, index):
        return self.schedule[index]

    def __setitem__(self, index, value):
        self.schedule[index] = value

    def __str__(self):
        output = ""
        for patient in self.schedule:
            output += f"{patient} ->"
        return output[:-2]

    def __assign_times(self):
        """
        Private method to assign each patient an appointment start time.
        :return: None
        """
        previous_patient = None
        for patient in self.schedule:
            if previous_patient is None:
                patient.start_time = 0
            elif self.classifier.attends(patient):
                patient.start_time = previous_patient.start_time + (self.appointment_duration * (1 - self.overlap))
            else:
                patient.start_time = previous_patient.start_time

            previous_patient = patient



class Schedular:
    def __init__(self, patients, mutation_name="swap", selection_name="tournament"):
        self.classifier = get_predictor()
        self.mutation_operator = MutationOperator(mutation_name)
        self.selection_operator = SelectionOperator(selection_name)

        self.patients = patients
        self.population = []
        self.population_size = 1000
        self.num_iterations = 1000
        self.num_restarts = 1
        self.parent_count = 20

        self.best = None

    def run(self):
        for i in range(self.num_restarts):
            self.population = []
            if self.best:
                self.population.append(self.best)
            for i in range(self.population_size):
                self.population.append(
                    Schedule(
                        self.create_individual(),
                        self.classifier
                    )
                )

            for run in tqdm.tqdm(range(self.num_iterations)):
                for candidate in self.population:
                    candidate.set_fitness(
                        self.fitness(
                            candidate.schedule
                        )
                    )

                parents = self.selection(self.population, self.parent_count)
                offspring = []
                while len(offspring) < self.population_size:
                    parent1, parent2 = self.select_two_parents(parents)
                    child1, child2 = self.cross_over(parent1, parent2)
                    child1 = self.mutation_operator.mutate(child1)
                    child2 = self.mutation_operator.mutate(child2)
                    child1 = Schedule(child1, self.classifier)
                    child1.set_fitness(self.fitness(child1.schedule))
                    child2 = Schedule(child2, self.classifier)
                    child2.set_fitness(self.fitness(child2.schedule))
                    offspring.append(child1)
                    offspring.append(child2)
                self.population = offspring
            self.best = self.get_best_schedule()
        return self.get_best_schedule()

    def get_best_schedule(self):
        sorted_schedules = sorted(self.population, key=lambda x: x.fitness)
        return sorted_schedules[-1]

    def cross_over(self, parent1, parent2):
        start = random.randint(0, len(parent1) - 2)
        end = random.randint(start, len(parent1) - 1)
        child1 = parent1[start:end]
        child2 = parent2[start:end]

        for index, patient in enumerate(parent1[0: start]):
            child1.insert(index, patient)

        for patient in parent1[end:]:
            child1.append(patient)

        for index, patient in enumerate(parent2[0: start]):
            child2.insert(index, patient)

        for patient in parent2[end:]:
            child2.append(patient)

        return child1, child2

    def select_two_parents(self, parents):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        while parent2 == parent1:
            parent2 = random.choice(parents)
        return parent1, parent2

    def fitness(self, schedule: List[Patient]):
        used_time = 0
        wasted_time = 0
        current_time = 0

        for i in range(len(schedule) - 1):
            patient = schedule[i]
            if self.classifier.attends(patient):
                used_time += patient.appointment_duration
                wasted_time += max(0, patient.start_time - current_time)
                current_time = max(current_time, patient.start_time) + patient.appointment_duration

        return (used_time + 0.000001) / (wasted_time + used_time + 0.000001)

    def create_individual(self):
        random.shuffle(self.patients)
        return self.patients

    def mutate(self, individual, rate):
        if random.random() < rate:
            return self.mutation_operator.mutate(individual)

    def selection(self, population, num_parents):
        return self.selection_operator.selection(population, num_parents)


if __name__ == '__main__':
    dataGenerator = DataGenerator(
        3,
        0.8,
        [(1, 5), (6, 10), (11, 15), (16, 20), (21, 30), (31, 60)],
        [0.223, 0.264, 0.198, 0.126, 0.118, 0.071]
    )

    patients = dataGenerator.get_patients()
    random.seed(1)
    schedular = Schedular(
        patients,
        selection_name="rank_based"
    )
    schedule = schedular.run()
    print(schedule)
    print(schedule.has_no_duplicates())
    print(schedule.fitness)
