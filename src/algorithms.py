import copy
import itertools
import time


class Item:
    def __init__(self, id, weight, value):
        self.id = id
        self.weight = weight
        self.value = value

    def __repr__(self):
        return f"Item(id={self.id}, w={self.weight}, v={self.value})"

class Mule:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.items = []
        self.current_weight = 0
        self.current_value = 0

    def add_item(self, item):
        if self.current_weight + item.weight <= self.capacity:
            self.items.append(item)
            self.current_weight += item.weight
            self.current_value += item.value
            return True
        return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.weight
            self.current_value -= item.value
            return True
        return False

    def clear(self):
        self.items = []
        self.current_weight = 0
        self.current_value = 0

    def __repr__(self):
        return f"Mule(id={self.id}, cap={self.capacity}, cur_w={self.current_weight}, cur_v={self.current_value})"


def calculate_difference(mules):
    if not mules:
        return 0
    values = [m.current_value for m in mules]
    return max(values) - min(values)


def brute_force_solve(items, mules_config):
    start_time = time.time()
    best_diff = float('inf')
    best_assignment = None

    num_items = len(items)
    num_mules = len(mules_config)

    for assignment in itertools.product(range(num_mules), repeat=num_items):

        current_mules = copy.deepcopy(mules_config)
        valid = True

        for item_idx, mule_idx in enumerate(assignment):
            item = items[item_idx]
            if not current_mules[mule_idx].add_item(item):
                valid = False
                break

        if valid:
            diff = calculate_difference(current_mules)
            if diff < best_diff:
                best_diff = diff
                best_assignment = current_mules

    end_time = time.time()
    return best_assignment, best_diff, end_time - start_time


def greedy_solve(items, mules_config):

    start_time = time.time()

    sorted_items = sorted(items, key=lambda x: x.value, reverse=True)

    mules = copy.deepcopy(mules_config)

    possible = True
    for item in sorted_items:
        best_mule = None
        min_current_val = float('inf')

        for mule in mules:
            if mule.current_weight + item.weight <= mule.capacity:
                if mule.current_value < min_current_val:
                    min_current_val = mule.current_value
                    best_mule = mule

        if best_mule:
            best_mule.add_item(item)
        else:
            possible = False
            break

    end_time = time.time()

    if not possible:
        return None, float('inf'), end_time - start_time

    diff = calculate_difference(mules)
    return mules, diff, end_time - start_time


def hill_climbing_solve(items, mules_config, max_iter=1000):
    """
    Starts with Greedy solution and tries to improve it.
    """
    start_time = time.time()

    current_mules, current_diff, _ = greedy_solve(items, mules_config)

    if current_mules is None:
        return None, float('inf'), time.time() - start_time

    improved = True
    iterations = 0

    while improved and iterations < max_iter:
        improved = False
        iterations += 1

        mules_sorted = sorted(current_mules, key=lambda m: m.current_value)
        min_mule = mules_sorted[0]
        max_mule = mules_sorted[-1]

        current_diff = max_mule.current_value - min_mule.current_value

        for item in list(max_mule.items):
            if min_mule.current_weight + item.weight <= min_mule.capacity:

                new_max_val = max_mule.current_value - item.value
                new_min_val = min_mule.current_value + item.value

                max_mule.remove_item(item)
                min_mule.add_item(item)

                new_diff = calculate_difference(current_mules)

                if new_diff < current_diff:
                    current_diff = new_diff
                    improved = True
                    break
                else:

                    min_mule.remove_item(item)
                    max_mule.add_item(item)

        if improved:
            continue

        for item_max in list(max_mule.items):
            for item_min in list(min_mule.items):

                w_max_new = max_mule.current_weight - item_max.weight + item_min.weight

                w_min_new = min_mule.current_weight - item_min.weight + item_max.weight

                if w_max_new <= max_mule.capacity and w_min_new <= min_mule.capacity:

                    max_mule.remove_item(item_max)
                    min_mule.remove_item(item_min)
                    max_mule.add_item(item_min)
                    min_mule.add_item(item_max)

                    new_diff = calculate_difference(current_mules)

                    if new_diff < current_diff:
                        current_diff = new_diff
                        improved = True
                        break
                    else:

                        max_mule.remove_item(item_min)
                        min_mule.remove_item(item_max)
                        max_mule.add_item(item_max)
                        min_mule.add_item(item_min)
            if improved:
                break

    end_time = time.time()
    return current_mules, current_diff, end_time - start_time
