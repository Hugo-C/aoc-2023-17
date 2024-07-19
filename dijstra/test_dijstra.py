from hypothesis import given
from hypothesis.strategies import composite, integers, lists

from dijstra.dijkstra import dijkstra, Node


@composite
def bamboo_graph(draw, elements=integers(min_value=0)) -> Node:
    xs = draw(lists(elements, min_size=2))
    prev_node: Node = None
    for i, weigth in enumerate(xs):
        n = Node(name=str(i))
        if prev_node:
            prev_node.add_link(n, weigth)
        prev_node = n
    return n


@given(bamboo_graph())
def test_dijkstra_result_begin_and_end_with_given_parameters(start_node: Node):
    next_node = list(start_node.links.keys())[0]

    node_list = dijkstra(start_node, next_node)

    assert node_list[0] == start_node
    assert node_list[1] == next_node


@given(bamboo_graph())
def test_dijkstra_result_for_a_bamboo_is_simply_the_list_of_nodes(start_node: Node):
    nodes = [start_node]
    node = start_node
    node_found = True
    while node_found:
        node_found = False
        for n in node.links.keys():
            if n not in nodes:
                nodes.append(n)
                node = n
                node_found = True

    node_list = dijkstra(nodes[0], nodes[-1])

    assert node_list == nodes
