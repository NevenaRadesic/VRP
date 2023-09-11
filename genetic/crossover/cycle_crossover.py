from genetic.crossover.crossover_abstract import Crossover


class CycleCrossover(Crossover):
    def find_next(self, c, last_inserted):
        index = self.p1.index(last_inserted)
        next = self.p2[index]
        if next not in c:
            new_index = self.p1.index(next)
            c[new_index] = next
            return c, next
        return c, -1


    def fill_others(self, c):
        to_be_inserted = [elem for elem in self.p2 if elem not in c]
        counter = 0
        for i in range(len(c)):
            if c[i] == -1:
                c[i] = to_be_inserted[counter]
                counter += 1
        return c


    def run(self):
        c = [-1] * len(self.p1)
        c[0] = self.p1[0]
        last_inserted = self.p1[0]
        while True:
            c, next_element = self.find_next(c, last_inserted)
            last_inserted = next_element
            if next_element == -1:
                break
        c = self.fill_others(c)
        return c

# p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# p2 = [4, 1,2, 8, 7, 6, 9, 3, 5]
# cc = CycleCrossover()
# c1 = cc.run()
# print(c1)




