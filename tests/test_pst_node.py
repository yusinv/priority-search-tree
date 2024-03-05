from priority_search_tree import Node


def test_node_init():
    node = Node(1, 2, False)
    assert node.heap_value == 1
    assert node.tree_value == 2
    assert node.placeholder is False
    assert node.color == 1


def test_node_set_left():
    p_node: Node = Node(1, 1)
    c_node: Node = Node(2, 2)
    p_node.set_left(c_node)
    assert p_node.left == c_node
    assert c_node.parent == p_node
    p_node.set_left(Node.NULL_NODE)
    assert p_node.left == Node.NULL_NODE


def test_node_set_right():
    p_node: Node = Node(1, 1)
    c_node: Node = Node(2, 2)
    p_node.set_right(c_node)
    assert p_node.right == c_node
    assert c_node.parent == p_node
    p_node.set_right(Node.NULL_NODE)
    assert p_node.right == Node.NULL_NODE
