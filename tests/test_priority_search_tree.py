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
    assert not pst
    assert 1 not in pst
    result = pst.query(0, 1, 2)
    assert len(result) == 0
    with pytest.raises(ValueError, match="Key not found:"):
        pst.remove(1)
    pst.add(1, 1)
    assert len(pst) == 1
    result = pst.query(0, 2, 0)
    assert len(result) == 1
    assert pst
    assert result[0] == 1
    pst.remove(1)
    assert len(pst) == 0
    result = pst.query(0, 2, 0)
    assert len(result) == 0
    with pytest.raises(IndexError):
        pst.heap_pop()
    pst = PrioritySearchTree([])
    assert len(pst) == 0
    with pytest.raises(IndexError):
        pst.heap_get_max()


def test_heap_pop():
    items = [[1, 0, 2, 3, 6, 5, 4], [1, 0, 6, 2, 3, 5, 4], [4, 6, 5, 0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7, 8]]

    for itm in items:
        pst = PrioritySearchTree()
        for i in itm:
            pst.add(i, i)
            assert_rb_tree(pst._root)

        for i in range(len(itm) - 1, -1, -1):
            assert i == pst.heap_pop()
            assert_rb_tree(pst._root)


def test_heap_get_max():
    pst = PrioritySearchTree([(1, 2), (2, 3), (3, 1)])
    assert pst.heap_get_max() == 2
    pst.add(0, 1)
    assert pst.heap_get_max() == 2
    pst.remove(2)
    assert pst.heap_get_max() == 1
    pst.add(5, 5)
    assert pst.heap_get_max() == 5
    pst.remove(1)
    assert pst.heap_get_max() == 5


def test_contains():
    items = [(1, 1), (2, 2), (3, 4), (4, 4)]
    pst = PrioritySearchTree(items)
    for itm in items:
        assert itm[0] in pst

    assert 5 not in pst


def test_large_pst():
    pst = PrioritySearchTree(LARGE_PST_INITIAL_DATA)
    assert len(pst) == len(LARGE_PST_INITIAL_DATA)
    for itm in LARGE_PST_ADD_DATA:
        pst.add(*itm)
        assert_rb_tree(pst._root)
    assert len(pst) == len(LARGE_PST_INITIAL_DATA) + len(LARGE_PST_ADD_DATA)
    for itm in LARGE_PST_REMOVE_DATA:
        pst.remove(itm)
        assert_rb_tree(pst._root)
    assert len(pst) == len(LARGE_PST_INITIAL_DATA) + len(LARGE_PST_ADD_DATA) - len(LARGE_PST_REMOVE_DATA)
    for itm in LARGE_PST_HEAP_POP_DATA:
        assert itm == pst.heap_pop()
        assert_rb_tree(pst._root)


def test_query():
    items = [(0, 0), (1, 6), (2, 1), (3, 7), (4, 4), (5, 2), (6, 3), (7, 5), (8, 8)]
    pst = PrioritySearchTree(items)
    for x_min in range(10):
        for x_max in range(x_min, 10):
            for y_min in range(10):
                tmp = []
                for item in items:
                    if x_min <= item[0] <= x_max and item[1] >= y_min:
                        tmp.append(item)
                query_expected = [x[0] for x in sorted(tmp, key=lambda x: (x[1], x[0]), reverse=True)]
                assert set(pst.query(x_min, x_max, y_min)) == set(query_expected)
                assert pst.sorted_query(x_min, x_max, y_min) == query_expected


def test_sorted_query_limit():
    items = [(0, 0), (1, 6), (2, 2), (3, 7), (4, 4), (5, 2), (6, 3), (7, 5), (8, 8)]
    pst = PrioritySearchTree(items)
    result = pst.sorted_query(0, 8, 0, items_limit=1)
    assert result == [8]
    result = pst.sorted_query(0, 8, 0, items_limit=2)
    assert result == [8, 3]
    result = pst.sorted_query(0, 8, 0, items_limit=3)
    assert result == [8, 3, 1]
    result = pst.sorted_query(0, 8, 0, items_limit=4)
    assert result == [8, 3, 1, 7]
    result = pst.sorted_query(0, 8, 0, items_limit=5)
    assert result == [8, 3, 1, 7, 4]
    result = pst.sorted_query(0, 8, 0, items_limit=6)
    assert result == [8, 3, 1, 7, 4, 6]
    result = pst.sorted_query(0, 8, 0, items_limit=7)
    assert result == [8, 3, 1, 7, 4, 6, 5]
    result = pst.sorted_query(0, 8, 0, items_limit=8)
    assert result == [8, 3, 1, 7, 4, 6, 5, 2]
    result = pst.sorted_query(0, 8, 0, items_limit=0)
    assert result == [8, 3, 1, 7, 4, 6, 5, 2, 0]


def test_stress_tester():
    stress_test()


def test_unique_tree_key():
    pst = PrioritySearchTree()
    pst.add(1, 1)
    with pytest.raises(ValueError, match="Value with tree_key:"):
        pst.add(1, 2)
    with pytest.raises(ValueError, match="More than one item with tree_key:"):
        PrioritySearchTree([(1, 1), (1, 2)])


def test_not_unique_heap_keys():
    pst = PrioritySearchTree()
    for i in range(100, -1, -1):
        pst.add(i, 5)
    assert_rb_tree(pst._root)
    result = pst.sorted_query(0, 1000, 0)
    assert len(result) == len(pst)
    for i, r in enumerate(reversed(result)):
        assert r == i

    pst.clear()
    for i in range(100):
        pst.add(i, 5)
    assert_rb_tree(pst._root)
    result = pst.sorted_query(0, 1000, 0)
    assert len(result) == len(pst)
    for i, r in enumerate(reversed(result)):
        assert r == i

    pst.clear()
    for itm in [8, 3, 1, 7, 4, 6, 5, 2, 0]:
        pst.add(itm, 5)
    assert_rb_tree(pst._root)
    result = pst.sorted_query(0, 1000, 0)
    assert len(result) == len(pst)
    for i, r in enumerate(reversed(result)):
        assert r == i
