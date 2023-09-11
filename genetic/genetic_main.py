import math
import random
import matplotlib.pyplot as plt

from genetic.Population import Population
from genetic.crossover.alternating_edges_crossover import AlternatingEdgesCrossover
from genetic.crossover.cycle_crossover import CycleCrossover
from genetic.crossover.edge_recombination_crossover import EdgeRecombinationCrossover
from genetic.crossover.order_crossover import OrderCrossover
from genetic.crossover.partially_mapped_crossover import PartiallyMappedCrossover
from genral.util import read_customers_from_file, read_vehicles_from_file


class GeneticAlgorithm(object):
    def __init__(self, customers, vehicles, num_vehicles, num_generations, mutation_rate, population_size, elitism, crossover):
        self.customers = customers
        self.vehicles = vehicles
        self.num_vehicles = num_vehicles
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.elitism = elitism
        self.crossover = crossover


    def run(self):
        population = Population(customers, vehicles, population_size, self.num_vehicles, self.elitism, self.mutation_rate, self.crossover)
        population.generate_initial_population()
        plt.ion()
        for i in range(num_generations):
            population.generate_new_population()
            population.write_sorted_fitness()
            # population.print_route()
            population.rank_individuals()
            population.draw_route()
        population.print_route()
        population.draw_final_route()
        print('kraj')
        plt.ioff()



customers = read_customers_from_file("../genral/files/customers1.txt")
vehicles = read_vehicles_from_file("../genral/files/vehicles1.txt")
num_vehicles = 5
num_generations = 100
mutation_rate = 0.6
population_size = 100
elitism = 4
# crossover = AlternatingEdgesCrossover()
# crossover = CycleCrossover()
crossover = EdgeRecombinationCrossover()
# crossover = OrderCrossover()
# crossover = PartiallyMappedCrossover()

ga = GeneticAlgorithm(customers, vehicles, num_vehicles, num_generations, mutation_rate, population_size, elitism, crossover)
best_route = ga.run()
