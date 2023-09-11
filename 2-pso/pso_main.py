import random
import numpy as np
import math

from genral.util import read_customers_in_dict, read_vehicles_in_dict


class ParticleSwarm():
    def __init__(self, customers, vehicles, num_particles, max_iterations, c1, c2, w, mutation_rate):
        self.customers = customers
        self.vehicles = vehicles
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.mutation_rate = mutation_rate

    def calculate_total_distance(self, route):
        total_distance = 0
        route = [1000] + route
        for i in range(len(route) - 1):
            total_distance += self.calculate_distance(route[i], route[i + 1])
        total_distance += self.calculate_distance(route[-1], route[0])
        route.pop(0)
        return total_distance

    def calculate_distance(self, p1, p2):
        n1 = self.find_by_id(p1)
        n2 = self.find_by_id(p2)
        return math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

    def convert_velocities_to_probabilities(self, velocity):
        min_el = min(velocity) - 1e-8
        centred = [elem - min_el for elem in velocity]
        sum_el = sum(centred)
        normalized = [elem / sum_el for elem in centred]
        return normalized

    def mutate(self, position):
        r = random.random()
        if r < self.mutation_rate:
            i, j = np.sort(np.random.choice(range(len(position)), 2, replace=False))
            position[i], position[j] = position[j], position[i]
        return position

    # ako je random broj manji od vjerovatnoce, onda tu poziciju pomijeramo tamo gdje je ona bila u local_best
    def update_position(self, position, velocity, local_best_position):
        probabilities = self.convert_velocities_to_probabilities(velocity)
        for i in range(len(probabilities)):
            r = random.random()
            if r < probabilities[i]:
                new_position = position.copy()
                j = np.where(local_best_position == position[i])[0][0]
                new_position[i], new_position[j] = new_position[j], new_position[i]
                new_position = self.mutate(new_position)
                # ako dobijeno resenje nije validno, vracamo na staro
                if self.solution_is_valid(new_position):
                    return new_position
        return position

    def update_best(self, particles, local_best, local_best_positions, global_best, global_best_position):
        for i in range(self.num_particles):
            total_distance = self.calculate_total_distance(particles[i])
            if total_distance < local_best[i]:
                local_best[i] = total_distance
                local_best_positions[i] = np.copy(particles[i])

            if total_distance < global_best:
                global_best = total_distance
                global_best_position = np.copy(particles[i])
        return local_best, local_best_positions, global_best, global_best_position

    def update_velocities_and_particles(self, velocities, particles, local_best_positions, global_best_position):
        for i in range(self.num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = self.w * velocities[i] + self.c1 * r1 * (
                        local_best_positions[i] - particles[i]) + self.c2 * r2 * (
                                    global_best_position - particles[i])
            particles[i] = self.update_position(particles[i], velocities[i], local_best_positions[i])
        return velocities, particles

    def generate_initial_path2(self):
        customer_list = self.customers.copy()
        route = []
        vehicle_counter = 0
        remaining_capacity = self.find_vehicle_by_counter(vehicle_counter).capacity
        for c_id in customer_list:
            c = self.customers[c_id]
            if c.id != 0:
                if c.demand <= remaining_capacity:
                    route.append(c.id)
                    remaining_capacity -= c.demand
                else:
                    route.append(self.find_vehicle_by_counter(vehicle_counter).id)
                    route.append(c.id)
                    vehicle_counter += 1
                    remaining_capacity = self.find_vehicle_by_counter(vehicle_counter).capacity - c.demand
        route = self.add_rest_vehicles(route)
        return route

    def generate_initial_path(self):
        remaining_customers = self.customers.copy()
        remaining_customers.pop(0)
        route = []
        vehicle_counter = 0
        remaining_capacity = self.find_vehicle_by_counter(vehicle_counter).capacity
        while remaining_customers:
            c = random.choice(list(remaining_customers.values()))
            remaining_customers.pop(c.id)
            if c.demand <= remaining_capacity:
                route.append(c.id)
                remaining_capacity -= c.demand
            else:
                route.append(self.find_vehicle_by_counter(vehicle_counter).id)
                route.append(c.id)
                vehicle_counter += 1
                remaining_capacity = self.find_vehicle_by_counter(vehicle_counter).capacity - c.demand
        route = self.add_rest_vehicles(route)
        return route

    def add_rest_vehicles(self, route):
        for vehicle_id in self.vehicles:
            if vehicle_id not in route:
                route.append(vehicle_id)
        return route

    def generate_initial_paths(self):
        return [self.generate_initial_path() for i in range(NUM_PARTICLES)]

    def run(self):
        num_nodes = len(self.customers) + len(self.vehicles) - 1
        particles = self.generate_initial_paths()
        velocities = np.zeros((self.num_particles, num_nodes), dtype=int)
        global_best = np.inf
        global_best_position = None
        local_best = np.full(self.num_particles, np.inf)
        local_best_positions = [np.copy(p) for p in particles]
        for iteration in range(self.max_iterations):
            local_best, local_best_positions, global_best, global_best_position = self.update_best(particles,
                                                                                                   local_best,
                                                                                                   local_best_positions,
                                                                                                   global_best,
                                                                                                   global_best_position)
            velocities, particles = self.update_velocities_and_particles(velocities, particles, local_best_positions,
                                                                         global_best_position)
        return global_best, global_best_position

    def find_vehicle_by_counter(self, vehicle_counter):
        return self.vehicles[1000 + vehicle_counter]

    def find_by_id(self, p):
        if p < 1000:
            return self.customers[p]
        return self.vehicles[p]

    def solution_is_valid(self, position):
        current_capacity = 0
        position.append(1000)
        for id in position:
            if self.is_vehicle(id):
                if current_capacity > self.find_vehicle_capacity_by_id(id):
                    position.pop()
                    return False
            else:
                current_capacity += self.find_customer_demand_by_id(id)
        position.pop()
        return True

    def is_vehicle(self, id):
        return id >= 1000

    def find_vehicle_capacity_by_id(self, id):
        return self.vehicles[id].capacity

    def find_customer_demand_by_id(self, id):
        return self.customers[id].demand


NUM_PARTICLES = 100
MAX_ITERATIONS = 100
C1 = 2
C2 = 2
W = 1
MUTATION_RATE = 0.2

customers = read_customers_in_dict("../genral/files/customers1.txt")
vehicles = read_vehicles_in_dict("../genral/files/vehicles1.txt")

pso = ParticleSwarm(customers, vehicles, NUM_PARTICLES, MAX_ITERATIONS, C1, C2, W, MUTATION_RATE)
best_solution, best_tour = pso.run()

print("Najbolji fitnes:", best_solution)
print("Najbolja ruta", best_tour)
