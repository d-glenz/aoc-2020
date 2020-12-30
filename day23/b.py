import fileinput
import sys


class Node:
    def __init__(self, data, head=None):
        self.data = data
        self.next = None
        self.head = head if head is not None else self

    def __repr__(self):
        return self.data

    def getnext(self):
        if self.next is None:
            return self.head
        return self.next


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        self.lowest = sys.maxsize
        self.highest = -sys.maxsize
        self.len = 1
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            head = node
            self.head = node
            for elem in nodes:
                elem = int(elem)
                if elem < self.lowest:
                    self.lowest = elem
                if elem > self.highest:
                    self.highest = elem
                node.next = Node(data=elem, head=head)
                node = node.next
                self.len += 1

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
        print(f"__getitem__: {item=}, {self.len=}")
        item = item if item < self.len else item - self.len
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
        print(f"{item=} not found")


def move(cups, current_idx):
    print(f"current_idx={current_idx}")
    current = cups[current_idx].head.data

    # the crab picks up three cups...
    three = cups[current_idx+1]
    print(f"cups[{current_idx=}+4].head={cups[current_idx+4]}")
    cups[current_idx].head.next = cups[current_idx+4].head
    three.head.getnext().getnext().next = None

    # selections a destination cup
    destination_label = current - 1
    while destination_label in three.nodes():
        # print(f"decreasing destination_label from {destination_label}", end='')
        destination_label = destination_label - 1 if destination_label - 1 > cups.lowest else cups.highest
        # print(f" to {destination_label}")

    destination_idx = cups.find(destination_label)
    print(f"idx: {destination_idx} {destination_label=}")

    # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
    after = cups[destination_idx].head.next
    three.head.getnext().getnext().next = after
    cups[destination_idx].head.next = three.head

    # shift
    new_idx = cups.find(current)
    current_idx = new_idx
    # print(f"need to shift current_idx={current_idx} new_idx={new_idx} by {new_idx - current_idx}")
    # cups = cups.shift(new_idx - current_idx)

    # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    return cups, current_idx + 1


for line in fileinput.input():
    line = line.strip()
    cups = LinkedList(nodes=list(map(int, line)))
    break

print(cups)

current_idx = 0
for i in range(10):
    cups, current_idx = move(cups, current_idx)
    print(cups)
