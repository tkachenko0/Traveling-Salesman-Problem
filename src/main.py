from tsp_solvers import *
from tsp_solvers import BranchAndBoundType
from costs_matrices import generate_random_cost_matrix, generate_space_matrix, get_test_cost_matrices

if __name__ == '__main__':
    num_vertices = 6

    costs_matrix = generate_random_cost_matrix(num_vertices)

    solve_with_cut_set(costs_matrix, visualize=True, print_time=False)

    #solve_with_subtour_elimination(costs_matrix, visualize=False, print_time=True)

    #solve_with_MTZ(costs_matrix, visualize=False, print_time=True)

    #solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.TOTAL, visualize=False, print_time=True)
    #solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.BINARY, visualize=False, print_time=True)

    solve_with_max_flow(costs_matrix, visualize=True, print_time=False)