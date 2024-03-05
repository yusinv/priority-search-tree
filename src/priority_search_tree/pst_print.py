from enum import Enum

from priority_search_tree import Node
from priority_search_tree import PrioritySearchTree


class _Style(Enum):
    WHITE = "\033[37m"
    RED = "\033[31m"
    STRIKETHROUGH_WHITE = "\033[37;9m"
    STRIKETHROUGH_RED = "\033[31;9m"
    RESET = "\033[0m"

    def __str__(self):
        return str(self.value)


def node_repr(node: Node) -> str:
    if node.color == 0:
        if node.placeholder:
            style = _Style.STRIKETHROUGH_WHITE
        else:
            style = _Style.WHITE
    else:
        if node.placeholder:
            style = _Style.STRIKETHROUGH_RED
        else:
            style = _Style.RED

    if node == Node.NULL_NODE:
        return f"{_Style.WHITE}[NULL_NODE]{_Style.RESET}"
    else:
        return f"{style}{node.tree_value}:{node.heap_value}{_Style.RESET}"


def tree_repr(tree: PrioritySearchTree, indent_width=4) -> str:
    def _tree_repr(node, indent, symbol) -> []:
        result = []
        if node and node != Node.NULL_NODE:
            result.append(f"{symbol}{'─' * indent_width}{node_repr(node)}")
            result.extend(_tree_repr(node.left, f"{indent}│{' ' * indent_width}", f"{indent}├"))
            result.extend(_tree_repr(node.right, f"{indent} {' ' * indent_width}", f"{indent}└"))
        return result

    result = [f"{node_repr(tree._root)}"]
    result.extend(_tree_repr(tree._root.left, f"│{' ' * indent_width}", "├"))
    result.extend(_tree_repr(tree._root.right, f" {' ' * indent_width}", "└"))
    return "\n".join(result)


def print_tree(tree: PrioritySearchTree):
    print(tree_repr(tree))
