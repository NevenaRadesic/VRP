# p1 = [1, 2, 3, 5, 4, 6, 7, 8, 9]
# p2 = [4, 5, 2, 1, 8, 7, 6, 9, 3]
import numpy as np

from genetic.crossover.crossover_abstract import Crossover

# p1 = [6, 7, 1000, 5, 9, 1001, 10, 3, 8, 1, 1002, 4, 2, 1003, 1004, 1005]
# p2 = [4, 7, 10, 8, 1000, 6, 1, 1001, 5, 3, 1002, 9, 2, 1003, 1004, 1005]
# p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# p2 = [9, 3, 8, 6, 7, 4, 5, 2, 1]

# x1 = 3
# x2 = 7
# x1 = 5
# x2 = 12


class PartiallyMappedCrossover(Crossover):
    def fill_with_dict(self, c1):
        for i in range(len(c1)):
            if c1[i] == -1:
                # ovo je trebalo da se slika
                should_have_been_inserted = self.p2[i]
                index = self.p1.index(should_have_been_inserted)
                to_be_inserted = self.p2[index]
                if to_be_inserted not in c1:
                    c1[i] = to_be_inserted
        return c1

    def fill_in_missing(self, c1):
        for i in range(len(self.p1)):
            if c1[i] == -1:
                if self.p2[i] not in c1:
                    c1[i] = self.p2[i]
        return self.fill_with_dict(c1)

    def fill_others(self, c1):
        if -1 in c1:
            not_filled = [elem for elem in self.p2 if elem not in c1]
            counter = 0
            for i in range(len(self.p2)):
                if c1[i] == -1:
                    c1[i] = not_filled[counter]
                    counter += 1
        return c1

    def run(self):
        n = len(self.p1)
        c1 = [-1] * n
        x1, x2 = np.sort(np.random.choice(range(len(self.p1)), 2, replace=False))
        c1[x1:x2] = self.p1[x1:x2]
        c1 = self.fill_in_missing(c1)
        c1 = self.fill_others(c1)
        return c1


# pmc = PartiallyMappedCrossover()
# pmc.p1 = p1
# pmc.p2 = p2
# c1 = pmc.run()
# print(c1)
