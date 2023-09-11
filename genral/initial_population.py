import random

from genral.util import read_customers_from_file, read_customers_in_dict


def initialize_population(customers, num_vehicles, vehicle_capacity):
    population = []
    random.shuffle(customers)
    for i in range(num_vehicles):
        vehicle_route = []
        remaining_capacity = vehicle_capacity
        for customer in customers:
            if customer not in vehicle_route and customer['demand'] <= remaining_capacity:
                vehicle_route.append(customer)
                remaining_capacity -= customer['demand']
        population.append(vehicle_route)
    return population


VEHICLE_CAPACITY = 15
NUMBER_OF_VEHICLES = 5


def get_initial_solution(customers, depot):
    routes = []
    for i in range(NUMBER_OF_VEHICLES):
        route = [depot]
        remaining_capacity = VEHICLE_CAPACITY
        while customers:
            c = random.choice(customers)
            if c.demand < remaining_capacity:
                route.append(c)
                remaining_capacity -= c.demand
                customers.remove(c)
            else:
                route.append(depot)
                routes.append(route)
                break
    return routes

def get_initial_solution_indices(customers, depot):
    routes = []
    for i in range(NUMBER_OF_VEHICLES):
        # recimo da je ovo jedna ruta
        route = [depot.id]
        remaining_capacity = VEHICLE_CAPACITY
        while customers:
            c = random.choice(customers)
            if c.demand < remaining_capacity:
                route.append(c.id)
                remaining_capacity -= c.demand
                customers.remove(c)
            else:
                route.append(depot.id)
                routes.append(route)
                break
    return routes


def get_initial_solution_tabu(customers, vehicles_count, vehicle_capacity):
    routes = []
    depot = customers[0]
    customers.pop(0)
    for i in range(vehicles_count):
        route = [depot.id]
        remaining_capacity = vehicle_capacity
        while customers:
            c = random.choice(list(customers.values()))
            if c.demand <= remaining_capacity:
                route.append(c.id)
                remaining_capacity -= c.demand
                del customers[c.id]
            else:
                routes = routes + route
                break
        # dodamo posljednje vozilo
        if not customers: routes = routes + route
    return routes


#
# customers = read_customers_in_dict("../genral/files/customers1.txt")
# routes = get_initial_solution_tabu(customers, 10, 20)
# print(routes, len(routes))
#


# depot = customers[0]
# # skidamo skladiste
# customers.pop(0)
# routes = get_initial_solution(customers, depot)
