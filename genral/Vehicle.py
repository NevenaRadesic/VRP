from genral.Node import Node

class Vehicle(Node):
    def __init__(self, id, name, x, y, capacity):
        super().__init__(id, name, x, y)
        self.capacity = capacity
