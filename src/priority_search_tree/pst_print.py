"""

This module contains printing helper methods for PST.


Example:
    Tree can be printed into console with the following code::

        from priority_search_tree import PrioritySearchTree
        from priority_search_tree.pst_print import print_tree
        # create PST
        pst = PrioritySearchTree([(0, 0), (1, 1), (2, 2), (3, 6), (4, 3), (5, 4), (6, 5), (7, 8), (8, 7)])
        # print PST
        print_tree(pst)

    As result next text will be printed into ``sys.stdout``::

        # print result
        (5, 4):(7, 8)
        ├────(3, 6):(3, 6)
        │    ├────(2, 2):(2, 2)
        │    │    ├────(1, 1):(1, 1)
        │    │    │    ├────(0, 0):(0, 0)
        │    │    │    └────(1, 1):[NULL_VALUE]
        │    │    └────(2, 2):[NULL_VALUE]
        │    └────(4, 3):(4, 3)
        │         ├────(3, 6):[NULL_VALUE]
        │         └────(4, 3):[NULL_VALUE]
        └────(7, 8):(8, 7)
             ├────(6, 5):(6, 5)
             │    ├────(5, 4):(5, 4)
             │    └────(6, 5):[NULL_VALUE]
             └────(8, 7):[NULL_VALUE]
                  ├────(7, 8):[NULL_VALUE]
                  └────(8, 7):[NULL_VALUE]

"""

from enum import Enum

from priority_search_tree import Node
from priority_search_tree import PrioritySearchTree


class _Style(Enum):
    WHITE = "\033[37m"
    RED = "\033[31m"
    STRIKETHROUGH_WHITE = "\033[37;9m"
    STRIKETHROUGH_RED = "\033[31;9m"
    RESET = "\033[0m"

    def __str__(self) -> str:
        return str(self.value)


def _node_repr(node: Node) -> str:
    if node.color == 0:
        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            style = _Style.STRIKETHROUGH_WHITE
        else:
            style = _Style.WHITE
    else:
        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            style = _Style.STRIKETHROUGH_RED
        else:
            style = _Style.RED

    if node == Node.NULL_NODE:
        return f"{_Style.WHITE}[NULL_NODE]{_Style.RESET}"
    else:
        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            return f"{style}{node.tree_key}:[NULL_VALUE]{_Style.RESET}"

        else:
            return f"{style}{node.tree_key}:{node.heap_key}{_Style.RESET}"


def tree_repr(tree: PrioritySearchTree, indent_width: int = 4) -> str:
    """
    Returns string representation of the PST

    Args:
        tree (PrioritySearchTree): PST to be visualised
        indent_width (int): number of spaces for indentation. Default value is ``4``

    Returns:
        str: string PST representation

    """

    def _tree_repr(node, indent, symbol) -> []:
        result = []
        if node and node != Node.NULL_NODE:
            result.append(f"{symbol}{'─' * indent_width}{_node_repr(node)}")
            result.extend(_tree_repr(node.left, f"{indent}│{' ' * indent_width}", f"{indent}├"))
            result.extend(_tree_repr(node.right, f"{indent} {' ' * indent_width}", f"{indent}└"))
        return result

    result = [f"{_node_repr(tree._root)}"]
    result.extend(_tree_repr(tree._root.left, f"│{' ' * indent_width}", "├"))
    result.extend(_tree_repr(tree._root.right, f" {' ' * indent_width}", "└"))
    return "\n".join(result)


def print_tree(tree: PrioritySearchTree, indent_width=4, file=None, flush=False):
    """
    prints string representation of the PST to sys.stdout

    Args:
        tree (PrioritySearchTree): PST to be visualised
        indent_width (int): number of spaces for indentation. Default value is ``4``
        file: a file-like object (stream); defaults to the current ``sys.stdout``.
        flush (bool): whether to forcibly flush the stream. Default value is ``False``

    """
    print(tree_repr(tree, indent_width), file=file, flush=flush)
