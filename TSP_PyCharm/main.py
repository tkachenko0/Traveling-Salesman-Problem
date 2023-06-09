from tsp_solvers import *
import utils
from tsp_solvers import BranchAndBoundType

if __name__ == '__main__':
    num_vertices = 15

    costs_matrix = utils.generate_random_cost_matrix(num_vertices)

    # costs_matrix = utils.generate_space_matrix()

    # solve_with_cut_set(costs_matrix, connected=True, visualize=False, print_time=True)
    # solve_with_subtour_elimination(costs_matrix, connected=True, visualize=False, print_time=True)
    solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.TOTAL, visualize=False, print_time=True)
    solve_with_MTZ(costs_matrix, visualize=False, print_time=True)