import numpy as np

from genetic.crossover.crossover_abstract import Crossover

p1 = [1, 2, 3, 5, 4, 6, 7, 8, 9]
p2 = [4, 5, 2, 1, 8, 7, 6, 9, 3]

class OrderCrossover(Crossover):
    def run(self):
        x1, x2 = np.sort(np.random.choice(range(len(self.p1)), 2, replace=False))
        n = len(self.p1)
        for_searching = self.p2[x2:n] + self.p2[:x2]
        to_insert = [el for el in for_searching if el not in self.p1[x1:x2]]
        c = to_insert[n - x2:] + self.p1[x1:x2] + to_insert[:n - x2]
        return c

# oc = OrderCrossover()
# c = oc.run()
# print(c)
