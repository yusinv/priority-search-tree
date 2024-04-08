from typing import Any
from typing import Optional
from typing import Tuple
from typing import TypeVar

_Self = TypeVar("_Self")


class Node:
    __slots__ = ["parent", "left", "right", "color", "heap_key", "tree_key"]

    NULL_NODE: _Self = None
    PLACEHOLDER_VALUE: object = None

    def __init__(self, tree_key: Any, heap_key: Tuple[Any, Any], color: int = 1) -> None:
        self.parent: Optional[_Self] = None
        self.left: _Self = self.NULL_NODE
        self.right: _Self = self.NULL_NODE
        self.color: int = color
        self.tree_key: Any = tree_key
        self.heap_key: Tuple[Any, Any] = heap_key

    def set_left(self, left_node: _Self) -> None:
        if left_node and left_node != self.NULL_NODE:
            left_node.parent = self
        self.left = left_node

    def set_right(self, right_node: _Self) -> None:
        if right_node and right_node != self.NULL_NODE:
            right_node.parent = self
        self.right = right_node


Node.PLACEHOLDER_VALUE = object()
Node.NULL_NODE = Node(tree_key=Node.PLACEHOLDER_VALUE, heap_key=(Node.PLACEHOLDER_VALUE, Node.PLACEHOLDER_VALUE), color=0)
