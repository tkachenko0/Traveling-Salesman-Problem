from tsp_solvers import *
from tsp_solvers import BranchAndBoundType
from costs_matrices import generate_random_cost_matrix, generate_space_matrix, get_test_cost_matrices
import json


def comparison():
    num_vertices = 30

    data = {}

    for n_instance in range(30):
        print("Instance", n_instance)
        costs_matrix = generate_random_cost_matrix(num_vertices)
        obj_value = solve_with_max_flow_v2(costs_matrix, visualize=False, print_time=True)

        data[n_instance] = {
            "obj_value": obj_value,
            "costs_matrix": costs_matrix
        }

    with open("data.json", "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    #num_vertices = 8

    #costs_matrix = generate_space_matrix(num_vertices)
    #costs_matrix = generate_space_matrix()

    #solve_with_cut_set(costs_matrix, visualize=True, print_time=True)

    #solve_with_subtour_elimination(costs_matrix, visualize=False, print_time=True)

    #solve_with_MTZ(costs_matrix, visualize=False, print_time=True)

    #solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.TOTAL, visualize=False, print_time=True)
    #solve_with_branch_and_bound(costs_matrix, bb_type=BranchAndBoundType.BINARY, visualize=False, print_time=True)

    #solve_with_max_flow_v1(costs_matrix, visualize=True, print_time=True)
    #solve_with_max_flow_v2(costs_matrix, visualize=False, print_time=True)

    comparison()