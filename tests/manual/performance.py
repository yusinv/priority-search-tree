import gc
import heapq
import multiprocessing
import random
from statistics import mean
from time import perf_counter_ns

from sortedcontainers import SortedSet

from priority_search_tree import PrioritySearchSet

NUMBER_OF_ITEMS = [1, 100, 10000, 1000000]
REPEAT_COUNT = 1

TIMEOUT_SEC = 60

DATATYPES = ["PrioritySearchSet", "Set", "HeapQ", "Dict", "SortedSet"]


def create_pst(items, sub_items, extra_items):
    PrioritySearchSet(key_func=pst_key, priority_func=pst_priority, iterable=items)


def create_set(items, sub_items, extra_items):
    set(items)


def create_heap(items, sub_items, extra_items):
    heapq.heapify(list(items))


def create_dict(items, sub_items, extra_items):
    dict(items)


def create_sorted(items, sub_items, extra_items):
    SortedSet(items, key=pst_key)


CREATE = {"PrioritySearchSet": create_pst, "Set": create_set, "HeapQ": create_heap, "Dict": create_dict, "SortedSet": create_sorted}


def add_pst(pst, sub_items, extra_items):
    pst.add(extra_items[0])


def add_set(st, sub_items, extra_items):
    st.add(extra_items[0])


def add_heap(heap, sub_items, extra_items):
    heapq.heappush(heap, extra_items[0])


def add_dict(dct, sub_items, extra_items):
    itm = extra_items[0]
    dct[itm[0]] = itm[1]


def add_sorted(ss: SortedSet, sub_items, extra_items):
    itm = extra_items[0]
    ss.add(itm)


ADD = {"PrioritySearchSet": add_pst, "Set": add_set, "HeapQ": add_heap, "Dict": add_dict, "SortedSet": add_sorted}


def remove_pst(pst, sub_items, extra_items):
    pst.remove(sub_items[0])


def remove_set(st: set, sub_items, extra_items):
    st.remove(sub_items[0])


def remove_heap(heap: list, sub_items, extra_items):
    x = heap.index(sub_items[0])
    heap[x] = heap[-1]
    heap.pop()
    heapq.heapify(heap)


def remove_dict(dct: dict, sub_items, extra_items):
    dct.pop(sub_items[0][0])


def remove_sorted(ss: SortedSet, sub_items, extra_items):
    ss.remove(sub_items[0])


REMOVE = {"PrioritySearchSet": remove_pst, "Set": remove_set, "HeapQ": remove_heap, "Dict": remove_dict, "SortedSet": remove_sorted}


def pop_pst(pst: PrioritySearchSet, sub_items, extra_items):
    pst.pop()


def pop_set(st: set, sub_items, extra_items):
    mx = max(st, key=pst_priority)
    st.remove(mx)


def pop_heap(heap: list, sub_items, extra_items):
    heapq.heappop(heap)


def pop_dict(dct: dict, sub_items, extra_items):
    mx = max(dct.items(), key=pst_priority)
    dct.pop(mx[0])


def pop_sorted(ss: SortedSet, sub_items, extra_items):
    mx = max(ss, key=pst_priority)
    ss.remove(mx)


PRIORITY_POP = {"PrioritySearchSet": pop_pst, "Set": pop_set, "HeapQ": pop_heap, "Dict": pop_dict, "SortedSet": pop_sorted}


def setup_generic(num_of_initial, num_of_existing, num_of_extra):
    if num_of_initial == 1:
        initial_items = [(0, 5)]
        max_priority = 10
    else:
        max_priority = num_of_initial // 2
        initial_priorities = list(range(max_priority))
        random.shuffle(initial_priorities)
        initial_items = [(x[0] * 2, x[1]) for x in enumerate(initial_priorities)]
        random.shuffle(initial_priorities)
        initial_items.extend((x[0] * 2, x[1]) for x in enumerate(initial_priorities, start=len(initial_priorities)))
        random.shuffle(initial_items)
    sub_items = random.sample(initial_items, k=num_of_existing)
    extra_items = [(x[0] + 1, random.randrange(max_priority)) for x in random.sample(initial_items, k=num_of_extra)]
    return initial_items, sub_items, extra_items


def pst_key(x):
    return x[0]


def pst_priority(x):
    return x[1]


def setup_pst(num_of_initial, num_of_sub, num_of_extra):
    initial_items, sub_items, extra_items = setup_generic(num_of_initial, num_of_sub, num_of_extra)
    return PrioritySearchSet(key_func=pst_key, priority_func=pst_priority, iterable=initial_items), sub_items, extra_items


def setup_set(num_of_initial, num_of_sub, num_of_extra):
    initial_items, sub_items, extra_items = setup_generic(num_of_initial, num_of_sub, num_of_extra)
    return set(initial_items), sub_items, extra_items


def setup_heap(num_of_initial, num_of_sub, num_of_extra):
    initial_items, sub_items, extra_items = setup_generic(num_of_initial, num_of_sub, num_of_extra)
    return initial_items.copy(), sub_items, extra_items


def setup_dict(num_of_initial, num_of_sub, num_of_extra):
    initial_items, sub_items, extra_items = setup_generic(num_of_initial, num_of_sub, num_of_extra)
    return dict(initial_items), sub_items, extra_items


def setup_sorted(num_of_initial, num_of_sub, num_of_extra):
    initial_items, sub_items, extra_items = setup_generic(num_of_initial, num_of_sub, num_of_extra)
    return SortedSet(initial_items, key=pst_key), sub_items, extra_items


SETUP = {"PrioritySearchSet": setup_pst, "Set": setup_set, "HeapQ": setup_heap, "Dict": setup_dict, "SortedSet": setup_sorted}

SETUP_GENERIC = {
    "PrioritySearchSet": setup_generic,
    "Set": setup_generic,
    "HeapQ": setup_generic,
    "Dict": setup_generic,
    "SortedSet": setup_generic,
}


def query10_pst(pst: PrioritySearchSet, sub_items, extra_items):
    pos = len(pst)
    pst.query((0, 0), (pos, pos), (0, pos // 2 - 10))


def query10_set(st: set, sub_items, extra_items):
    pos = len(st)
    result = []
    for itm in st:
        if 0 <= itm[0] <= pos and itm[1] >= pos // 2 - 10:
            result.append(itm)


def query10_heap(heap: list, sub_items, extra_items):
    pos = len(heap)
    result = []
    for itm in heap:
        if 0 <= itm[0] <= pos and itm[1] >= pos // 2 - 10:
            result.append(itm)


def query10_dict(dct: dict, sub_items, extra_items):
    pos = len(dct)
    result = []
    for ik, iv in dct.items():
        if 0 <= ik <= pos and iv >= pos // 2 - 10:
            result.append((ik, iv))


def query10_sorted(ss: SortedSet, sub_items, extra_items):
    pos = len(ss)
    result = []
    for itm in ss.irange((0, 0), (pos, 0)):
        if pst_priority(itm) >= pos // 2 - 10:
            result.append(itm)


QUERY10 = {"PrioritySearchSet": query10_pst, "Set": query10_set, "HeapQ": query10_heap, "Dict": query10_dict, "SortedSet": query10_sorted}


def _exec(init_fun, exec_fun, *args):
    exec_args = init_fun(*args)
    gc.disable()
    st = perf_counter_ns()
    exec_fun(*exec_args)
    return perf_counter_ns() - st


def perf_measurement(setup_fun, exec_fun, repeat_cycles, *args):
    times = []
    for _ in range(repeat_cycles):
        try:
            with multiprocessing.Pool() as pool:
                result = pool.apply_async(_exec, [setup_fun, exec_fun, *args]).get(timeout=TIMEOUT_SEC)
        except multiprocessing.TimeoutError:
            return -1

        times.append(result)

    return mean(times)


def zero(x):
    return 0


def one(x):
    return 1


def counts(x):
    return x


def perf_test(name: str, setup, exe, init_cnt, sub_cnt, extra_cnt):
    print(f"{name:=^110}")
    print(f"{'':^9}", end="|")
    for dtype in DATATYPES:
        print(f"{dtype:^19}", end="|")
    print()
    print(f"{'':-^110}")
    for cnt in NUMBER_OF_ITEMS:
        print(f"{cnt:>9}", end="|")
        for dtype in DATATYPES:
            time = perf_measurement(setup[dtype], exe[dtype], REPEAT_COUNT, init_cnt(cnt), sub_cnt(cnt), extra_cnt(cnt))
            print(f"{time:>19}", end="|")
        print()
    print(f"{'':-^110}")


if __name__ == "__main__":
    # create
    perf_test(" Create from iterable. ", SETUP_GENERIC, CREATE, counts, zero, zero)

    # add
    perf_test(" Add item. ", SETUP, ADD, counts, zero, one)

    # delete
    perf_test(" Delete random item. ", SETUP, REMOVE, counts, one, zero)

    # heap pop
    perf_test(" Delete item with max priority. ", SETUP, PRIORITY_POP, counts, zero, zero)

    # 3-sided query 10 items (0<key<N//2 and priority>N-10)
    perf_test(" 3-sided query (10 items). ", SETUP, QUERY10, counts, zero, zero)
