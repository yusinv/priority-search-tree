import random

from priority_search_tree import PrioritySearchTree
from utils import assert_rb_tree

ITEM_LIMITS = 100000
NUM_OF_ITEMS = 500
NUM_OF_CYCLES = 15

GEN_COUNTER = 0


def generate_items(items_count):
    global GEN_COUNTER
    result = list(
        zip(
            random.sample(range(ITEM_LIMITS), k=items_count),
            random.sample(range(ITEM_LIMITS), k=items_count),
            range(GEN_COUNTER, GEN_COUNTER + items_count),
        )
    )
    GEN_COUNTER += items_count
    return result


def stress_test():
    print()
    items = set()
    pst = PrioritySearchTree()
    for cycle in range(NUM_OF_CYCLES):
        items_to_add = random.randrange(NUM_OF_ITEMS - len(items))
        for item in generate_items(items_to_add):
            pst.add(item)
            items.add(item)
            assert_rb_tree(pst._root)

        x_min = (random.randrange(ITEM_LIMITS), -1, -1)
        x_max = (random.randrange(x_min[0], ITEM_LIMITS), -1, -1)
        y_min = (0, random.randrange(ITEM_LIMITS), -1)
        # print(x_min,x_max,y_min)

        query_expected = set()
        for item in items:
            if x_min <= item <= x_max and item[1:] >= y_min[1:]:
                query_expected.add(item)

        items_to_delete = pst.query(x_min, x_max, y_min)
        set_to_delete = set(items_to_delete)
        assert len(items_to_delete) == len(set_to_delete)
        assert set_to_delete == query_expected

        for item in items_to_delete:
            pst.remove(item)
            assert_rb_tree(pst._root)
            items.remove(item)

        print(f"iter {cycle} processed. items {len(items)} in tree")


if __name__ == "__main__":
    ITEM_LIMITS = 100000
    NUM_OF_ITEMS = 10000
    NUM_OF_CYCLES = 5000
    stress_test()
