"""

This module contains printing helper methods for PST.


Example:
    Tree can be printed into console with the following code::

        from priority_search_tree import PrioritySearchTree
        from priority_search_tree.print_helpers import print_tree
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

from . import Node
from . import PrioritySearchSet
from . import PrioritySearchTree


class _Style(Enum):
    WHITE = "\033[37m"
    RED = "\033[31m"
    STRIKETHROUGH_WHITE = "\033[37;9m"
    STRIKETHROUGH_RED = "\033[31;9m"
    RESET = "\033[0m"

    def __str__(self) -> str:
        return str(self.value)


def _repr_node(node: Node) -> str:
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


def repr_tree(tree: PrioritySearchTree, indent_width: int = 4) -> str:
    """Returns string representation of the PST

    Args:
        tree (PrioritySearchTree): PST to be visualised
        indent_width (int): number of spaces for indentation. Default value is ``4``

    Returns:
        str: string PST representation

    """

    def _repr_tree(node, indent, symbol) -> []:
        tmp = []
        if node and node != Node.NULL_NODE:
            tmp.append(f"{symbol}{'─' * indent_width}{_repr_node(node)}")
            tmp.extend(_repr_tree(node.left, f"{indent}│{' ' * indent_width}", f"{indent}├"))
            tmp.extend(_repr_tree(node.right, f"{indent} {' ' * indent_width}", f"{indent}└"))
        return tmp

    result = [f"{_repr_node(tree._root)}"]
    result.extend(_repr_tree(tree._root.left, f"│{' ' * indent_width}", "├"))
    result.extend(_repr_tree(tree._root.right, f" {' ' * indent_width}", "└"))
    return "\n".join(result)


def print_tree(tree: PrioritySearchTree, indent_width=4, file=None, flush=False):
    """Prints string representation of the PST to ``sys.stdout``

    Args:
        tree (PrioritySearchTree): PST to be visualised
        indent_width (int): number of spaces for indentation. Default value is ``4``
        file: a file-like object (stream); defaults to the current ``sys.stdout``.
        flush (bool): whether to forcibly flush the stream. Default value is ``False``

    """
    print(repr_tree(tree, indent_width), file=file, flush=flush)


def repr_set(ps_set: PrioritySearchSet, indent_width: int = 4) -> str:
    """
    Returns string representation of the PSS

    Args:
        ps_set (PrioritySearchSet): PSS to be visualised
        indent_width (int): number of spaces for indentation. Default value is ``4``

    Returns:
        str: string PSS representation

    """
    tree = ps_set._pst
    values = ps_set._values

    if not tree:
        return "[NULL_NODE]"

    def _repr_set(node, indent, symbol) -> []:
        tmp = []
        if node and node != Node.NULL_NODE and node.heap_key[0] != Node.PLACEHOLDER_VALUE:
            tmp.append(f"{symbol}{'─' * indent_width}{values[node.heap_key[1]]!r}")
            if node.right.heap_key[0] == Node.PLACEHOLDER_VALUE:
                tmp.extend(_repr_set(node.left, f"{indent} {' ' * indent_width}", f"{indent}└"))
            else:
                tmp.extend(_repr_set(node.left, f"{indent}│{' ' * indent_width}", f"{indent}├"))
            tmp.extend(_repr_set(node.right, f"{indent} {' ' * indent_width}", f"{indent}└"))
        return tmp

    result = [f"{values[tree._root.heap_key[1]]!r}"]
    if tree._root.right.heap_key[0] == Node.PLACEHOLDER_VALUE:
        result.extend(_repr_set(tree._root.left, f" {' ' * indent_width}", "└"))
    else:
        result.extend(_repr_set(tree._root.left, f"│{' ' * indent_width}", "├"))
    result.extend(_repr_set(tree._root.right, f" {' ' * indent_width}", "└"))
    return "\n".join(result)


def print_set(ps_set: PrioritySearchSet, indent_width=4, file=None, flush=False):
    """Prints string representation of the PSS to ``sys.stdout``

    Args:
        ps_set (PrioritySearchSet): PSS to be visualised
        indent_width (int): number of spaces for indentation. Default value is ``4``
        file: a file-like object (stream); defaults to the current ``sys.stdout``.
        flush (bool): whether to forcibly flush the stream. Default value is ``False``

    """
    print(repr_set(ps_set, indent_width), file=file, flush=flush)
