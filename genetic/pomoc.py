import math

from genral.util import read_customers_from_file, read_vehicles_from_file


class Pomoc():
    def __init__(self, customers, vehicles, mutation_rate):
        # self.route = [7, 8, 10, 11, 1001, 9, 13, 14, 12, 1002, 4, 1, 3, 1007, 6, 5, 1006, 1004, 1005, 1003, 1000]
        # self.route = [1005, 4, 3, 7, 8, 10, 11, 1006, 1002, 1001, 5, 6, 1004, 2, 1, 1000, 1003, 9, 13, 14, 12, 1007]
        # self.route = [12, 14, 13, 9, 1001, 6, 5, 1002, 1007, 7, 1, 2, 1003, 4, 1004, 3, 8, 10, 11, 1005, 1006, 1000 ]
        # self.route = [11, 12, 8, 7, 1000, 2, 1, 1007, 5, 6, 1003, 10, 14, 13, 9, 1004, 3 ,1005, 4, 1001 ,1006, 1002]
        # self.route = [1006 ,4 ,1001, 1000, 11, 10 ,13 ,7 ,1002 ,12, 14, 8, 1003 ,2 ,1 ,3, 1004, 5, 6 ,1005, 9, 1007]
        # self.route = [13, 14, 12, 9 ,1001, 4, 1004, 1006, 3 ,1, 2 ,1002, 5 ,11, 10, 8, 7 ,1005, 1000 ,1007 ,1003, 6]
        self.route = [1 ,2 ,1000, 6 ,7 ,1001 ,5 ,8 ,10, 11, 1004, 13 ,14 ,12 ,1003, 4 ,1005 ,3 ,9, 1007, 1006, 1002]
        self.customers = customers
        self.vehicles = vehicles
        self.mutation_rate = mutation_rate

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

    def is_vehicle(self, p):
        for vehicle in self.vehicles:
            if vehicle.id == p:
                return True
        return False

    def get_vehicle_capacity_by_id(self, n):
        for vehicle in self.vehicles:
            if vehicle.id == n:
                return vehicle.capacity

    def calculate_distance(self, p1, p2):
        n1 = self.find_by_id(p1)
        n2 = self.find_by_id(p2)
        return math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)

    def find_by_id(self, p):
        for vehicle in self.vehicles:
            if vehicle.id == p:
                return vehicle
        return self.customers[p]


customers = read_customers_from_file("../genral/files/customers1.txt")
vehicles = read_vehicles_from_file("../genral/files/vehicles1.txt")
p = Pomoc(customers, vehicles, 0.5)
print(p.calculate_fitness())
