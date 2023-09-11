import random

from genetic.crossover.crossover_abstract import Crossover

p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
p2 = [4, 1,2, 8, 7, 6, 9, 3, 5]

x1 = 3
x2 = 7

class EdgeRecombinationCrossover(Crossover):
    def create_dict(self):
        dict = {}
        p1 = [self.p1[-1]] + self.p1 + [self.p1[0]]
        p2 = [self.p2[-1]] + self.p2 + [self.p2[0]]

        for i in range(1, len(p1) - 1):
            dict[p1[i]] = [p1[i-1], p1[i+1]]

        for i in range(1, len(p2) - 1):
            if p2[i-1] not in dict[p2[i]]:
                dict[p2[i]].append(p2[i-1])
            if p2[i+1] not in dict[p2[i]]:
                dict[p2[i]].append(p2[i+1])
        return dict


    def find_next(self, c1, dict):
        # sad treba uzeti zadnji i onda vidjeti ko su sve njegove komsije
        # print(self.p1, self.p2, "su roditelji")
        candidates = dict[c1[-1]]
        # sad od svih komsija treba odabrati onoga koji ima najmanje komsija
        # zapravo, ako ih ima vise, treba uzeti bilo koji
        while True:
            if len(candidates) > 0:
                curr = [candidates[0]]
                min_neigh = len(dict[candidates[0]])
                for elem in candidates:
                    if len(dict[elem])<min_neigh:
                        min_neigh = len(dict[elem])
                        curr = [elem]
                    elif len(dict[elem]) == min_neigh:
                        curr.append(elem)
                # mislim da sad tek mogu da obrisem sve vezano za ovog maloprije
                elem = random.choice(curr)
                if elem not in c1:
                    break
            else:
                elem = random.choice(list(dict.keys()))
                if elem not in c1:
                    break
        return elem


    def delete_element(self, dict, element):
        dict.pop(element)
        for key in dict:
            if element in dict[key]:
                dict[key].remove(element)
        return dict


    def create_child(self, c1, dict):
        while len(dict) > 1:
            elem = self.find_next(c1, dict)
            c1.append(elem)
            dict = self.delete_element(dict, c1[-2])
        return c1



    def run(self):
        c1 = [p1[0]]
        # c2 = [p2[0]]
        c1 = self.create_child(c1, self.create_dict())
        # c2 = self.create_child(c2, self.create_dict(p1, p2))
        return c1

# erc = EdgeRecombinationCrossover()
# c1 = erc.run()
# print(c1)