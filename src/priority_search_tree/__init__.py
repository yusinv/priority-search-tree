__version__ = "0.0.0"

from collections import deque

from priority_search_tree.pst_node import Node


class PrioritySearchTree:

    def _push_down(self, node, value):
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

    def _push_up(self, node):
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

    def __init__(self, iterable=None, tree_key=lambda x: x, heap_key=lambda x: x[1:]):
        self._root = Node.NULL_NODE
        self.tree_key = tree_key
        self.heap_key = heap_key

        if iterable is not None:
            sn = sorted(iterable, key=self.tree_key)
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

    def heap_get_max(self):
        """get item with the largest heap_key

        Return the item with the largest heap_key from the PST, Complexity is O(1).

        Returns:
            item with the largest heap_key

        Raises:
            IndexError If the PST is empty

        """
        if self._root == Node.NULL_NODE:
            raise IndexError
        return self._root.heap_value

    def heap_pop(self):
        if self._root == Node.NULL_NODE:
            raise IndexError
        result = self._root.heap_value
        self.remove(result)
        return result

    def add(self, value):
        if self._root == Node.NULL_NODE:
            self._root = Node(heap_value=value, tree_value=value, color=0)
            return

        prev = None
        node = self._root
        while node != Node.NULL_NODE:
            prev = node
            if self.tree_key(value) < self.tree_key(node.tree_value):
                node = node.left
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

        if self.tree_key(value) < self.tree_key(prev.tree_value):
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

    def remove(self, value):
        node = self._root
        heap_node = None
        tree_node = None
        leaf_node = None

        while node != Node.NULL_NODE:
            leaf_node = node
            if heap_node is None and node.heap_value == value:
                heap_node = node
            if tree_node is None and node.tree_value == value:
                tree_node = node
            if self.tree_key(value) < self.tree_key(node.tree_value):
                node = node.left
            else:
                node = node.right

        if heap_node is None:
            raise ValueError(f"value not found:{value}")

        if leaf_node == self._root:
            self._root = Node.NULL_NODE
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

    def _fix_delete(self, node):
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
                    # parent = node.parent.parent
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

    def _transplant(self, u: Node, v: Node):
        if u.parent is None:
            self._root = v
            self._root.parent = None
        elif u == u.parent.left:
            u.parent.set_left(v)
        else:
            u.parent.set_right(v)

    def query(self, left_x, right_x, bottom_y):
        result = []
        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()

            if node == Node.NULL_NODE:
                continue

            if node.heap_value:
                if self.heap_key(node.heap_value) >= self.heap_key(bottom_y):
                    if self.tree_key(left_x) <= self.tree_key(node.heap_value) <= self.tree_key(right_x) and not node.placeholder:
                        result.append(node.heap_value)
                else:
                    continue

            if self.tree_key(right_x) < self.tree_key(node.tree_value):
                queue.append(node.left)
            elif self.tree_key(left_x) >= self.tree_key(node.tree_value):
                queue.append(node.right)
            else:
                queue.append(node.left)
                queue.append(node.right)

        return result

    def _fix_insert(self, node):
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

    def _rotate_right(self, x):
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

    def _rotate_left(self, x):
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
