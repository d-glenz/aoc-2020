import fileinput
import sys


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        self.lowest = sys.maxsize
        self.highest = -sys.maxsize
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                if elem < self.lowest:
                    self.lowest = elem
                if elem > self.highest:
                    self.higest = elem
                node.next = Node(data=elem)
                node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(map(str, nodes))

    def __getitem__(self, item):
        node = self.head
        num = 0
        while node is not None:
            if num == item:
                ll = LinkedList()
                ll.head = node
                return ll
            node = node.next
            num += 1

    def nodes(self):
        result = []
        node = self.head
        while node is not None:
            result.append(node.data)
            node = node.next
        return result

    def find(self, item):
        i = 0
        node = self.head
        while node is not None:
            if node.data == item:
                return i
            i += 1
            node = node.next


def move(cups, current_idx):
    current = cups[current_idx].head.data

    # the crab picks up three cups...
    three = cups[current_idx+1]
    fourth = cups[current_idx+4]
    cups.head.next = fourth.head
    three.head.next.next.next = None

    # selections a destination cup
    destination_label = current - 1
    while destination_label in three.nodes():
        destination_label = destination_label - 1 if destination_label - 1 > lowest_cup else highest_cup

    destination_idx = cups.find(destination_label)

    # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
    after = cups[destination_idx].head.next
    three.head.next.next.next = after
    cups[destination_idx].head.next = three.head

    # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    return cups, current_idx + 1


for line in fileinput.input():
    line = line.strip()
    cups = LinkedList(nodes=list(map(int, line)))

lowest_cup = cups.lowest
highest_cup = cups.highest
print(cups)

current_idx = 0
cups, current_idx = move(cups, current_idx)
print(cups)
