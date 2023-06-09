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


class BranchAndBoundType(Enum):
    BINARY = 0,
    TOTAL = 1


def solve_with_branch_and_bound(costs_matrix, bb_type, visualize=True, print_time=True):
    print("Branch and Bound Binary" if bb_type == BranchAndBoundType.BINARY else "Branch and Bound Total")
    num_vertices = len(costs_matrix)

    start_time = time.time()

    if bb_type == BranchAndBoundType.BINARY:
        solution = branch_and_bound_binary(costs_matrix)
    else:
        solution = branch_and_bound_total(costs_matrix)

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
