import fileinput
from typing import List, Optional, Dict


class Node:
    def __init__(self, data: Optional[int]) -> None:
        self.data = data
        self._next: Optional['Node'] = None

    @property
    def next(self) -> 'Node':
        if self._next is None:
            raise ValueError('No next. Since the LinkedList is circular, this should never occur.')
        return self._next

    @next.setter
    def next(self, next: 'Node') -> None:
        self._next = next

    @property
    def value(self) -> int:
        if self.data is None:
            raise ValueError('Node value should not be None')
        return self.data

    def __repr__(self) -> str:
        return f"[{self.data}]"


class LinkedList:
    def __init__(self, nodes: Optional[List[int]] = None) -> None:
        self.head = Node(None)
        if nodes is not None:
            self.min, self.max = min(nodes), max(nodes)
            self.node_map: Dict[int, Node] = {}
            self.add_numbers(nodes)

    def add_numbers(self, data: List[int]) -> None:
        node = self.head
        for elem in data:
            node.next = Node(data=elem)
            node = node.next
            self.node_map[elem] = node

        # circular
        node.next = self.head.next
        # remove None-head
        self.head = self.head.next

    def next_three(self, node: Node) -> Node:
        node_after = node.next.next.next.next
        three = node.next
        node.next = node_after
        return three

    def insert_at(self, value: int, three: Node) -> None:
        destination = self.node_map[value]
        node_after = destination.next
        destination.next = three
        three.next.next.next = node_after

    def __repr__(self) -> str:
        return " -> ".join(map(str, nodes(self.head)))


def nodes(current: Node) -> List[int]:
    node = current
    first = node.data
    if first is None:
        raise ValueError('Valid node cannot have None data')
    nodes = [first]
    node = node.next
    while node.data != first:
        if node.data is None:
            raise ValueError('Valid node cannot have None data')
        nodes.append(node.data)
        node = node.next
    return nodes


def play(llist: LinkedList, current: Node) -> None:
    three = llist.next_three(current)
    fst, snd, thd = three.data, three.next.data, three.next.next.data
    destination_label = current.value - 1
    while destination_label in [fst, snd, thd, 0]:
        destination_label -= 1
        if destination_label < llist.min:
            destination_label = llist.max
    llist.insert_at(destination_label, three)

def solution2(ll: LinkedList) -> int:
    current = ll.head
    for i in range(10000000):
        play(ll, current)
        current = current.next

    current = ll.node_map[1]
    fst = current.next.value
    snd = current.next.next.value
    return fst * snd

def solution1(ll: LinkedList) -> str:
    current = ll.head
    for i in range(100):
        play(ll, current)
        current = current.next

    current = ll.node_map[1]
    ll2 = LinkedList(nodes(current.next))
    return ''.join(map(str, nodes(ll2.head)[:-1]))

def main() -> None:
    inp = list(map(int, [line.strip() for line in fileinput.input()][0]))
    ll = LinkedList(inp)
    print(f"Solution 1: {solution1(ll)}")
    ll2 = LinkedList(inp + list(range(max(inp)+1, 1000001)))
    print(f"Solution 2: {solution2(ll2)}")


if __name__ == "__main__":
    main()
