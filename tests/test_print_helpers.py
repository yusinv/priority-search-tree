from dataclasses import dataclass

from priority_search_tree import PrioritySearchSet
from priority_search_tree import PrioritySearchTree
from priority_search_tree.print_helpers import print_set
from priority_search_tree.print_helpers import print_tree
from priority_search_tree.print_helpers import repr_set
from priority_search_tree.print_helpers import repr_tree


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
    assert result == repr_tree(pst)
    print_tree(pst)


def test_set_representation():
    result = (
        "Point(x=7, y=8)\n"
        "├────Point(x=3, y=6)\n"
        "│    ├────Point(x=2, y=2)\n"
        "│    │    └────Point(x=1, y=1)\n"
        "│    │         └────Point(x=0, y=0)\n"
        "│    └────Point(x=4, y=3)\n"
        "└────Point(x=8, y=7)\n"
        "     └────Point(x=6, y=5)\n"
        "          └────Point(x=5, y=4)"
    )

    @dataclass
    class Point:
        x: int
        y: int

        def __repr__(self):
            return f"Point(x={self.x}, y={self.y})"

    pss = PrioritySearchSet(
        key_func=lambda p: p.x,
        priority_func=lambda p: p.y,
        iterable=[Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 6), Point(4, 3), Point(5, 4), Point(6, 5), Point(7, 8), Point(8, 7)],
    )
    assert result == repr_set(pss)
    print_set(pss)


def test_print_tree(capsys):
    pst = PrioritySearchTree()
    print_tree(pst)
    assert capsys.readouterr()[0].startswith("\x1b[37m[NULL_NODE]\x1b[0m")


def test_print_set(capsys):
    @dataclass
    class Point:
        x: int
        y: int

        def __repr__(self):
            return f"Point(x={self.x}, y={self.y})"

    pss = PrioritySearchSet(key_func=lambda p: p.x, priority_func=lambda p: p.y)
    print_set(pss)
    assert capsys.readouterr()[0].startswith("[NULL_NODE]")
    pss.add(Point(3, 3))
    pss.add(Point(1, 1))
    pss.add(Point(2, 2))
    print_set(pss)
