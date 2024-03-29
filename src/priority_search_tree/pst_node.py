from typing import Any
from typing import Optional
from typing import TypeVar

_Self = TypeVar("_Self")


class Node:
    __slots__ = ["parent", "left", "right", "color", "heap_value", "tree_value"]

    NULL_NODE: _Self = None
    PLACEHOLDER_VALUE: object = None

    def __init__(self, heap_value: Any, tree_value: Any, color: int = 1) -> None:
        self.parent: Optional[_Self] = None
        self.left: _Self = self.NULL_NODE
        self.right: _Self = self.NULL_NODE
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


Node.PLACEHOLDER_VALUE = object()
Node.NULL_NODE = Node(color=0, tree_value=Node.PLACEHOLDER_VALUE, heap_value=Node.PLACEHOLDER_VALUE)
