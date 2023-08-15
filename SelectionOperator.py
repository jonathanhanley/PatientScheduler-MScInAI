import random


class SelectionOperator:

    def __init__(self, selection_name):
        self.__selection_name = selection_name
        self.__selection_methods = {
            "tournament": self.__tournament_selection,
            "roulette_wheel": self.__roulette_wheel_selection,
            "rank_based": self.__rank_based_selection
        }

    def selection(self, population, num_parents):
        return self.__selection_methods[self.__selection_name](population, num_parents)

    def __tournament_selection(self, population, num_parents):
        tournament_size = int(len(population) * 0.25)
        parents = []

        # repeat tournament process to select desired number of parents
        while len(parents) < num_parents:
            # randomly select a subset of the population
            tournament = random.sample(population, tournament_size)

            # select the fittest individual in the tournament as a parent
            parent = max(tournament, key=lambda individual: individual.fitness)
            if parent not in parents:
                parents.append(parent)

        return parents

    def __roulette_wheel_selection(self, population, num_parents):
        # calculate total fitness of the population
        total_fitness = sum(individual.fitness for individual in population)

        # assign probabilities proportional to fitness
        probabilities = [individual.fitness / total_fitness for individual in population]

        parents = []

        for i in range(num_parents):
            # spin the wheel to select a parent
            parent_index = random.choices(range(len(population)), weights=probabilities)[0]
            parents.append(population[parent_index])

        return parents

    def __rank_based_selection(self, population, num_parents):
        sorted_pop = sorted(population, key=lambda x: x.fitness, reverse=True)
        # Assign a rank to each individual based on its position in the sorted population
        ranks = [i + 1 for i in range(len(sorted_pop))]
        rank_sum = sum(ranks)
        probabilities = [rank / rank_sum for rank in ranks]
        parents = []
        for i in range(num_parents):
            parent = random.choices(sorted_pop, probabilities)[0]
            parent_index = sorted_pop.index(parent)
            del sorted_pop[parent_index]
            del probabilities[parent_index]
            parents.append(parent)

        return parents