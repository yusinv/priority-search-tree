__version__ = "0.0.2"

from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import TypeVar

from .pst_node import Node

_KEY = TypeVar("_KEY")
_PRIORITY = TypeVar("_PRIORITY")
_SupportsRichComparisonT = TypeVar("_SupportsRichComparisonT")


class PrioritySearchTree:
    """
    Class that represents Priority search tree.

    Example::

        # create new tree
        pst = PrioritySearchTree([(1,1),(2,2)])
        # add item to the tree
        pst.add((3,3))
        # perform 3 sided query
        result = pst.query((0,0),(4,0),(0,2))

    Args:
        iterable (Iterable): Initial values to build priority search tree. The default value is ``None``.
        tree_key (Callable): Specifies a function of one argument that is used to extract a *tree* comparison key
            from each element (for example, ``tree_key=str.lower``). The default value is ``tree_key=lambda x: x``
        heap_key (Callable): Specifies a function of one argument that is used to extract a *heap* comparison key
            from each element (for example, ``tree_key=str.lower``). The default value is ``tree_key=lambda x: x[1:]``

    Raises:
        ValueError: in case if iterable contains values with not unique tree_key

    Complexity:
        O(N*log(N)) where **N** is number of items to be added to new PST
    """

    __slots__ = ["_root", "_len"]

    def _push_down(self, node: Node, heap_key: Tuple[_PRIORITY, _KEY]) -> None:

        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            node.heap_key = heap_key
            return

        if node.heap_key[1] < node.tree_key:
            self._push_down(node.left, node.heap_key)
        else:
            self._push_down(node.right, node.heap_key)

        node.heap_key = heap_key

    def _sieve_down(self, node: Node, heap_key: Tuple[_PRIORITY, _KEY]) -> None:

        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            node.heap_key = heap_key
            return

        if heap_key > node.heap_key:
            self._push_down(node, heap_key)
            return

        if heap_key[1] < node.tree_key:
            self._sieve_down(node.left, heap_key)
        else:
            self._sieve_down(node.right, heap_key)

    def _push_up(self, node: Node) -> None:
        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            return

        if node.left.heap_key[0] == Node.PLACEHOLDER_VALUE:
            node.heap_key = node.right.heap_key
            self._push_up(node.right)
            return

        if node.right.heap_key[0] == Node.PLACEHOLDER_VALUE:
            node.heap_key = node.left.heap_key
            self._push_up(node.left)
            return

        if node.left.heap_key >= node.right.heap_key:
            node.heap_key = node.left.heap_key
            self._push_up(node.left)
        else:
            node.heap_key = node.right.heap_key
            self._push_up(node.right)

    def __init__(self, iterable: Optional[Iterable[Tuple[_KEY, _PRIORITY]]] = None) -> None:
        self._root: Node = Node.NULL_NODE
        self._len: int = 0

        if iterable:
            sn = sorted(iterable)
            current_key = sn[0]
            for next_key in sn[1:]:
                if current_key[0] == next_key[0]:
                    raise ValueError(f"More than one item with tree_key:{current_key[0]}")
                current_key = next_key

            sn_len = len(sn)
            sn_iter = iter(sn)
            tree_nodes = []
            lvl = sn_len.bit_length()
            for _ in range(sn_len - 2 ** (lvl - 1)):
                keys = next(sn_iter)
                ln = Node(tree_key=keys[0], heap_key=(keys[1], keys[0]))
                keys = next(sn_iter)
                rn = Node(tree_key=keys[0], heap_key=(keys[1], keys[0]))
                pn = Node(tree_key=rn.tree_key, heap_key=(keys[1], keys[0]), color=0)
                pn.set_left(ln)
                pn.set_right(rn)
                self._push_up(pn)
                tree_nodes.append((pn, ln.tree_key, rn.tree_key))

            for keys in sn_iter:
                pn = Node(tree_key=keys[0], heap_key=(keys[1], keys[0]), color=0)
                tree_nodes.append((pn, pn.tree_key, pn.tree_key))

            while len(tree_nodes) > 1:
                new_nodes = []
                for i in range(0, len(tree_nodes), 2):
                    ln, ln_min, ln_max = tree_nodes[i]
                    rn, rn_min, rn_max = tree_nodes[i + 1]
                    pn = Node(tree_key=rn_min, heap_key=ln.heap_key, color=0)
                    pn.set_left(ln)
                    pn.set_right(rn)
                    self._push_up(pn)
                    new_nodes.append((pn, ln_min, rn_max))
                tree_nodes = new_nodes

            self._root = tree_nodes[0][0]
            self._len = sn_len

    def heap_get_max(self) -> _KEY:
        """
        Return the item with the largest **heap_key** from the PST.

        Returns:
            item with the largest **heap_key**

        Raises:
            IndexError: If the PST is empty

        Complexity:
            O(1)
        """
        if self._root == Node.NULL_NODE:
            raise IndexError
        return self._root.heap_key[1]

    def heap_pop(self) -> _KEY:
        """
        Remove and return the item with the largest **heap_key** from the PST.

        Returns:
            item with the largest **heap_key**

        Raises:
            IndexError: If the PST is empty

        Complexity:
            O(log(N)) where **N** is number of items in PST
        """
        if self._root == Node.NULL_NODE:
            raise IndexError
        result = self._root.heap_key[1]
        self.remove(result)
        return result

    def add(self, key: _KEY, priority: _PRIORITY) -> None:
        """
        Add new item to PST.

        Args:
            value: Value to insert into PST

        Raises:
            ValueError: in case if value with **tree_key** already exists in PST

        Complexity:
            O(log(N)) where **N** is number of items in PST
        """
        if self._root == Node.NULL_NODE:
            self._root = Node(tree_key=key, heap_key=(priority, key), color=0)
            self._len = 1
            return

        prev = None
        node = self._root
        while node != Node.NULL_NODE:
            prev = node
            if key < node.tree_key:
                node = node.left
            elif key == node.tree_key:
                raise ValueError(f"Value with tree_key:{key} already in tree")
            else:
                node = node.right

        new_placeholder = Node(tree_key=key, heap_key=(Node.PLACEHOLDER_VALUE, Node.PLACEHOLDER_VALUE))
        prev_placeholder = Node(tree_key=prev.tree_key, heap_key=(Node.PLACEHOLDER_VALUE, Node.PLACEHOLDER_VALUE))

        if key < prev.tree_key:
            prev.set_right(prev_placeholder)
            prev.set_left(new_placeholder)
        else:
            prev.tree_key = key
            prev.set_right(new_placeholder)
            prev.set_left(prev_placeholder)

        self._sieve_down(self._root, (priority, key))
        self._fix_insert(new_placeholder)
        self._len += 1

    def remove(self, key: _KEY) -> None:
        """
        Remove item from PST.

        Args:
            value: Value to remove from PST

        Raises:
            ValueError: in case if value not exists in PST

        Complexity:
            O(log(N)) where **N** is number of items in PST

        Note:
            this function is using ``tree_key(value)`` to compare the items
        """
        tree_node = None
        node = self._root
        while node != Node.NULL_NODE:
            if key == node.tree_key:
                tree_node = node
                break
            elif key < node.tree_key:
                node = node.left
            else:
                node = node.right

        if tree_node is None:
            raise ValueError(f"Key not found:{key}")

        leaf_node = None
        node = tree_node
        while node != Node.NULL_NODE:
            leaf_node = node
            if key < node.tree_key:
                node = node.left
            else:
                node = node.right

        if leaf_node == self._root:
            self._root = Node.NULL_NODE
            self._len = 0
            return

        # remove heap value
        node = leaf_node
        while node.heap_key[1] != key:
            node = node.parent
        self._push_up(node)

        if tree_node.left == Node.NULL_NODE:  # left node
            cut_node = tree_node.parent
            fix_node = tree_node.parent.right
        elif tree_node.right == leaf_node:  # leaf children
            cut_node = tree_node
            fix_node = tree_node.left
        else:  # subtree case
            tree_node.tree_key = leaf_node.parent.tree_key
            cut_node = leaf_node.parent
            fix_node = leaf_node.parent.right

        self._push_down(cut_node, cut_node.heap_key)
        self._transplant(cut_node, fix_node)

        if cut_node.color == 0:
            self._fix_delete(fix_node)

        self._len -= 1

    def _fix_delete(self, node: Node) -> None:
        while node != self._root and node.color == 0:
            if node == node.parent.left:
                s_node = node.parent.right
                if s_node.color == 1:
                    s_node.color = 0
                    node.parent.color = 1
                    self._rotate_left(node.parent)
                    s_node = node.parent.right

                if s_node.left.color == 0 and s_node.right.color == 0:
                    s_node.color = 1
                    node = node.parent
                else:
                    if s_node.right.color == 0:
                        s_node.left.color = 0
                        s_node.color = 1
                        self._rotate_right(s_node)
                        s_node = node.parent.right

                    s_node.color = node.parent.color
                    node.parent.color = 0
                    s_node.right.color = 0
                    self._rotate_left(node.parent)
                    node = self._root
            else:
                s_node = node.parent.left
                if s_node.color == 1:
                    s_node.color = 0
                    node.parent.color = 1
                    self._rotate_right(node.parent)
                    s_node = node.parent.left

                if s_node.right.color == 0 and s_node.left.color == 0:
                    s_node.color = 1
                    node = node.parent
                else:
                    if s_node.left.color == 0:
                        s_node.right.color = 0
                        s_node.color = 1
                        self._rotate_left(s_node)
                        s_node = node.parent.left

                    s_node.color = node.parent.color
                    node.parent.color = 0
                    s_node.left.color = 0
                    self._rotate_right(node.parent)
                    node = self._root
        node.color = 0

    def _transplant(self, u: Node, v: Node) -> None:
        if u.parent is None:
            self._root = v
            self._root.parent = None
        elif u == u.parent.left:
            u.parent.set_left(v)
        else:
            u.parent.set_right(v)

    def query(self, key_left: _KEY, key_right: _KEY, priority_bottom: _PRIORITY) -> list[_KEY]:
        """Performs 3 sided query on PST.

        This function returns list of items that meet the following criteria:
            1. items have **tree_key** grater or equal to **tree_key** of tree_left argument
            2. items have **tree_key** smaller or equal to **tree_key** of tree_right argument
            3. items have **heap_key** grater or equal to **heap_key** of heap_bottom argument

        Args:
            tree_left: Left bound for query (**tree_key** is used).
            tree_right: Right bound for query (**tree_key** is used).
            heap_bottom: Bottom bound for query (**heap_key** is used).

        Returns:
            List: list of items that satisfy criteria, or empty list if no items found

        Complexity:
            O(log(N)+K) where **N** is number of items in PST and **K** is number of reported items
        """
        result = []

        def _query_node(node):
            if node == Node.NULL_NODE or node.heap_key[0] == Node.PLACEHOLDER_VALUE:
                return

            if node.heap_key[0] >= priority_bottom:
                if key_left <= node.heap_key[1] <= key_right:
                    result.append(node.heap_key[1])
            else:
                return

            if key_right < node.tree_key:
                _query_node(node.left)
            elif key_left >= node.tree_key:
                _query_node(node.right)
            else:
                _query_node(node.left)
                _query_node(node.right)

        _query_node(self._root)
        return result

    def sorted_query(self, key_left: _KEY, key_right: _KEY, priority_bottom: _PRIORITY, items_limit: int = 0) -> [_KEY]:
        """Performs 3 sided query on PST.

        This function returns list of items that meet the following criteria:
            1. items have **tree_key** grater or equal to **tree_key** of tree_left argument
            2. items have **tree_key** smaller or equal to **tree_key** of tree_right argument
            3. items have **heap_key** grater or equal to **heap_key** of heap_bottom argument

        Args:
            tree_left: Left bound for query (**tree_key** is used).
            tree_right: Right bound for query (**tree_key** is used).
            heap_bottom: Bottom bound for query (**heap_key** is used).
            items_limit (int): Number of items to return. Default value is ``0`` - no limit.

        Returns:
            List: list of items that satisfy criteria and sorted by **heap_key**
            (in case of limit, items with largest **heap_key** will be returned), or empty list if no items found

        Complexity:
            O(log(N)+K*log(K)) where **N** is number of items in PST and **K** is number of returned items
        """
        if items_limit <= 0:
            items_limit = self._len

        def _sorted_query_node(node, limit):
            result = []
            if node == Node.NULL_NODE or node.heap_key[0] == Node.PLACEHOLDER_VALUE or limit == 0:
                return result

            if node.heap_key[0] >= priority_bottom:
                if key_left <= node.heap_key[1] <= key_right:
                    result.append(node.heap_key)
                    limit -= 1
            else:
                return result

            if key_right < node.tree_key:
                result.extend(_sorted_query_node(node.left, limit))
            elif key_left >= node.tree_key:
                result.extend(_sorted_query_node(node.right, limit))
            else:
                left = _sorted_query_node(node.left, limit)
                right = _sorted_query_node(node.right, limit)
                # merge
                i, j = 0, 0
                while i < len(left) and j < len(right) and len(result) < items_limit:
                    if left[i] >= right[j]:
                        result.append(left[i])
                        i += 1
                    else:
                        result.append(right[j])
                        j += 1
                while i < len(left) and len(result) < items_limit:
                    result.append(left[i])
                    i += 1
                while j < len(right) and len(result) < items_limit:
                    result.append(right[j])
                    j += 1

            return result

        return [x[1] for x in _sorted_query_node(self._root, items_limit)]

    def _fix_insert(self, node: Node) -> None:
        while node.parent.color == 1:
            if node.parent.parent.right == node.parent:
                u = node.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node.parent.left == node:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self._rotate_left(node.parent.parent)
            else:
                u = node.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node.parent.right == node:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self._rotate_right(node.parent.parent)

            if node == self._root:
                break

        self._root.color = 0

    def _rotate_right(self, x: Node) -> None:
        y = x.left
        self._push_down(y, x.heap_key)
        x.set_left(y.right)

        if not x.parent:
            self._root = y
            y.parent = None

        elif x == x.parent.left:
            x.parent.set_left(y)
        else:
            x.parent.set_right(y)

        y.set_right(x)
        self._push_up(x)

    def _rotate_left(self, x: Node) -> None:
        y = x.right
        self._push_down(y, x.heap_key)
        x.set_right(y.left)

        if not x.parent:
            self._root = y
            y.parent = None

        elif x == x.parent.left:
            x.parent.set_left(y)
        else:
            x.parent.set_right(y)

        y.set_left(x)
        self._push_up(x)

    def __len__(self) -> int:
        """
        Implements the built-in function len()

        Returns:
            int: Number of items in PST.

        Complexity:
            O(1)
        """
        return self._len

    def __contains__(self, key: _KEY) -> bool:
        """
        Implements membership test operator.

        Args:
            value: Value to test for membership

        Returns:
            bool:  ``True`` if value is in ``self``, ``False`` otherwise.

        Complexity:
            O(log(N)) where **N** is number of items in PST

        Note:
            this function is using ``tree_key(value)`` to compare the items
        """
        node = self._root
        while node != Node.NULL_NODE:
            if key < node.tree_key:
                node = node.left
            elif key == node.tree_key:
                return True
            else:
                node = node.right

        return False

    def clear(self) -> None:
        """
        Removes **all** items from PST.

        Complexity:
            O(1)
        """
        self._root = Node.NULL_NODE
        self._len = 0


_V = TypeVar("_V")


class PrioritySearchSet:
    """
    Class that represents Priority search tree.

    Example::

        # create new tree
        pst = PrioritySearchTree([(1,1),(2,2)])
        # add item to the tree
        pst.add((3,3))
        # perform 3 sided query
        result = pst.query((0,0),(4,0),(0,2))

    Args:
        iterable (Iterable): Initial values to build priority search tree. The default value is ``None``.
        tree_key (Callable): Specifies a function of one argument that is used to extract a *tree* comparison key
            from each element (for example, ``tree_key=str.lower``). The default value is ``tree_key=lambda x: x``
        heap_key (Callable): Specifies a function of one argument that is used to extract a *heap* comparison key
            from each element (for example, ``tree_key=str.lower``). The default value is ``tree_key=lambda x: x[1:]``

    Raises:
        ValueError: in case if iterable contains values with not unique tree_key

    Complexity:
        O(N*log(N)) where **N** is number of items to be added to new PST
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

    def heap_get_max(self) -> _KEY:
        """
        Return the item with the largest **heap_key** from the PST.

        Returns:
            item with the largest **heap_key**

        Raises:
            IndexError: If the PST is empty

        Complexity:
            O(1)
        """
        return self._values[self._pst.heap_get_max()]

    def heap_pop(self) -> _KEY:
        """
        Remove and return the item with the largest **heap_key** from the PST.

        Returns:
            item with the largest **heap_key**

        Raises:
            IndexError: If the PST is empty

        Complexity:
            O(log(N)) where **N** is number of items in PST
        """
        return self._values[self._pst.heap_pop()]

    def add(self, value: _V) -> None:
        """
        Add new item to PST.

        Args:
            value: Value to insert into PST

        Raises:
            ValueError: in case if value with **tree_key** already exists in PST

        Complexity:
            O(log(N)) where **N** is number of items in PST
        """
        key = self.key_func(value)
        priority = self.priority_func(value)
        self._pst.add(key, priority)
        self._values[key] = priority

    def remove(self, value: _V) -> _V:
        """
        Remove item from PST.

        Args:
            value: Value to remove from PST

        Raises:
            ValueError: in case if value not exists in PST

        Complexity:
            O(log(N)) where **N** is number of items in PST

        Note:
            this function is using ``tree_key(value)`` to compare the items
        """
        key = self.key_func(value)
        self._pst.remove(key)
        return self._values.pop(key)

    def query(self, left: _V, right: _V, bottom: _V) -> list[_V]:
        """Performs 3 sided query on PST.

        This function returns list of items that meet the following criteria:
            1. items have **tree_key** grater or equal to **tree_key** of tree_left argument
            2. items have **tree_key** smaller or equal to **tree_key** of tree_right argument
            3. items have **heap_key** grater or equal to **heap_key** of heap_bottom argument

        Args:
            tree_left: Left bound for query (**tree_key** is used).
            tree_right: Right bound for query (**tree_key** is used).
            heap_bottom: Bottom bound for query (**heap_key** is used).

        Returns:
            List: list of items that satisfy criteria, or empty list if no items found

        Complexity:
            O(log(N)+K) where **N** is number of items in PST and **K** is number of reported items
        """
        key_left = self.key_func(left)
        key_right = self.key_func(right)
        priority_bottom = self.priority_func(bottom)
        return [self._values[x] for x in self._pst.query(key_left, key_right, priority_bottom)]

    def sorted_query(self, left: _V, right: _V, bottom: _V, items_limit: int = 0) -> [_V]:
        """Performs 3 sided query on PST.

        This function returns list of items that meet the following criteria:
            1. items have **tree_key** grater or equal to **tree_key** of tree_left argument
            2. items have **tree_key** smaller or equal to **tree_key** of tree_right argument
            3. items have **heap_key** grater or equal to **heap_key** of heap_bottom argument

        Args:
            tree_left: Left bound for query (**tree_key** is used).
            tree_right: Right bound for query (**tree_key** is used).
            heap_bottom: Bottom bound for query (**heap_key** is used).
            items_limit (int): Number of items to return. Default value is ``0`` - no limit.

        Returns:
            List: list of items that satisfy criteria and sorted by **heap_key**
            (in case of limit, items with largest **heap_key** will be returned), or empty list if no items found

        Complexity:
            O(log(N)+K*log(K)) where **N** is number of items in PST and **K** is number of returned items
        """
        key_left = self.key_func(left)
        key_right = self.key_func(right)
        priority_bottom = self.priority_func(bottom)
        return [self._values[x] for x in self._pst.sorted_query(key_left, key_right, priority_bottom, items_limit)]

    def __len__(self) -> int:
        """
        Implements the built-in function len()

        Returns:
            int: Number of items in PST.

        Complexity:
            O(1)
        """
        return len(self._pst)

    def __contains__(self, item: _V) -> bool:
        """
        Implements membership test operator.

        Args:
            value: Value to test for membership

        Returns:
            bool:  ``True`` if value is in ``self``, ``False`` otherwise.

        Complexity:
            O(log(N)) where **N** is number of items in PST

        Note:
            this function is using ``tree_key(value)`` to compare the items
        """
        return self.key_func(item) in self._values

    def clear(self) -> None:
        """
        Removes **all** items from PST.

        Complexity:
            O(1)
        """
        self._pst.clear()
        self._values.clear()
