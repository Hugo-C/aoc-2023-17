from typing import Self

"""Warning, worst Dijkstra implementation ever written, this was just a warmup"""

class Node:
    """Node of a non oriented graph"""

    def __init__(self, name: str):
        self.name = name
        self.links = dict()

    def add_link(self, node: Self, weight: int, reverse=False):
        self.links[node] = weight
        if not reverse:
            node.add_link(self, weight, reverse=True)

    def __repr__(self):
        return f"Node {self.name}-#{len(self.links)}{[(node.name, weight) for (node, weight) in self.links.items()]}"


def get_closest_node(distances, nodes_done) -> Node:
    min_weight = None
    closest_node = None
    for (node_1, node_2), weight in distances.items():
        # The 2 nodes cannot be both outside of nodes_done
        if node_1 not in nodes_done and (min_weight is None or weight < min_weight):
            min_weight = weight
            closest_node = node_1
        if node_2 not in nodes_done and (min_weight is None or weight < min_weight):
            min_weight = weight
            closest_node = node_2
    return closest_node


def build_result(distances, start_node: Node, end_node: Node) -> list[Node]:
    current_node = end_node
    path = [current_node]
    while current_node != start_node:
        min_weight = None
        closest_node = None
        for (node_1, node_2), weight in distances.items():
            if node_2 == current_node and node_1 not in path and (min_weight is None or weight < min_weight):
                min_weight = weight
                closest_node = node_1
        current_node = closest_node
        path.append(current_node)
    return list(reversed(path))


def dijkstra(start: Node, end: Node) -> list[Node]:
    distances = {}  # key: Node 1 to Node 2 (tuple), value: weight (int)
    nodes_done = set()
    current_node = start
    while end not in nodes_done:
        for linked_node, weight in current_node.links.items():
            existing_weight = distances.get((current_node, linked_node))
            if not existing_weight or existing_weight > weight:
                distances[(current_node, linked_node)] = weight
        nodes_done.add(current_node)
        current_node = get_closest_node(distances, nodes_done)

    return build_result(distances, start, end)


if __name__ == '__main__':
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    e = Node("e")
    f = Node("f")
    g = Node("g")
    h = Node("h")
    i = Node("i")
    j = Node("j")

    a.add_link(b, 85)
    b.add_link(f, 80)
    f.add_link(i, 250)
    i.add_link(j, 84)
    a.add_link(c, 217)
    c.add_link(g, 186)
    c.add_link(h, 103)
    h.add_link(d, 183)
    h.add_link(j, 167)
    a.add_link(e, 173)
    e.add_link(j, 502)

    result = dijkstra(a, j)
    print(f"path={[node.name for node in result]}")
    length = 0
    for i in range(1, len(result)):
        start = result[i-1]
        end = result[i]
        length += start.links[end]

    print(f"{length=}")
