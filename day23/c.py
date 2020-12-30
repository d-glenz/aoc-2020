import fileinput


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"[{self.data}]"


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        self.node_map = {}
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.node_map[node.data] = node
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                self.node_map[elem] = node.next
                node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)


def main():
    inp = [line.strip() for line in fileinput.input()][0]
    ll = LinkedList(list(inp))
    print(ll)
    print(ll.node_map['3'])


if __name__ == "__main__":
    main()
