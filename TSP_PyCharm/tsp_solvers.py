import time
from tsp_methods import *


def solve_with_cut_set(costs_matrix, connected=True, visualize=True, print_time=True):
    print("Cut Set")

    model = create_cut_set_model(costs_matrix, connected)

    start_time = time.time()
    solution = model.solve()
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_results(solution, method_name="Cut Set")


def solve_with_subtour_elimination(costs_matrix, connected=True, visualize=True, print_time=True):
    print("Subtour Elimination")

    model = create_subtour_elimination_model(costs_matrix, connected)

    start_time = time.time()
    solution = model.solve()
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_results(solution, method_name="Subtour Elimination")


def solve_with_branch_and_bound(costs_matrix, bb_type, visualize=True, print_time=True):
    print("Branch and Bound")

    start_time = time.time()
    solution = branch_and_bound(costs_matrix, bb_type)
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_results(solution, method_name="Branch and Bound")


def solve_with_brute_force(cost_matrix, print_time=True):
    print("Brute Force")

    start_time = time.time()

    n_vertices = len(cost_matrix)
    best_path = None
    best_cost = float('inf')

    # Generate all possible permutations of vertices
    permutations = itertools.permutations(range(n_vertices))

    # Iterate through each permutation
    for permutation in permutations:
        current_cost = 0

        # Calculate the cost of the current permutation
        for i in range(n_vertices - 1):
            current_cost += cost_matrix[permutation[i]][permutation[i + 1]]

        current_cost += cost_matrix[permutation[n_vertices - 1]][permutation[0]]

        # Check if the current permutation gives a better cost
        if current_cost < best_cost:
            best_path = permutation
            best_cost = current_cost

    if print_time:
        print("\tTime:", time.time() - start_time)

    print("\tTotal Cost:   ", best_cost)

    return best_path, best_cost
