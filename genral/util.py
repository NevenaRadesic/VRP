from genral.Customer import Customer
from genral.Vehicle import Vehicle


def read_customers_from_file(path):
    customers = []
    with open(path, 'r') as file:
        for line in file:
            id, name, x, y, demand = line.strip().split('|')
            c = Customer(int(id), name, int(x), int(y), int(demand))
            customers.append(c)
    return customers


def read_customers_in_dict(path):
    customers = {}
    with open(path, 'r') as file:
        for line in file:
            id, name, x, y, demand = line.strip().split('|')
            c = Customer(int(id), name, int(x), int(y), int(demand))
            customers[int(id)] = c
    return customers


def read_vehicles_from_file(path):
    vehicles = []
    with open(path, 'r') as file:
        for line in file:
            id, name, x, y, capacity = line.strip().split('|')
            v = Vehicle(int(id), name, int(x), int(y), int(capacity))
            vehicles.append(v)
    return vehicles


def read_vehicles_in_dict(path):
    vehicles = {}
    with open(path, 'r') as file:
        for line in file:
            id, name, x, y, capacity = line.strip().split('|')
            v = Vehicle(int(id), name, int(x), int(y), int(capacity))
            vehicles[int(id)] = v
    return vehicles


