from typing import Any
from typing import Optional
from typing import TypeVar

_Self = TypeVar("_Self")


class Node:
    NULL_NODE: _Self = None

    def __init__(self, heap_value: Any = None, tree_value: Any = None, placeholder: bool = False, color: int = 1) -> None:
        self.parent: Optional[_Self] = None
        self.left: _Self = self.NULL_NODE
        self.right: _Self = self.NULL_NODE
        self.placeholder: bool = placeholder
        self.color: int = color
        self.heap_value: Any = heap_value
        self.tree_value: Any = tree_value

    def set_left(self, left_node: _Self) -> None:
        if left_node and left_node != self.NULL_NODE:
            left_node.parent = self
        self.left = left_node

    def set_right(self, right_node: _Self) -> None:
        if right_node and right_node != self.NULL_NODE:
            right_node.parent = self
        self.right = right_node


if Node.NULL_NODE is None:
    Node.NULL_NODE = Node(color=0, placeholder=True)
