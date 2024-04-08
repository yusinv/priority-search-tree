import random
from typing import Any
from typing import Iterable

from priority_search_tree import PrioritySearchTree
from utils import assert_rb_tree

ITEM_LIMITS = 100000
NUM_OF_ITEMS = 500
NUM_OF_CYCLES = 15


def tree_key_func(item: Any) -> Any:
    return id(item)


def heap_key_func(item: Any) -> Any:
    return item[::-1]


def generate_items(count: int, **kwargs) -> Iterable:
    return ((kwargs["cycle"], val) for val in random.choices(range(ITEM_LIMITS), k=count))


def stress_test():
    print()
    items = {}
    pst = PrioritySearchTree()
    for cycle in range(NUM_OF_CYCLES):
        items_count = random.randrange(NUM_OF_ITEMS - len(items))
        for item in generate_items(items_count, cycle=cycle):
            key = tree_key_func(item)
            pst[key] = heap_key_func(item)
            items[key] = item

        assert_rb_tree(pst._root)

        if not items:
            print("skipped due to empty list")
            continue

        lk = list(items.keys())
        x_min = random.choice(lk)
        x_max = random.choice(lk)
        if x_min > x_max:
            x_min, x_max = x_max, x_min
        y_min = random.choice(lk)

        tmp = []
        for item_tree_key, item in items.items():
            if x_min <= item_tree_key <= x_max and heap_key_func(item) >= heap_key_func(items[y_min]):
                tmp.append(item)

        query_expected = [tree_key_func(x) for x in sorted(tmp, key=lambda x: (heap_key_func(x), tree_key_func(x)), reverse=True)]

        query_result = pst.query(x_min, x_max, heap_key_func(items[y_min]))
        assert len(query_result) == len(query_expected)
        assert set(query_result) == set(query_expected)
        assert pst.sorted_query(x_min, x_max, heap_key_func(items[y_min])) == query_expected

        for item in query_result:
            assert item in pst
            del pst[item]
            assert item not in pst
            items.pop(item)

        assert_rb_tree(pst._root)

        if pst:
            k, p = pst.popitem()
            items.pop(k)
            assert_rb_tree(pst._root)

        print(f"iter {cycle} processed. items {len(items)} in tree")


if __name__ == "__main__":
    ITEM_LIMITS = 10
    NUM_OF_ITEMS = 100000
    NUM_OF_CYCLES = 500
    stress_test()
