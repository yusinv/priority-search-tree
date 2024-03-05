from priority_search_tree import PrioritySearchTree
from priority_search_tree.pst_print import tree_repr


def test_tree_representation():
    result = (
        "\x1b[37m(5, 4):(7, 8)\x1b[0m\n"
        "├────\x1b[37m(3, 6):(3, 6)\x1b[0m\n"
        "│    ├────\x1b[37m(2, 2):(2, 2)\x1b[0m\n"
        "│    │    ├────\x1b[37m(1, 1):(1, 1)\x1b[0m\n"
        "│    │    │    ├────\x1b[31m(0, 0):(0, 0)\x1b[0m\n"
        "│    │    │    └────\x1b[31;9m(1, 1):(1, 1)\x1b[0m\n"
        "│    │    └────\x1b[37;9m(2, 2):(2, 2)\x1b[0m\n"
        "│    └────\x1b[37m(4, 3):(4, 3)\x1b[0m\n"
        "│         ├────\x1b[37;9m(3, 6):(3, 6)\x1b[0m\n"
        "│         └────\x1b[37;9m(4, 3):(4, 3)\x1b[0m\n"
        "└────\x1b[37m(7, 8):(8, 7)\x1b[0m\n"
        "     ├────\x1b[37m(6, 5):(6, 5)\x1b[0m\n"
        "     │    ├────\x1b[37m(5, 4):(5, 4)\x1b[0m\n"
        "     │    └────\x1b[37;9m(6, 5):(6, 5)\x1b[0m\n"
        "     └────\x1b[37m(8, 7):None\x1b[0m\n"
        "          ├────\x1b[37;9m(7, 8):(7, 8)\x1b[0m\n"
        "          └────\x1b[37;9m(8, 7):(8, 7)\x1b[0m"
    )
    pst = PrioritySearchTree([(0, 0), (1, 1), (2, 2), (3, 6), (4, 3), (5, 4), (6, 5), (7, 8), (8, 7)])
    assert result == tree_repr(pst)
