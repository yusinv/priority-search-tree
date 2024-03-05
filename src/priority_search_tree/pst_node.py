class Node:
    NULL_NODE = None

    def __init__(self, heap_value=None, tree_value=None, placeholder=False, color=1):
        self.parent = None
        self.left = self.NULL_NODE
        self.right = self.NULL_NODE
        self.placeholder = placeholder
        self.color = color
        self.heap_value = heap_value
        self.tree_value = tree_value

    def set_left(self, left_node):
        if left_node and left_node != self.NULL_NODE:
            left_node.parent = self
        self.left = left_node

    def set_right(self, right_node):
        if right_node and right_node != self.NULL_NODE:
            right_node.parent = self
        self.right = right_node


if Node.NULL_NODE is None:
    Node.NULL_NODE = Node(color=0, placeholder=True)
