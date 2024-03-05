from priority_search_tree import Node


def assert_rb_tree(node):
    if node == Node.NULL_NODE:
        return 1
    result = 0
    if node.color == 0:
        result += 1
    else:
        assert node.parent
        assert node.parent.color == 0
    rr = assert_rb_tree(node.right)
    rl = assert_rb_tree(node.left)
    assert rr == rl
    return result + rr
