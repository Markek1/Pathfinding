import math, random

import heap

class Node:
    """g_cost - distance to starting node
       h_cost - distance to end node
       f_cost = g_cost + h_cost
    """
    def __init__(self, pos):
        self.pos = pos
        self.g_cost = math.inf
        self.h_cost = math.inf
        self.f_cost = math.inf
        self.previous = None
        self.make_walkable()

    def calculate_f_cost(self):
        self.f_cost = self.h_cost + self.g_cost

    def make_unwalkable(self):
        self.walkable = False
        self.color = (0, 0, 0)

    def make_walkable(self):
        self.walkable = True
        self.color = (255, 255, 255)

    def compare_to(self, node):
        dif_f_cost = self.f_cost - node.f_cost
        if dif_f_cost == 0:
            return -(self.h_cost - node.h_cost)
        else:
            return -dif_f_cost

    def __repr__(self):
        return f'{self.pos}'


class Grid:

    def __init__(self, dimensions, start_pos, end_pos):
        self.finished = False

        self.coefficient = 1

        self.dims = dimensions
        self.grid = [[Node((y, x)) for x in range(dimensions[1])] for y in range(dimensions[0])]

        self.open = heap.Heap()
        self.closed = set()

        self.start_pos = start_pos
        self.grid[start_pos[0]][start_pos[1]].g_cost = 0

        self.end_pos = end_pos
        self.grid[end_pos[0]][end_pos[1]].color = (0, 0, 255)

        self._close((start_pos[0], start_pos[1]))

        self.grid[start_pos[0]][start_pos[1]].color = (0, 0, 255)


    def _close(self, closed_pos):
        y, x = closed_pos[0], closed_pos[1]
        to_close = self.grid[y][x]
        self.closed.add(to_close)
        to_close.color = (255, 0, 0)
        self._find_all_open(closed_pos)

    def _find_all_open(self, closed_pos):
        c_y, c_x = closed_pos[0], closed_pos[1]
        s_y, s_x = self.start_pos[0], self.start_pos[1]
        e_y, e_x = self.end_pos[0], self.end_pos[1]
        for y in range(max(0, c_y - 1), min(self.dims[0], c_y + 2)):
            for x in range(max(0, c_x - 1), min(self.dims[1], c_x + 2)):
                to_open = self.grid[y][x]
                if (y == c_y and x == c_x) or to_open in self.closed or not to_open.walkable:
                    continue
                elif to_open.f_cost <= (self.grid[c_y][c_x].g_cost + self.distance((y, x), (s_y, s_x)) + self.coefficient * self.distance((y, x), (e_y, e_x))):
                        continue
                else:
                    to_open.g_cost = self.grid[c_y][c_x].g_cost + self.distance((y, x), (c_y, c_x))
                    to_open.h_cost = self.coefficient * self.distance((y, x), self.end_pos)
                    to_open.calculate_f_cost()
                    to_open.previous = self.grid[c_y][c_x]
                    if (y, x) != self.end_pos:
                        to_open.color = (0, 255, 0)
                    self.open.add(to_open)

    def next(self):
        min_dist = self.open.remove_first()

        if min_dist.pos == self.end_pos:
            self.finish(min_dist)
        else:
            self._close(min_dist.pos)

    def finish(self, last):
        self.finished = True
        at_start = False
        while not at_start:
            if last.pos == self.start_pos:
                at_start = True
            last.color = (0, 0, 255)
            last = last.previous

    def print_open(self):
        for key, value in self.open.items():
            print(key, value)

    @staticmethod
    def distance(first_pos, second_pos):
        f_y, f_x = first_pos[0], first_pos[1]
        s_y, s_x = second_pos[0], second_pos[1]
        return round(((f_x - s_x) ** 2 + (s_y - f_y) ** 2) ** 0.5 * 10)


if __name__ == '__main__':
    h = heap.Heap()
    nodes = []
    for j in range(10):
        node = Node((j, 0))
        node.g_cost = random.randint(1, 20)
        node.h_cost = random.randint(1, 20)
        node.calculate_f_cost()

        nodes.append(node)
    for node in nodes:
        h.add(node)
    for x in range(len(h.heap)):
        node = h.remove_first()
        print(x, node.f_cost, node.h_cost)
