from tsp_solvers import *
import utils
from tsp_methods import BranchAndBoundType

if __name__ == '__main__':
    num_vertices = 30

    costs_matrix = utils.generate_random_cost_matrix(num_vertices)

    # costs_matrix = utils.generate_space_matrix()

    # soluzione troppo alta per il bb binario
    # costs_matrix = [[0, 70, 27, 11, 55, 58, 31, 78], [60, 0, 1, 57, 97, 85, 99, 47], [29, 35, 0, 96, 92, 47, 100, 9], [46, 15, 39, 0, 70, 9, 50, 69], [92, 63, 20, 7, 0, 87, 37, 1], [35, 96, 66, 37, 42, 0, 63, 33], [3, 71, 91, 78, 6, 27, 0, 99], [90, 33, 45, 97, 79, 61, 65, 0]]

    # solve_with_cut_set(costs_matrix, connected=False, visualize=False, print_time=True)
    # solve_with_subtour_elimination(costs_matrix, connected=True, visualize=False, print_time=True)
    # solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.BINARY, visualize=False, print_time=True)
    # solve_with_brute_force(costs_matrix, print_time=True)
    solve_with_MTZ(costs_matrix, visualize=False, print_time=True)