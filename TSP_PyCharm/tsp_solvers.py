import time
from tsp_methods import *


def solve_with_cut_set(costs_matrix, connected=True, visualize=True, print_time=True):
    print("Cut Set")
    num_vertices = len(costs_matrix)

    model = create_cut_set_model(costs_matrix, connected)

    start_time = time.time()
    solution = model.solve()
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_tours(solution, num_vertices, method_name="Cut Set")

    print("\tTotal Cost:   ", solution.get_objective_value())


def solve_with_subtour_elimination(costs_matrix, connected=True, visualize=True, print_time=True):
    print("Subtour Elimination")
    num_vertices = len(costs_matrix)

    model = create_subtour_elimination_model(costs_matrix, connected)

    start_time = time.time()
    solution = model.solve()
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_tours(solution, num_vertices, method_name="Subtour Elimination")

    print("\tTotal Cost:   ", solution.get_objective_value())


def solve_with_branch_and_bound(costs_matrix, bb_type, visualize=True, print_time=True):
    print("Branch and Bound")
    num_vertices = len(costs_matrix)

    start_time = time.time()
    solution = branch_and_bound(costs_matrix, bb_type)
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_tours(solution, num_vertices, method_name="Branch and Bound")

    print("\tTotal Cost:   ", solution.get_objective_value())


def solve_with_MTZ(costs_matrix, visualize=True, print_time=True):
    print("Miller–Tucker–Zemlin")
    num_vertices = len(costs_matrix)

    model = create_MTZ_model(costs_matrix)

    start_time = time.time()
    solution = model.solve()
    if print_time:
        print("\tTime:", time.time() - start_time)

    if visualize:
        utils.print_tours(solution, num_vertices, method_name="Miller–Tucker–Zemlin")

    print("\tTotal Cost:   ", solution.get_objective_value())


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
