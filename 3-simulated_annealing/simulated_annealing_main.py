import random
import math

from genral.initial_population import get_initial_solution_tabu
from genral.util import read_customers_in_dict


class SimulatedAnnealing():
    def __init__(self, customers, vehicle_capacity, initial_temperature, cooling_rate, max_iterations):
        self.customers = customers
        self.vehicle_capacity = vehicle_capacity
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def calculate_total_distance(self, route):
        total_distance = 0
        route = [0] + route
        for i in range(len(route) - 1):
            total_distance += self.euclidean_distance(self.customers[route[i]], self.customers[route[i + 1]])
        total_distance += self.euclidean_distance(self.customers[route[-1]],
                                                  self.customers[route[0]])  # Return to starting city
        route.pop(0)
        return total_distance

    def solution_is_valid(self, new_solution):
        remaining_capacity = self.vehicle_capacity
        for id in new_solution:
            if id == 0:
                remaining_capacity = self.vehicle_capacity
            else:
                remaining_capacity -= self.customers[id].demand
                if remaining_capacity < 0:
                    return False
        return True

    def generate_neighbor(self, solution):
        # iteriramo dok ne nadjemo resenje
        while True:
            new_solution = solution.copy()
            # Randomly select two distinct cities
            city1_idx = random.randint(0, len(new_solution) - 1)
            city2_idx = random.randint(0, len(new_solution) - 1)
            # Swap the cities
            new_solution[city1_idx], new_solution[city2_idx] = new_solution[city2_idx], new_solution[city1_idx]
            if self.solution_is_valid(new_solution):
                return new_solution

    def simulated_annealing(self, initial_solution, initial_temperature):
        current_solution = initial_solution
        best_solution = current_solution
        temperature = initial_temperature

        for iteration in range(self.max_iterations):
            neighbor_solution = self.generate_neighbor(current_solution)
            delta_distance = self.calculate_total_distance(neighbor_solution) - self.calculate_total_distance(
                current_solution)

            if delta_distance < 0 or random.random() < math.exp(-delta_distance / temperature):
                current_solution = neighbor_solution

                if self.calculate_total_distance(current_solution) < self.calculate_total_distance(best_solution):
                    best_solution = current_solution

            temperature *= self.cooling_rate

        return best_solution


vehicle_capacity = 20
initial_temperature = 110
cooling_rate = 0.99
max_iterations = 1000

customers = read_customers_in_dict("../genral/files/customers1.txt")
initial_solution = get_initial_solution_tabu(customers.copy(), 6, vehicle_capacity)
sa = SimulatedAnnealing(customers, vehicle_capacity, initial_temperature, cooling_rate, max_iterations)
best_solution = sa.simulated_annealing(initial_solution, initial_temperature)
print("Finalna ruta:", best_solution)
print("Distanca:", sa.calculate_total_distance(best_solution))
