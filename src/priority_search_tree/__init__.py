__version__ = "0.0.2"

from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TypeVar

from .pst_node import Node

_V = TypeVar("_V")
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

    __slots__ = ["_root", "_len", "tree_key", "heap_key"]

    def _push_down(self, node: Node, value: _V) -> None:

        if node.heap_value == Node.PLACEHOLDER_VALUE:
            node.heap_value = value
            return

        if self.tree_key(node.heap_value) < node.tree_value:
            self._push_down(node.left, node.heap_value)
        else:
            self._push_down(node.right, node.heap_value)

        node.heap_value = value

    def _sieve_down(self, node: Node, value: _V) -> None:

        if node.heap_value == Node.PLACEHOLDER_VALUE:
            node.heap_value = value
            return

        heap_key_value = self.heap_key(value)
        tree_key_value = self.tree_key(value)

        if heap_key_value > self.heap_key(node.heap_value):
            self._push_down(node, value)
            return

        if heap_key_value == self.heap_key(node.heap_value) and tree_key_value < self.tree_key(node.heap_value):
            self._push_down(node, value)
            return

        if tree_key_value < node.tree_value:
            self._sieve_down(node.left, value)
        else:
            self._sieve_down(node.right, value)

    def _push_up(self, node: Node) -> None:
        if node.heap_value == Node.PLACEHOLDER_VALUE:
            return

        if node.left.heap_value == Node.PLACEHOLDER_VALUE:
            node.heap_value = node.right.heap_value
            self._push_up(node.right)
            return

        if node.right.heap_value == Node.PLACEHOLDER_VALUE:
            node.heap_value = node.left.heap_value
            self._push_up(node.left)
            return

        if self.heap_key(node.left.heap_value) >= self.heap_key(node.right.heap_value):
            node.heap_value = node.left.heap_value
            self._push_up(node.left)
        else:
            node.heap_value = node.right.heap_value
            self._push_up(node.right)

    def __init__(
        self,
        iterable: Optional[Iterable[_V]] = None,
        tree_key: Callable[[_V], _SupportsRichComparisonT] = lambda x: x,
        heap_key: Callable[[_V], _SupportsRichComparisonT] = lambda x: x[1:],
    ) -> None:
        self._root: Node = Node.NULL_NODE
        self.tree_key = tree_key
        self.heap_key = heap_key
        self._len: int = 0

        if iterable:
            sn = sorted(iterable, key=self.tree_key)

            current_key = self.tree_key(sn[0])
            for next_key in map(self.tree_key, sn[1:]):
                if current_key == next_key:
                    raise ValueError(f"More than one item with tree_key:{current_key}")
                current_key = next_key

            sn_len = len(sn)
            sn_iter = iter(sn)
            tree_nodes = []
            lvl = sn_len.bit_length()
            for _ in range(sn_len - 2 ** (lvl - 1)):
                value = next(sn_iter)
                ln = Node(tree_value=self.tree_key(value), heap_value=value)
                value = next(sn_iter)
                rn = Node(tree_value=self.tree_key(value), heap_value=value)
                pn = Node(tree_value=rn.tree_value, heap_value=value, color=0)
                pn.set_left(ln)
                pn.set_right(rn)
                self._push_up(pn)
                tree_nodes.append((pn, ln.tree_value, rn.tree_value))

            for value in sn_iter:
                pn = Node(tree_value=self.tree_key(value), heap_value=value, color=0)
                tree_nodes.append((pn, pn.tree_value, pn.tree_value))

            while len(tree_nodes) > 1:
                new_nodes = []
                for i in range(0, len(tree_nodes), 2):
                    ln, ln_min, ln_max = tree_nodes[i]
                    rn, rn_min, rn_max = tree_nodes[i + 1]
                    pn = Node(tree_value=rn_min, heap_value=ln.heap_value, color=0)
                    pn.set_left(ln)
                    pn.set_right(rn)
                    self._push_up(pn)
                    new_nodes.append((pn, ln_min, rn_max))
                tree_nodes = new_nodes

            self._root = tree_nodes[0][0]
            self._len = sn_len

    def heap_get_max(self) -> _V:
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
        return self._root.heap_value

    def heap_pop(self) -> _V:
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
        result = self._root.heap_value
        self.remove(result)
        return result

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
        value_tree_key = self.tree_key(value)

        if self._root == Node.NULL_NODE:
            self._root = Node(tree_value=value_tree_key, heap_value=value, color=0)
            self._len = 1
            return

        prev = None
        node = self._root
        while node != Node.NULL_NODE:
            prev = node
            if value_tree_key < node.tree_value:
                node = node.left
            elif value_tree_key == node.tree_value:
                raise ValueError(f"Value with tree_key:{value_tree_key} already in tree")
            else:
                node = node.right

        new_placeholder = Node(tree_value=value_tree_key, heap_value=Node.PLACEHOLDER_VALUE)
        prev_placeholder = Node(tree_value=prev.tree_value, heap_value=Node.PLACEHOLDER_VALUE)

        if value_tree_key < prev.tree_value:
            prev.set_right(prev_placeholder)
            prev.set_left(new_placeholder)
        else:
            prev.tree_value = value_tree_key
            prev.set_right(new_placeholder)
            prev.set_left(prev_placeholder)

        self._sieve_down(self._root, value)
        self._fix_insert(new_placeholder)
        self._len += 1

    def remove(self, value: _V) -> None:
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
        value_tree_key = self.tree_key(value)

        tree_node = None
        node = self._root
        while node != Node.NULL_NODE:
            if value_tree_key == node.tree_value:
                tree_node = node
                break
            elif value_tree_key < node.tree_value:
                node = node.left
            else:
                node = node.right

        if tree_node is None:
            raise ValueError(f"Value not found:{value}")

        leaf_node = None
        node = tree_node
        while node != Node.NULL_NODE:
            leaf_node = node
            if value_tree_key < node.tree_value:
                node = node.left
            else:
                node = node.right

        if leaf_node == self._root:
            self._root = Node.NULL_NODE
            self._len = 0
            return

        heap_node = None
        node = leaf_node
        while node:
            if node.heap_value != Node.PLACEHOLDER_VALUE:
                if self.tree_key(node.heap_value) == value_tree_key:
                    heap_node = node
                    break
            node = node.parent

        self._push_up(heap_node)

        if tree_node.left == Node.NULL_NODE:  # left node
            cut_node = tree_node.parent
            fix_node = tree_node.parent.right
        elif tree_node.right == leaf_node:  # leaf children
            cut_node = tree_node
            fix_node = tree_node.left
        else:  # subtree case
            tree_node.tree_value = leaf_node.parent.tree_value
            cut_node = leaf_node.parent
            fix_node = leaf_node.parent.right

        self._push_down(cut_node, None)
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

    def query(self, tree_left: _V, tree_right: _V, heap_bottom: _V) -> [_V]:
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
        tree_left_key = self.tree_key(tree_left)
        tree_right_key = self.tree_key(tree_right)
        heap_bottom_key = self.heap_key(heap_bottom)
        result = []

        def _query_node(node):
            if node == Node.NULL_NODE or node.heap_value == Node.PLACEHOLDER_VALUE:
                return

            if self.heap_key(node.heap_value) >= heap_bottom_key:
                if tree_left_key <= self.tree_key(node.heap_value) <= tree_right_key:
                    result.append(node.heap_value)
            else:
                return

            if tree_right_key < node.tree_value:
                _query_node(node.left)
            elif tree_left_key >= node.tree_value:
                _query_node(node.right)
            else:
                _query_node(node.left)
                _query_node(node.right)

        _query_node(self._root)
        return result

    def sorted_query(self, tree_left: _V, tree_right: _V, heap_bottom: _V, items_limit: int = 0) -> [_V]:
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
        tree_left_key = self.tree_key(tree_left)
        tree_right_key = self.tree_key(tree_right)
        heap_bottom_key = self.heap_key(heap_bottom)
        if items_limit <= 0:
            items_limit = self._len

        def _sorted_query_node(node, limit):
            result = []
            if node == Node.NULL_NODE or node.heap_value == Node.PLACEHOLDER_VALUE or limit == 0:
                return result

            if self.heap_key(node.heap_value) >= heap_bottom_key:
                if tree_left_key <= self.tree_key(node.heap_value) <= tree_right_key:
                    result.append(node.heap_value)
                    limit -= 1
            else:
                return result

            if tree_right_key < node.tree_value:
                result.extend(_sorted_query_node(node.left, limit))
            elif tree_left_key >= node.tree_value:
                result.extend(_sorted_query_node(node.right, limit))
            else:
                left = _sorted_query_node(node.left, limit)
                right = _sorted_query_node(node.right, limit)
                # merge
                i, j = 0, 0
                while i < len(left) and j < len(right) and len(result) < items_limit:
                    if self.heap_key(left[i]) >= self.heap_key(right[j]):
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

        return _sorted_query_node(self._root, items_limit)

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
        self._push_down(y, x.heap_value)
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
        self._push_down(y, x.heap_value)
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

    def __contains__(self, value) -> bool:
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
        value_tree_key = self.tree_key(value)

        node = self._root
        while node != Node.NULL_NODE:
            if value_tree_key < node.tree_value:
                node = node.left
            elif value_tree_key == node.tree_value:
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
