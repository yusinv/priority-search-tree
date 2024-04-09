from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import MutableSet
from typing import Optional
from typing import TypeVar

from .ps_tree import _KEY
from .ps_tree import _PRIORITY
from .ps_tree import PrioritySearchTree

_V = TypeVar("_V")


class PrioritySearchSet(MutableSet):
    """Mutable Set that maintains priority search tree properties.

    PrioritySearchSet can be used to store any type of objects.
    2 functions should be passed to PrioritySearchSet constructor:

    * ``key_func`` to extract **key** for the object
    * ``priority_func`` to extract **priority** for the object

    extracted **key**, **priority** values will be used in underlying PrioritySearchTree

    Example::

        @dataclass
        class Point:
            x: int
            y: int

        # create new set with Point.x as key and Point.y as priority
        pss = PrioritySearchSet(key_func=lambda p: p.x,
                                priority_func=lambda p: p.y,
                                iterable=[Point(1, 1), Point(2, 2)])
        # add new item to set
        pss.add(Point(3, 3))
        # 3-sided query
        result = pss.query(Point(1, 1), Point(3, 1), Point(2, 2))
        # result = [Point(x=3, y=3), Point(x=2, y=2)]

    Args:
        key_func (Callable): Specifies a function of one argument that is used to extract a comparison **key**
            (for example, ``key_func=lambda p: p.x``).
        priority_func (Callable): Specifies a function of one argument that is used to extract a *priority* value
            (for example, ``priority_func=lambda p: p.y``).
        iterable (Iterable): Initial values to build priority search set. The default value is ``None``.

    Raises:
        KeyError: in case if iterable contains values with not unique **key**

    Complexity:
        `O(N*log(N))` where **N** is number of items to be added to new PSS
    """

    __slots__ = ["_values", "key_func", "priority_func", "_pst"]

    def __init__(
        self, key_func: Callable[[_V], _KEY], priority_func: Callable[[_V], _PRIORITY], iterable: Optional[Iterable[_V]] = None
    ) -> None:

        self.key_func = key_func
        self.priority_func = priority_func
        self._values = {}

        key_priorities = []
        if iterable:
            for item in iterable:
                key = key_func(item)
                priority = priority_func(item)
                self._values[key] = item
                key_priorities.append((key, priority))

        self._pst = PrioritySearchTree(key_priorities)

    def get_with_max_priority(self) -> _KEY:
        """Return the item with the largest **priority** from the PSS.

        Returns:
            item with the largest **priority**

        Raises:
            KeyError: If the PSS is empty

        Complexity:
            Amortized `O(1)`
        """
        return self._values[self._pst.get_with_max_priority()]

    def pop(self) -> _V:
        """Remove and return the item with the largest **priority** from the PSS.

        Returns:
            item with the largest **priority**

        Raises:
            KeyError: If the PSS is empty

        Complexity:
            `O(log(N))` where **N** is number of items in PSS
        """
        return self._values.pop(self._pst.popitem()[0])

    def add(self, value: _V) -> None:
        """Add new item to priority search Set.

        Args:
            value: Value to insert into PSS

        Raises:
            KeyError: in case if value already exists in PSS

        Complexity:
            `O(log(N))` where **N** is number of items in PSS

        Note:
            this function is using ``key_func(value)`` to compare the items
        """
        key = self.key_func(value)
        priority = self.priority_func(value)
        self._pst[key] = priority
        self._values[key] = value

    def remove(self, value: _V) -> None:
        """Remove value from PSS.

        Args:
            value: Value to remove from PSS

        Raises:
            KeyError: in case if value not exists in PSS

        Complexity:
            `O(log(N))` where **N** is number of items in PSS

        Note:
            this function is using ``key_func(value)`` to compare the items
        """
        key = self.key_func(value)
        del self._pst[key]
        del self._values[key]

    def query(self, left: _V, right: _V, bottom: _V) -> list:
        """Performs 3 sided query on PSS.

        This function returns list of items that meet the following criteria:
            1. items have **key** grater or equal to **key** of `left` argument
            2. items have **key** smaller or equal to **key** of `right` argument
            3. items have **priority** grater or equal to **priority** of `bottom` argument

        Args:
            left: Left bound for query (**key** is used to compare).
            right: Right bound for query (**key** is used to compare).
            bottom: Bottom bound for query (**priority** is used to compare).

        Returns:
            List: list of items that satisfy criteria, or empty list if no items found

        Complexity:
            `O(log(N)+K)` where **N** is number of items in PSS and **K** is number of reported items
        """
        key_left = self.key_func(left)
        key_right = self.key_func(right)
        priority_bottom = self.priority_func(bottom)
        return [self._values[x] for x in self._pst.query(key_left, key_right, priority_bottom)]

    def sorted_query(self, left: _V, right: _V, bottom: _V, items_limit: int = 0) -> list:
        """Performs sorted 3 sided query on PSS.

        This function returns list of items that meet the following criteria:
            1. items have **key** grater or equal to **key** of `left` argument
            2. items have **key** smaller or equal to **key** of `right` argument
            3. items have **priority** grater or equal to **priority** of `bottom` argument

        Args:
            left: Left bound for query (**key** is used).
            right: Right bound for query (**key** is used).
            bottom: Bottom bound for query (**priority** is used).
            items_limit (int): Number of items to return. Default value is ``0`` - no limit.

        Returns:
            List: list of items that satisfy criteria and sorted by **priority**
            (in case of limit, items with largest **priority** will be returned), or empty list if no items found.

        Complexity:
            `O(log(N)+K*log(K))` where **N** is number of items in PSS and **K** is number of returned items
        """
        key_left = self.key_func(left)
        key_right = self.key_func(right)
        priority_bottom = self.priority_func(bottom)
        return [self._values[x] for x in self._pst.sorted_query(key_left, key_right, priority_bottom, items_limit)]

    def __len__(self) -> int:
        """Implements the built-in function len()

        Returns:
            int: Number of items in PSS.

        Complexity:
            `O(1)`
        """
        return len(self._pst)

    def __contains__(self, value: _V) -> bool:
        """Membership test operator

        Args:
            value: Value to test for membership

        Returns:
            bool:  ``True`` if value is in ``self``, ``False`` otherwise.

        Complexity:
            `O(log(N))` where **N** is number of items in PSS

        Note:
            this function is using ``key_func(value)`` to compare the items
        """
        return self.key_func(value) in self._values

    def clear(self) -> None:
        """Removes **all** items from priority search set.

        Complexity:
            `O(1)`
        """
        self._pst.clear()
        self._values.clear()

    def discard(self, value) -> None:
        """Remove value from PSS if it exists.

        Args:
            value: Value to remove from PSS

        Complexity:
            `O(log(N))` where **N** is number of items in PSS

        Note:
            this function is using ``key_func(value)`` to compare the items
        """
        key = self.key_func(value)
        if key in self._values:
            del self._pst[key]
            del self._values[key]

    def __iter__(self) -> Iterator:
        """Create an iterator that iterates values in sorted by **key** order

        Returns:
            Iterator: in order iterator
        """
        for key in self._pst:
            yield self._values[key]
