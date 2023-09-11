from genral.Node import Node


class Customer(Node):
    def __init__(self, id, name, x, y, demand):
        super().__init__(id, name, x, y)
        self.demand = demand
