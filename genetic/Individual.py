import math
import random

import numpy as np


class Individual(object):
    def __init__(self, route, customers, vehicles, mutation_rate):
        self.route = route
        self.customers = customers
        self.vehicles = vehicles
        self.mutation_rate = mutation_rate
        # self.fitness = self.calculate_fitness()


    def calculate_fitness(self):
        full_route = [1000] + self.route + [1000] + [1000]
        total_distance = 0
        # total_distance += self.calculate_distance(0, self.route[0])
        current_demands = 0
        for i in range(len(full_route) - 1):
            # n je trenutni id
            n = full_route[i]
            total_distance += self.calculate_distance(full_route[i], full_route[i + 1])
            # sad treba da vidim da li je u pitanju vozilo ili klijent
            if self.is_vehicle(n):
                # ako smo dosli do vozila, treba da vidim da li je prekrseno pravilo o zapremini
                # diff = current_demands - self.get_vehicle_capacity_by_id(n)
                # if diff > 0:
                #     total_distance += 100
                if current_demands > self.get_vehicle_capacity_by_id(n):
                    total_distance += 100
                current_demands = 0
            else:
                # ako je klijent
                customer = self.customers[n]
                current_demands += customer.demand

        # total_distance += self.calculate_distance(self.route[-1], 0)
        return total_distance


    def mutate(self):
        r = random.random()
        if r < self.mutation_rate:
            i, j = np.sort(np.random.choice(range(len(self.route)), 2, replace=False))
            self.route[i], self.route[j] = self.route[j], self.route[i]
        return self

    def calculate_distance(self, p1, p2):
        n1 = self.find_by_id(p1)
        n2 = self.find_by_id(p2)
        return math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

    # ako ga ima u vozilima, vrati ga, a ako ga nema, vrati iz liste klijenata
    def find_by_id(self, p):
        for vehicle in self.vehicles:
            if vehicle.id == p:
                return vehicle
        return self.customers[p]

    def is_vehicle(self, p):
        for vehicle in self.vehicles:
            if vehicle.id == p:
                return True
        return False

    def get_vehicle_capacity_by_id(self, n):
        for vehicle in self.vehicles:
            if vehicle.id == n:
                return vehicle.capacity


