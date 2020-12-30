import fileinput


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"[{self.data}]"


class LinkedList:
    def __init__(self, nodes=None):
        self.head = Node(None)
        self.min, self.max = min(nodes), max(nodes)
        self.node_map = {}
        if nodes is not None:
            self.add_numbers(nodes)

    def add_numbers(self, data):
        node = self.head
        for elem in data:
            node.next = Node(data=elem)
            node = node.next
            self.node_map[elem] = node
        
        # circular
        node.next = self.head.next
        # remove None-head
        self.head = self.head.next

    def next_three(self, node):
        node_after = node.next.next.next.next
        three = node.next
        node.next = node_after
        return three

    def insert_at(self, value, three):
        destination = self.node_map[value]
        node_after = destination.next
        destination.next = three
        three.next.next.next = node_after

    def nodes(self):
        node = self.head
        first = node.data
        nodes = [first]
        node = node.next
        while node.data != first:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return nodes

    def __repr__(self):
        return " -> ".join(map(str, self.nodes()))


def nodes2(current):
    node = current
    first = node.data
    nodes = [first]
    node = node.next
    while node.data != first:
        nodes.append(node.data)
        node = node.next
    return nodes


def play(llist, current):
    three = llist.next_three(current)
    fst, snd, thd = three.data, three.next.data, three.next.next.data
    destination_label = current.data - 1
    while destination_label in [fst, snd, thd, 0]:
        destination_label -= 1
        if destination_label < llist.min:
            destination_label = llist.max
    llist.insert_at(destination_label, three)

def solution2(ll):
    current = ll.head
    for i in range(10000000):
        play(ll, current)
        current = current.next

    current = ll.node_map[1]
    fst = current.next.data
    snd = current.next.next.data
    print(fst * snd)

def solution1(ll):
    current = ll.head
    for i in range(100):
        play(ll, current)
        current = current.next

    current = ll.node_map[1]
    ll2 = LinkedList(nodes2(current.next))
    print(ll2)

def main():
    inp = list(map(int, [line.strip() for line in fileinput.input()][0]))
    ll = LinkedList(inp)
    solution1(ll)
    ll2 = LinkedList(inp + list(range(max(inp)+1, 1000001)))
    solution2(ll2)


if __name__ == "__main__":
    main()
