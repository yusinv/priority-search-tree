import pytest

from priority_search_tree import PrioritySearchSet
from utils import assert_rb_tree


def test_priority_search_set():
    class Point:
        def __init__(self, x: int, y: int):
            self.x: int = x
            self.y: int = y

    items = [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4), Point(5, 6), Point(6, 6)]

    pss = PrioritySearchSet(key_func=lambda v: v.x, priority_func=lambda v: v.y, iterable=items)
    assert_rb_tree(pss._pst._root)

    assert pss.query(Point(1, 1), Point(2, 2), Point(2, 2)) == [items[1]]
    assert pss.query(Point(1, 1), Point(5, 1), Point(1, 6)) == [items[4]]
    assert pss.sorted_query(Point(1, 1), Point(6, 1), Point(1, 6)) == [items[5], items[4]]
    assert pss.sorted_query(Point(1, 1), Point(4, 1), Point(1, 1), items_limit=1) == [items[3]]

    assert items[2] in pss
    assert Point(10, 10) not in pss
    assert Point(2, 10) in pss

    pss.remove(items[2])
    pss.remove(Point(2, 10))
    pss.discard(Point(4, 1))
    pss.discard(Point(4, 1))

    with pytest.raises(KeyError, match="Key not found:"):
        pss.remove(Point(7, 1))

    with pytest.raises(KeyError, match="Key not found:"):
        pss.remove(Point(7, 7))

    assert_rb_tree(pss._pst._root)

    assert pss.get_with_max_priority().y == 6

    assert pss.pop().y == 6
    assert pss.pop().y == 6
    assert pss.pop().y == 1

    assert not pss

    pss = PrioritySearchSet(key_func=lambda v: v.x, priority_func=lambda v: v.y)
    pss.add(Point(1, 4))
    assert len(pss) == 1
    for p in pss:
        assert p.x == 1
        assert p.y == 4
    pss.clear()
    assert not pss
