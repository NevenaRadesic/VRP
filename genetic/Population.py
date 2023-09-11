import random
import numpy as np
import matplotlib.pyplot as plt

from genetic.Individual import Individual


class Population(object):
    def __init__(self, customers, vehicles, population_size, num_vehicles, elitism, mutation_rate, crossover_method):
        self.customers = customers
        self.vehicles = vehicles
        self.population_size = population_size
        self.num_vehicles = num_vehicles
        # self.vehicle_capacity = vehicle_capacity
        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.individuals = []
        self.crossover_method = crossover_method

    def generate_initial_population(self):
        self.individuals = []
        for i in range(self.population_size):
            c = self.customers.copy()
            random.shuffle(c)
            self.individuals.append(self.get_initial_inidividual(c))
        print("n")

    # id vozila se dodaje na kraj rute
    def get_initial_inidividual(self, customer_list):
        route = []
        vehicle_counter = 0
        remaining_capacity = self.vehicles[vehicle_counter].capacity
        for c in customer_list:
            if c.id != 0:
                if c.demand <= remaining_capacity:
                    route.append(c.id)
                    remaining_capacity -= c.demand
                else:
                    # dodamo vozilo za zavrsetak voznje
                    route.append(self.vehicles[vehicle_counter].id)
                    # dodamo sledeceg klijenta
                    route.append(c.id)
                    vehicle_counter += 1
                    # sada nam je kapacitet jednak kapacitetu narednog vozila
                    remaining_capacity = self.vehicles[vehicle_counter].capacity - c.demand
        route = self.add_rest_vehicles(route)
        # print("treci clan je", route[2])
        return Individual(route, self.customers, self.vehicles, self.mutation_rate)

    def generate_new_population(self):
        self.rank_individuals()
        elite = self.get_elite_members()
        children = self.generate_children()
        self.individuals = elite + children

    def rank_individuals(self):
        self.individuals = sorted(self.individuals, key=lambda c: c.calculate_fitness())

    # vraca prvih 6
    def get_elite_members(self):
        return self.individuals[:self.elitism]

    def generate_children(self):
        children = []
        for i in range(0, self.population_size - self.elitism, 2):
            parent1, parent2 = self.choose_pair_of_parents()
            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)
            children.append(child1.mutate())
            children.append(child2.mutate())
        return children

    def choose_pair_of_parents(self):
        max_val1 = max_val2 = float('-inf')
        index1 = index2 = 0
        for i in range(self.population_size):
            # skor je proporcionalan sa pozicijom u sortiranoj populaciji. Najbolje rangirani imaju malo i, pa je vrijednost veca
            # ja zelim sada da napravim da od najveceg oduzmemo trenutni i to mnozimo sa random
            score = (self.population_size - i + 1) * random.random()
            # max_fintess = self.individuals[-1].fitness
            # score = (max_fintess - self.individuals[i].fitness + 1) * random.random()
            if score > max_val1:
                max_val1, max_val2 = score, max_val1
                index1, index2 = i, index1
            elif score > max_val2:
                max_val2 = score
                index2 = i
        return self.individuals[index1], self.individuals[index2]

    def crossover(self, parent1, parent2):
        self.crossover_method.p1 = parent1.route
        self.crossover_method.p2 = parent2.route
        c = self.crossover_method.run()
        return Individual(c, self.customers, self.vehicles, self.mutation_rate)

    def write_sorted_fitness(self):
        fitnesses = [c.calculate_fitness() for c in self.individuals]
        sorted_fitnesses = sorted(fitnesses)
        print(sorted_fitnesses)


    def print_route(self):
        # print('najbolja ruta')
        # self.individuals = sorted(self.individuals, key=lambda c: c.fitness)
        # for r in self.individuals[0].route:
        #     print(r, end=" ")
        pass

    def add_rest_vehicles(self, route):
        for vehicle in self.vehicles:
            if vehicle.id not in route:
                route.append(vehicle.id)
        return route

    def draw_route(self):
        x_list, y_list = self.find_coordinate_list()
        plt.clf()
        plt.plot(x_list, y_list, 'ro')
        plt.plot(x_list, y_list)
        # plt.show(block=True)
        plt.pause(.03)

    def find_coordinate_list(self):
        x_list, y_list = [0], [0]
        best_individual = self.individuals[0]
        best_route = best_individual.route

        for i in range(len(best_route)):
            if best_route[i] < 500:
                x, y = self.customers[best_route[i]].x, self.customers[best_route[i]].y
                x_list.append(x)
                y_list.append(y)
            else:
                x_list.append(0)
                y_list.append(0)
        x_list.append(0)
        y_list.append(0)
        return x_list, y_list

    def draw_final_route(self):
        x_list, y_list = self.find_coordinate_list()
        plt.clf()
        plt.plot(x_list, y_list, 'ro')
        plt.plot(x_list, y_list)
        # plt.show(block=True)
        plt.pause(100)
