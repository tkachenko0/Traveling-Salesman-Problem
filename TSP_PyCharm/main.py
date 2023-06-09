from tsp_solvers import *
import utils
from tsp_solvers import BranchAndBoundType
from costs_matrices import generate_random_cost_matrix, generate_space_matrix, get_test_cost_matrices


def bb_total_vs_binary():
    costs_matrices = get_test_cost_matrices()

    for i, cm in enumerate(costs_matrices):
        print(f"Id: {i+1}")
        t1, num_added_nodes1, sol_value1 = solve_with_branch_and_bound(cm,
                                                                       bb_type=BranchAndBoundType.TOTAL)
        t2, num_added_nodes2, sol_value2 = solve_with_branch_and_bound(cm,
                                                                       bb_type=BranchAndBoundType.BINARY)

        increase_perc = round((100 * (sol_value2 - sol_value1) / sol_value1), 2)
        print(
            f"{i+1} & {t1} & {num_added_nodes1} & {sol_value1} & {t2} & {num_added_nodes2} & {sol_value2} & {increase_perc} \% \\\\")

def test_mtz_time():
    costs_matrices = get_test_cost_matrices()

    for i, cm in enumerate(costs_matrices):
        t = solve_with_MTZ(cm, visualize=False, print_time=False)
        print(f"Id {i+1}: {t}")



if __name__ == '__main__':
    num_vertices = 15

    # costs_matrix = generate_random_cost_matrix(num_vertices)

    # costs_matrix = generate_space_matrix()

    # solve_with_cut_set(costs_matrix, connected=True, visualize=False, print_time=True)
    # solve_with_subtour_elimination(costs_matrix, connected=True, visualize=False, print_time=True)
    # solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.TOTAL, visualize=False, print_time=True)
    # solve_with_MTZ(costs_matrix, visualize=False, print_time=True)

    # bb_total_vs_binary()
    test_mtz_time()
