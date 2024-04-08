import pytest

from priority_search_tree import PrioritySearchSet
from utils import assert_rb_tree


def test_priority_search_set():
    class Point:
        def __init__(self, x: int, y: int):
            self.x: int = x
            self.y: int = y

    items = [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4), Point(5, 6), Point(6, 6)]

    pst = PrioritySearchSet(key_func=lambda v: v.x, priority_func=lambda v: v.y, iterable=items)
    assert_rb_tree(pst._pst._root)

    assert pst.query(Point(1, 1), Point(2, 2), Point(2, 2)) == [items[1]]
    assert pst.query(Point(1, 1), Point(5, 1), Point(1, 6)) == [items[4]]
    assert pst.sorted_query(Point(1, 1), Point(6, 1), Point(1, 6)) == [items[5], items[4]]
    assert pst.sorted_query(Point(1, 1), Point(4, 1), Point(1, 1), items_limit=1) == [items[3]]

    assert items[2] in pst
    assert Point(10, 10) not in pst
    assert Point(2, 10) in pst

    pst.remove(items[2])
    pst.remove(Point(2, 10))
    pst.discard(Point(4, 1))
    pst.discard(Point(4, 1))

    with pytest.raises(KeyError, match="Key not found:"):
        pst.remove(Point(7, 1))

    with pytest.raises(KeyError, match="Key not found:"):
        pst.remove(Point(7, 7))

    assert_rb_tree(pst._pst._root)

    assert pst.get_with_max_priority().y == 6

    assert pst.pop().y == 6
    assert pst.pop().y == 6
    assert pst.pop().y == 1

    assert not pst

    pst = PrioritySearchSet(key_func=lambda v: v.x, priority_func=lambda v: v.y)
    pst.add(Point(1, 1))
    assert len(pst) == 1
    pst.clear()
    assert not pst
