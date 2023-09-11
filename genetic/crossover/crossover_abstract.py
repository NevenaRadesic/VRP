from abc import abstractmethod, ABC


class Crossover(ABC):

    def __init__(self):
        self.p1 = None
        self.p2 = None

