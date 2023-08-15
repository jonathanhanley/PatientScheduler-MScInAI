import random


class MutationOperator:
    def __init__(self, mutation_name):
        self.__mutation_name = mutation_name
        self.__mutation_methods = {
            "swap": self.__swap_mutation,
            "scramble": self.__scramble_mutation,
            "inversion": self.__inversion_mutation
        }

    def mutate(self, individual):
        return self.__mutation_methods[self.__mutation_name](individual)

    def __swap_mutation(self, individual):
        left_index = random.randint(0, len(individual) - 1)
        right_index = random.randint(0, len(individual) - 1)
        individual[left_index], individual[right_index] = individual[right_index], individual[left_index]
        return individual

    def __scramble_mutation(self, individual):
        left_index = random.randint(0, len(individual) - 2)
        right_index = random.randint(left_index, len(individual) - 1)
        left_copy = individual[0: left_index]
        right_copy = individual[right_index:]
        middle = individual[left_index: right_index]
        random.shuffle(middle)
        return left_copy + middle + right_copy

    def __inversion_mutation(self, individual):
        left_index = random.randint(0, len(individual) - 2)
        right_index = random.randint(left_index, len(individual) - 1)
        left_copy = individual[0: left_index]
        right_copy = individual[right_index:]
        middle = individual[left_index: right_index][::-1]
        return left_copy + middle + right_copy