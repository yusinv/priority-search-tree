__version__ = "0.0.1"

from collections import deque
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

    def _push_down(self, node: Node, value: _V) -> None:
        while node != Node.NULL_NODE:
            if node.heap_value is None:
                node.heap_value = value
                return

            if self.heap_key(value) > self.heap_key(node.heap_value):
                node.heap_value, value = value, node.heap_value
            elif self.heap_key(value) == self.heap_key(node.heap_value):
                node.placeholder = False

            if self.tree_key(value) < self.tree_key(node.tree_value):
                node = node.left
            else:
                node = node.right

    def _push_up(self, node: Node) -> None:
        vl, vr = None, None

        if not node.left.placeholder:
            vl = node.left.heap_value

        if not node.right.placeholder:
            vr = node.right.heap_value

        if vl and vr:
            if self.heap_key(vl) > self.heap_key(vr):
                node.heap_value = vl
                self._push_up(node.left)
            else:
                node.heap_value = vr
                self._push_up(node.right)
        elif vl:
            node.heap_value = vl
            self._push_up(node.left)
        elif vr:
            node.heap_value = vr
            self._push_up(node.right)
        else:
            if node.left == Node.NULL_NODE and node.right == Node.NULL_NODE:
                node.placeholder = True
            else:
                node.heap_value = None

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
                ln = Node(heap_value=value, tree_value=value)
                value = next(sn_iter)
                rn = Node(heap_value=value, tree_value=value)
                pn = Node(tree_value=rn.tree_value, color=0)
                pn.set_left(ln)
                pn.set_right(rn)
                self._push_up(pn)
                tree_nodes.append((pn, ln.tree_value, rn.tree_value))

            for value in sn_iter:
                pn = Node(heap_value=value, tree_value=value, color=0)
                tree_nodes.append((pn, pn.tree_value, pn.tree_value))

            while len(tree_nodes) > 1:
                new_nodes = []
                for i in range(0, len(tree_nodes), 2):
                    ln, ln_min, ln_max = tree_nodes[i]
                    rn, rn_min, rn_max = tree_nodes[i + 1]
                    pn = Node(tree_value=rn_min, color=0)
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
        if self._root == Node.NULL_NODE:
            self._root = Node(heap_value=value, tree_value=value, color=0)
            self._len = 1
            return

        value_tree_key = self.tree_key(value)

        prev = None
        node = self._root
        while node != Node.NULL_NODE:
            prev = node
            if value_tree_key < self.tree_key(node.tree_value):
                node = node.left
            elif value_tree_key == self.tree_key(node.tree_value):
                raise ValueError(f"Value with tree_key:{value_tree_key} already in tree")
            else:
                node = node.right

        new_internal_node = Node(color=prev.color)
        new_leaf_node = Node(tree_value=value, heap_value=value, placeholder=True)
        prev.color = 1

        if prev.parent:
            if prev.parent.left == prev:
                prev.parent.set_left(new_internal_node)
            else:
                prev.parent.set_right(new_internal_node)
        else:
            self._root = new_internal_node
            new_internal_node.color = 0

        if value_tree_key < self.tree_key(prev.tree_value):
            new_internal_node.tree_value = prev.tree_value
            new_internal_node.set_right(prev)
            new_internal_node.set_left(new_leaf_node)
        else:
            new_internal_node.tree_value = value
            new_internal_node.set_right(new_leaf_node)
            new_internal_node.set_left(prev)

        if not prev.placeholder:
            new_internal_node.heap_value = prev.heap_value
            prev.placeholder = True

        self._push_down(self._root, value)
        self._fix_insert(new_leaf_node)
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
        """
        node = self._root
        value_tree_key = self.tree_key(value)
        value_heap_key = self.heap_key(value)
        heap_node = None
        tree_node = None
        leaf_node = None

        while node != Node.NULL_NODE:
            leaf_node = node
            if heap_node is None and self.tree_key(node.heap_value) == value_tree_key and self.heap_key(node.heap_value) == value_heap_key:
                heap_node = node
            if tree_node is None and self.tree_key(node.tree_value) == value_tree_key:
                tree_node = node
            if value_tree_key < self.tree_key(node.tree_value):
                node = node.left
            else:
                node = node.right

        if heap_node is None:
            raise ValueError(f"Value not found:{value}")

        if leaf_node == self._root:
            self._root = Node.NULL_NODE
            self._len = 0
            return

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

        self._push_down(cut_node, cut_node.heap_value)
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
        result = []
        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()

            if node == Node.NULL_NODE or node.placeholder:
                continue

            if node.heap_value:
                if self.heap_key(node.heap_value) >= self.heap_key(heap_bottom):
                    if self.tree_key(tree_left) <= self.tree_key(node.heap_value) <= self.tree_key(tree_right):
                        result.append(node.heap_value)
                else:
                    continue

            if self.tree_key(tree_right) < self.tree_key(node.tree_value):
                queue.append(node.left)
            elif self.tree_key(tree_left) >= self.tree_key(node.tree_value):
                queue.append(node.right)
            else:
                queue.append(node.left)
                queue.append(node.right)

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

        def _query_node(node, limit):
            result = []
            if node == Node.NULL_NODE or node.placeholder or limit == 0:
                return result

            if node.heap_value:
                if self.heap_key(node.heap_value) >= heap_bottom_key:
                    if tree_left_key <= self.tree_key(node.heap_value) <= tree_right_key:
                        result.append(node.heap_value)
                        limit -= 1
                else:
                    return result

            if tree_right_key < self.tree_key(node.tree_value):
                result.extend(_query_node(node.left, limit))
            elif tree_left_key >= self.tree_key(node.tree_value):
                result.extend(_query_node(node.right, limit))
            else:
                left = _query_node(node.left, limit)
                right = _query_node(node.right, limit)
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

        return _query_node(self._root, items_limit)

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

    def __len__(self):
        return self._len
