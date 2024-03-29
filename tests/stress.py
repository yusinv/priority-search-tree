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
    pst = PrioritySearchTree(tree_key=tree_key_func, heap_key=heap_key_func)
    for cycle in range(NUM_OF_CYCLES):
        items_count = random.randrange(NUM_OF_ITEMS - len(items))
        for item in generate_items(items_count, cycle=cycle):
            pst.add(item)
            items[tree_key_func(item)] = item

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

        query_expected = []
        for item_tree_key, item in items.items():
            if x_min <= item_tree_key <= x_max and heap_key_func(item) >= heap_key_func(items[y_min]):
                query_expected.append(item)

        query_result = pst.query(items[x_min], items[x_max], items[y_min])

        query_result.sort(key=tree_key_func)
        query_result.sort(key=heap_key_func, reverse=True)
        query_expected.sort(key=tree_key_func)
        query_expected.sort(key=heap_key_func, reverse=True)

        assert len(query_result) == len(query_expected)
        assert query_result == query_expected
        assert pst.sorted_query(items[x_min], items[x_max], items[y_min]) == query_expected

        for item in query_result:
            assert item in pst
            pst.remove(item)
            assert item not in pst
            items.pop(tree_key_func(item))

        assert_rb_tree(pst._root)

        if pst:
            item = pst.heap_pop()
            items.pop(tree_key_func(item))
            assert_rb_tree(pst._root)

        print(f"iter {cycle} processed. items {len(items)} in tree")


# if __name__ == "__main__":
#     ITEM_LIMITS = 10
#     NUM_OF_ITEMS = 10000
#     NUM_OF_CYCLES = 500
#     stress_test()
