import random

from genetic.crossover.crossover_abstract import Crossover


class AlternatingEdgesCrossover(Crossover):

    def find_next_element(self, c):
        last_inserted = c[-1]
        index = self.p2.index(last_inserted)
        # moglo je i ovako
        # if index<len(p2) - 1:
        #     return p2[index + 1]
        # return p2[0]
        return self.p2[(index + 1) % len(self.p2)]

    def find_any(self, c):
        not_selected_yet = [elem for elem in self.p2 if elem not in c]
        return random.choice(not_selected_yet)

    def run(self):
        # prva dva smo uzeli od prvog roditelja
        c = [self.p1[0], self.p1[1]]
        for i in range(len(self.p1) - 2):
            n = self.find_next_element(c)
            if n not in c:
                self.p2, self.p1 = self.p1, self.p2
            else:
                n = self.find_any(c)
            c.append(n)
        return c


# p1 = [5, 1, 7, 8, 4, 9, 6, 2, 3]
# p2 = [3, 6, 2, 5, 1, 9, 8, 4, 7]
#
# aec = AlternatingEdgesCrossover()
# print(aec.run())
