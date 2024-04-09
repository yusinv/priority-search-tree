from typing import Iterable
from typing import Iterator
from typing import MutableMapping
from typing import Optional
from typing import Tuple
from typing import TypeVar

from .ps_tree_node import Node

_KEY = TypeVar("_KEY")
_PRIORITY = TypeVar("_PRIORITY")


class PrioritySearchTree(MutableMapping):
    """Class that represents Priority search tree.

    PrioritySearchTree is a mutable mapping that stores **keys** and corresponding **priorities**.

    * Keys are stored in balanced binary search tree (red/black tree) that allow to effectively perform next operations:

            * in order traversal
            * find min/max keys
            * find next/previous keys

    * Priorities and keys form max priority queue, that allow to effectively perform next operations:

            * find element with max priority
            * remove element with max priority
            * update priority for a given key

    * It is capable to perform 3 sided queries

    Example::

        # create new tree
        pst = PrioritySearchTree([(1,1),(2,2)])
        # add key 3 to the tree with priority 5
        pst[3] = 5
        # perform 3 sided query
        result = pst.query(0,4,2)

    Args:
        iterable (Iterable): Initial values to build priority search tree.
            Each item in the iterable must itself be an iterable with exactly two objects.
            The first object of each item becomes a **key** in the new pst, and the second object the corresponding
            **priority**. The default value is ``None``.

    Raises:
        KeyError: in case if iterable contains values with not unique **key**

    Complexity:
        `O(N*log(N))` where **N** is number of items to be added to new PST
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

    def _sift_down(self, node: Node, heap_key: Tuple[_PRIORITY, _KEY]) -> None:

        if node.heap_key[0] == Node.PLACEHOLDER_VALUE:
            node.heap_key = heap_key
            return

        if heap_key > node.heap_key:
            self._push_down(node, heap_key)
            return

        if heap_key[1] < node.tree_key:
            self._sift_down(node.left, heap_key)
        else:
            self._sift_down(node.right, heap_key)

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
                    raise KeyError(f"More than one item with key:{current_key[0]}")
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

    def get_with_max_priority(self) -> _KEY:
        """Returns the **key** with the largest **priority** in PST.

        Returns:
            **key** with the largest **priority**

        Raises:
            KeyError: If the PST is empty

        Complexity:
            `O(1)`
        """
        if self._root == Node.NULL_NODE:
            raise KeyError
        return self._root.heap_key[1]

    def popitem(self) -> Tuple[_KEY, _PRIORITY]:
        """Remove and return (key, priority) pair from the PST. Pair with max **priority** will be removed.

        Returns:
            Tuple: **key** and **priority** pair

        Raises:
            KeyError: If the PST is empty

        Complexity:
            `O(log(N))` where **N** is number of items in PST
        """
        if self._root == Node.NULL_NODE:
            raise KeyError
        result = self._root.heap_key
        del self[result[1]]
        return result[1], result[0]

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

    def query(self, key_left: _KEY, key_right: _KEY, priority_bottom: _PRIORITY) -> list:
        """Performs 3 sided query on PST.

        This function returns list of items that meet the following criteria:
            1. items have **key** grater or equal to `key_left` argument
            2. items have **key** smaller or equal to `key_right` argument
            3. items have **priority** grater or equal to `priority_bottom` argument

        Args:
            key_left: Left bound for query (**key** is used to compare).
            key_right: Right bound for query (**key** is used to compare).
            priority_bottom: Bottom bound for query (**priority** is used to compare).

        Returns:
            List: list of **keys** that satisfy criteria, or empty list if no items found

        Complexity:
            `O(log(N)+K)` where **N** is number of items in PST and **K** is number of reported items
        """
        result = []

        def _query_node(node) -> None:
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

    def sorted_query(self, key_left: _KEY, key_right: _KEY, priority_bottom: _PRIORITY, items_limit: int = 0) -> list:
        """Performs 3 sided query on PST.

        This function returns list of items that meet the following criteria:
            1. items have **key** grater or equal to `key_left` argument
            2. items have **key** smaller or equal to `key_right` argument
            3. items have **priority** grater or equal to `priority_bottom` argument

        Args:
            key_left: Left bound for query (**key** is used to compare).
            key_right: Right bound for query (**key** is used to compare).
            priority_bottom: Bottom bound for query (**priority** is used to compare).
            items_limit (int): Number of items to return. Default value is ``0`` - no limit.

        Returns:
            List: list of items that satisfy criteria and sorted by **priority**
            (in case of limit, items with largest **priority** will be returned), or empty list if no items found

        Complexity:
            `O(log(N)+K*log(K))` where **N** is number of items in PST and **K** is number of returned items
        """
        if items_limit <= 0:
            items_limit = self._len

        def _sorted_query_node(node, limit) -> list:
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
        """Implements the built-in function len()

        Returns:
            int: Number of items in PST.

        Complexity:
            `O(1)`
        """
        return self._len

    def clear(self) -> None:
        """Removes **all** items from PST.

        Complexity:
            `O(1)`
        """
        self._root = Node.NULL_NODE
        self._len = 0

    def update_priority(self, key: _KEY, priority: _PRIORITY) -> _PRIORITY:
        """Updates priority for the given key.

        Args:
            key: **key** to update
            priority: new **priority** value

        Returns:
            old **priority** value

        Raises:
            KeyError: in case if **key** not exists in PST

        Complexity:
            `O(log(N))` where **N** is number of items in PST

        """
        node = self._root
        heap_node = None
        while node.heap_key[0] != Node.PLACEHOLDER_VALUE:

            if key == node.heap_key[1]:
                heap_node = node
                break

            if key < node.tree_key:
                node = node.left
            else:
                node = node.right

        if not heap_node:
            raise KeyError(f"Key not found:{key}")

        result = heap_node.heap_key[0]
        self._push_up(heap_node)
        self._sift_down(self._root, (priority, key))
        return result

    def __setitem__(self, key: _KEY, priority: _PRIORITY) -> None:
        """implements assignment operation.

        Args:
            key: **key** to add/update
            priority: new **priority**

        Complexity:
            `O(log(N))` where **N** is number of items in PST

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
                self.update_priority(key, priority)
                return
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

        self._sift_down(self._root, (priority, key))
        self._fix_insert(new_placeholder)
        self._len += 1

    def __delitem__(self, key: _KEY) -> None:
        """Remove **key** from PST.

        Args:
            key: **key** to remove

        Raises:
            KeyError: in case if **key** not exists in PST

        Complexity:
            `O(log(N))` where **N** is number of items in PST
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
            raise KeyError(f"Key not found:{key}")

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

    def __getitem__(self, key: _KEY) -> _PRIORITY:
        """Returns **priority** of given **key** in PST.

        Args:
            key: **key** to find

        Returns:
            **priority** value if the given **key**

        Raises:
            KeyError: in case if **key** not exists in PST

        Complexity:
            `O(log(N))` where **N** is number of items in PST
        """
        node = self._root
        heap_node = None
        while node.heap_key[0] != Node.PLACEHOLDER_VALUE:
            if key == node.heap_key[1]:
                heap_node = node
                break
            if key < node.tree_key:
                node = node.left
            else:
                node = node.right

        if not heap_node:
            raise KeyError(f"Key not found:{key}")

        return heap_node.heap_key[0]

    def __iter__(self) -> Iterator:
        """Create an iterator that iterates **keys** in sorted order

        Returns:
            Iterator: in order iterator
        """
        stack = []
        current = self._root
        yielded_key = None
        while True:
            if current != Node.NULL_NODE:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                if current.tree_key != yielded_key:
                    yielded_key = current.tree_key
                    yield yielded_key
                current = current.right
            else:
                break
