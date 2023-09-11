import numpy as np

from genral.util import read_customers_in_dict


class AntColonyTSP:
    def __init__(self, customers, distances, num_ants, num_iterations, alpha, beta, rho, q, vehicle_capacity):
        self.customers = customers
        self.distances = distances
        self.num_customers = distances.shape[0] if distances is not None else 0
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.pheromone = np.ones((self.num_customers, self.num_customers))
        self.depot = 0
        self.vehicle_capacity = vehicle_capacity

    def run(self):
        best_path = None
        best_distance = np.inf
        for i in range(self.num_iterations):
            paths = self.generate_ant_paths()
            self.update_pheromone(paths)
            best_distance, best_path = self.update_best(paths, best_distance, best_path)
        return best_path, best_distance

    def update_best(self, paths, best_distance, best_path):
        for path in paths:
            distance = self.calculate_path_distance(path)
            if distance < best_distance:
                best_distance = distance
                best_path = path
        return best_distance, best_path


    def generate_ant_paths(self):
        paths = []
        for _ in range(self.num_ants):
            path = self.construct_path()
            paths.append(path)
        return paths

    def construct_path(self):
        path = []
        visited = set()
        current_customer = self.depot
        visited.add(current_customer)
        path.append(current_customer)
        remaining_capacity = self.vehicle_capacity

        while len(visited) < self.num_customers:
            next_customer = self.choose_next_customer(current_customer, visited, remaining_capacity)
            path.append(next_customer)
            current_customer = next_customer
            remaining_capacity -= self.customers[next_customer].demand
            if next_customer == self.depot:
                remaining_capacity = self.vehicle_capacity
            else:
                visited.add(next_customer)

        path.append(self.depot)
        return path

    def calculate_probabilities(self, current_customer, unvisited_customers, remaining_capacity):
        probabilities = []
        for cust in unvisited_customers:
            if self.customers[cust].demand > remaining_capacity:
                p = 0
            else:
                p = (self.pheromone[current_customer][cust] ** self.alpha) * (1.0 / self.distances[current_customer][cust] ** self.beta)
            probabilities.append(p)
        return probabilities

    def choose_next_customer(self, current_customer, visited, remaining_capacity):
        unvisited_customers = set(range(self.num_customers)) - visited
        unnormalized_probabilities = self.calculate_probabilities(current_customer, unvisited_customers, remaining_capacity)
        if sum(unnormalized_probabilities) == 0: return 0
        unnormalized_probabilities /= np.sum(unnormalized_probabilities)
        next_customer = np.random.choice(list(unvisited_customers), p=unnormalized_probabilities)
        return next_customer

    def update_pheromone(self, paths):
        delta_pheromone = np.zeros((self.num_customers, self.num_customers))
        for path in paths:
            path_distance = self.calculate_path_distance(path)
            for i in range(self.num_customers - 1):
                delta_pheromone[path[i]][path[i+1]] += self.q / path_distance

        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone


    def calculate_path_distance(self, path):
        path = [0] + path
        distance = sum(self.distances[path[i]][path[i+1]] for i in range(len(path) - 1))
        distance += self.distances[path[-1]][path[0]]
        path.pop(0)
        return distance


    @staticmethod
    def calculate_distance_matrix(customers):
        num_customers = len(customers)
        distance_matrix = np.zeros((num_customers, num_customers))

        for i in range(num_customers):
            for j in range(i, num_customers):
                x1, y1 = customers[i].x, customers[i].y
                x2, y2 = customers[j].x, customers[j].y
                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
        return distance_matrix


if __name__ == "__main__":
    NUM_ANTS = 50
    NUM_ITERATIONS = 300
    ALPHA = 1
    BETA = 2
    EVAPORATION_RATE = 0.1
    PHEROMONE_DEPOSIT = 1
    VEHICLE_CAPACITY = 20

    customers = read_customers_in_dict("../genral/files/customers1.txt")
    distances = AntColonyTSP.calculate_distance_matrix(customers)
    ant_colony = AntColonyTSP(customers, distances, NUM_ANTS, NUM_ITERATIONS, ALPHA, BETA, EVAPORATION_RATE, PHEROMONE_DEPOSIT, VEHICLE_CAPACITY)

    best_path, best_distance = ant_colony.run()

    print("Najbolja ruta:", best_path)
    print("Duzina:", best_distance)
