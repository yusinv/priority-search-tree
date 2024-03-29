from priority_search_tree import PrioritySearchTree
from priority_search_tree.pst_print import print_tree
from priority_search_tree.pst_print import tree_repr


def test_tree_representation():
    result = (
        "\x1b[37m5:(8, 7)\x1b[0m\n"
        "├────\x1b[37m3:(6, 3)\x1b[0m\n"
        "│    ├────\x1b[37m2:(2, 2)\x1b[0m\n"
        "│    │    ├────\x1b[37m1:(1, 1)\x1b[0m\n"
        "│    │    │    ├────\x1b[31m0:(0, 0)\x1b[0m\n"
        "│    │    │    └────\x1b[31;9m1:[NULL_VALUE]\x1b[0m\n"
        "│    │    └────\x1b[37;9m2:[NULL_VALUE]\x1b[0m\n"
        "│    └────\x1b[37m4:(3, 4)\x1b[0m\n"
        "│         ├────\x1b[37;9m3:[NULL_VALUE]\x1b[0m\n"
        "│         └────\x1b[37;9m4:[NULL_VALUE]\x1b[0m\n"
        "└────\x1b[37m7:(7, 8)\x1b[0m\n"
        "     ├────\x1b[37m6:(5, 6)\x1b[0m\n"
        "     │    ├────\x1b[37m5:(4, 5)\x1b[0m\n"
        "     │    └────\x1b[37;9m6:[NULL_VALUE]\x1b[0m\n"
        "     └────\x1b[37;9m8:[NULL_VALUE]\x1b[0m\n"
        "          ├────\x1b[37;9m7:[NULL_VALUE]\x1b[0m\n"
        "          └────\x1b[37;9m8:[NULL_VALUE]\x1b[0m"
    )
    pst = PrioritySearchTree([(0, 0), (1, 1), (2, 2), (3, 6), (4, 3), (5, 4), (6, 5), (7, 8), (8, 7)])
    assert result == tree_repr(pst)
    print_tree(pst)


def test_print_tree(capsys):
    pst = PrioritySearchTree()
    print_tree(pst)
    assert capsys.readouterr()[0].startswith("\x1b[37m[NULL_NODE]\x1b[0m")
