from tsp_solvers import *
from tsp_solvers import BranchAndBoundType
from costs_matrices import generate_random_cost_matrix, generate_space_matrix, get_test_cost_matrices

if __name__ == '__main__':
    num_vertices = 10

    costs_matrix = generate_random_cost_matrix(num_vertices)

    # Cut Set formulation
    solve_with_cut_set(costs_matrix, connected=False, visualize=True, print_time=True)

    # SUbtour Elimination formulazion
    solve_with_subtour_elimination(costs_matrix, connected=True, visualize=False, print_time=True)

    # Branch and Bound in two versions
    solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.TOTAL, visualize=True, print_time=True)
    solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.BINARY, visualize=True, print_time=True)

    # Miller–Tucker–Zemlin formulation
    solve_with_MTZ(costs_matrix, visualize=True, print_time=True)
