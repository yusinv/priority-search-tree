import pytest

from data import LARGE_PST_ADD_DATA
from data import LARGE_PST_HEAP_POP_DATA
from data import LARGE_PST_INITIAL_DATA
from data import LARGE_PST_REMOVE_DATA
from priority_search_tree import PrioritySearchTree
from stress import stress_test
from utils import assert_rb_tree


def test_empty_pst():
    pst = PrioritySearchTree()
    result = pst.query((0, 0), (1, 2), (1, 1))
    assert len(result) == 0
    with pytest.raises(ValueError, match="value not found:"):
        pst.remove((1, 1))
    pst.add((1, 1))
    result = pst.query((0, 0), (2, 0), (0, 0))
    assert len(result) == 1
    assert result[0] == (1, 1)
    pst.remove((1, 1))
    result = pst.query((0, 0), (2, 0), (0, 0))
    assert len(result) == 0
    with pytest.raises(IndexError):
        pst.heap_pop()
    with pytest.raises(IndexError):
        pst.heap_get_max()


def test_heap_pop():
    items = [
        [(1, 4), (0, 6), (2, 5), (3, 0), (6, 1), (5, 2), (4, 3)],
        [(1, 4), (0, 6), (6, 5), (2, 0), (3, 1), (5, 2), (4, 3)],
        [(4, 4), (6, 6), (5, 5), (0, 0), (1, 1), (2, 2), (3, 3)],
        [(0, 0), (1, 6), (2, 1), (3, 7), (4, 4), (5, 2), (6, 3), (7, 5), (8, 8)],
        [(0, 0), (1, 1), (2, 2), (3, 6), (4, 3), (5, 4), (6, 5), (7, 8), (8, 7)],
    ]

    for itm in items:
        pst = PrioritySearchTree()
        for i in itm:
            pst.add(i)
            assert_rb_tree(pst._root)

        for i in range(len(itm) - 1, -1, -1):
            assert i == pst.heap_pop()[1]
            assert_rb_tree(pst._root)


def test_heap_get_max():
    pst = PrioritySearchTree([(1, 2), (2, 3), (3, 1)])
    assert pst.heap_get_max() == (2, 3)
    pst.add((0, 1))
    assert pst.heap_get_max() == (2, 3)
    pst.remove((2, 3))
    assert pst.heap_get_max() == (1, 2)
    pst.add((5, 5))
    assert pst.heap_get_max() == (5, 5)
    pst.remove((1, 2))
    assert pst.heap_get_max() == (5, 5)


def test_large_pst():
    pst = PrioritySearchTree(LARGE_PST_INITIAL_DATA)
    for itm in LARGE_PST_ADD_DATA:
        pst.add(itm)
        assert_rb_tree(pst._root)

    for itm in LARGE_PST_REMOVE_DATA:
        pst.remove(itm)
        assert_rb_tree(pst._root)

    for itm in LARGE_PST_HEAP_POP_DATA:
        assert itm == pst.heap_pop()
        assert_rb_tree(pst._root)


def test_query():
    items = [(0, 0), (1, 6), (2, 1), (3, 7), (4, 4), (5, 2), (6, 3), (7, 5), (8, 8)]
    pst = PrioritySearchTree(items)
    for x_min in range(10):
        for x_max in range(x_min, 10):
            for y_min in range(10):
                query_expected = set()
                for item in items:
                    if (x_min, 0) <= item <= (x_max, 8) and item[1:] >= (y_min,):
                        query_expected.add(item)
                assert set(pst.query((x_min, 0), (x_max, 8), (0, y_min))) == query_expected


def test_stress_tester():
    stress_test()
