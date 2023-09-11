import numpy as np

from genral.initial_population import get_initial_solution_tabu
from genral.util import read_customers_in_dict


class TabuSearch():

    def __init__(self, customers, tabu_size, max_iterations, vehicle_capacity, vehicle_count, number_of_attempts):
        self.customers = customers
        self.tabu_size = tabu_size
        self.max_iterations = max_iterations
        self.vehicle_capacity = vehicle_capacity
        self.number_of_attempts = number_of_attempts
        self.vehicle_count = vehicle_count

    def distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def total_distance(self, route):
        route = [0] + route
        total = 0
        for i in range(len(route) - 1):
            total += self.distance(self.customers[route[i]], self.customers[route[i + 1]])
        total += self.distance(self.customers[route[-1]], self.customers[route[0]])
        route.pop(0)
        return total

    def solution_is_valid(self, neighbor):
        remaining_capacity = self.vehicle_capacity
        for id in neighbor:
            if id == 0:
                remaining_capacity = self.vehicle_capacity
            else:
                remaining_capacity -= self.customers[id].demand
                if remaining_capacity < 0:
                    return False
        return True

    def find_neighbors(self, current_solution, num_customers):
        neighbors = []
        for i in range(1, num_customers + 1):
            for j in range(i + 1, num_customers + 1):
                neighbor = current_solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                if self.solution_is_valid(neighbor):
                    neighbors.append(neighbor)
        return neighbors

    def find_best_neighbor(self, neighbors, tabu_list):
        best_neighbor = None
        best_neighbor_distance = float('inf')

        for  neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_distance = self.total_distance(neighbor)
                if neighbor_distance < best_neighbor_distance:
                    best_neighbor = neighbor
                    best_neighbor_distance = neighbor_distance

        return best_neighbor

    def update_tabu_list(self, tabu_list, best_neighbor):
        tabu_list.append(best_neighbor)
        if len(tabu_list) > self.tabu_size:
            tabu_list.pop(0)

    def search(self, initial_solution):
        best_solution = initial_solution.copy()
        current_solution = best_solution.copy()
        tabu_list = []
        num_customers = len(self.customers) - 1

        for _ in range(self.max_iterations):
            neighbors = self.find_neighbors(current_solution, num_customers)
            best_neighbor = self.find_best_neighbor(neighbors, tabu_list)

            if best_neighbor is not None:
                current_solution = best_neighbor.copy()
                self.update_tabu_list(tabu_list, best_neighbor)

            if self.total_distance(current_solution) < self.total_distance(best_solution):
                best_solution = current_solution.copy()
        return best_solution

    def run(self):
        curr_best = float('inf')
        curr_route = None
        for i in range(self.number_of_attempts):
            initial_solution = get_initial_solution_tabu(self.customers.copy(), self.vehicle_count, self.vehicle_capacity)
            best_route = self.search(initial_solution)

            score = self.total_distance(best_route)
            if score < curr_best:
                curr_best = score
                curr_route = best_route
            print("Najbolja u ovoj iteraciji:", score)

        print('konacno najbolji:', curr_best)
        print('konacno najbolja ruta:', curr_route)


tabu_size = 20
max_iterations = 200
vehicle_capacity = 20
number_of_attempts = 20
vehicle_count = 10
customers = read_customers_in_dict("../genral/files/customers1.txt")
t = TabuSearch(customers, tabu_size, max_iterations, vehicle_capacity, vehicle_count, number_of_attempts)
t.run()
