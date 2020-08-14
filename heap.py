

class Heap:

    def __init__(self):
        self.heap = []

    def add(self, node):
        self.heap.append(node)
        self.sort_up(node)

    def remove_first(self):
        first_item = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop(-1)
        if len(self.heap) > 0:
            self.sort_down(self.heap[0])
        return first_item

    def sort_down(self, node):
        while True:
            node_i = self.heap.index(node)
            left_child_i = node_i * 2 + 1
            right_child_i = node_i * 2 + 2
            swap_index = 0

            if left_child_i < len(self.heap):
                swap_index = left_child_i
                if right_child_i < len(self.heap):
                    if self.heap[left_child_i].compare_to(self.heap[right_child_i]) < 0:
                        swap_index = right_child_i
                if node.compare_to(self.heap[swap_index]) < 0:
                    self.swap(node, self.heap[swap_index])
                else:
                    return
            else:
                return

    def sort_up(self, node):
        node_i = self.heap.index(node)
        parent_i = (node_i - 1) // 2
        while True:
            if parent_i < 0:
                break
            parent = self.heap[parent_i]
            if node.compare_to(parent) > 0:
                self.swap(node, parent)
            else:
                break
            node_i = self.heap.index(node)
            parent_i = (node_i - 1) // 2

    def swap(self, node1, node2):
        node1_i = self.heap.index(node1)
        node2_i = self.heap.index(node2)
        self.heap[node1_i], self.heap[node2_i] = node2, node1

