import itertools
from docplex.mp.model import Model
import utils
from enum import Enum


def generate_basic_model(costs_matrix):
    num_vertices = len(costs_matrix)

    # Create a binary optimization model
    model = Model(name='TSP_Basic_Model')

    # Create binary variables for edges
    x = {(i, j): model.binary_var(name=f'x_{i}_{j}') for i in range(num_vertices) for j in range(num_vertices)}

    for i in range(num_vertices):
        # Ensure that every vertex has exactly one outgoing edge
        model.add_constraint(model.sum(x[i, j] for j in range(num_vertices) if j != i) == 1, ctname='out_{0}'.format(i))
        # Ensure that every vertex has exactly one incoming edge
        model.add_constraint(model.sum(x[j, i] for j in range(num_vertices) if j != i) == 1, ctname='in_{0}'.format(i))

    # Objective function
    model.minimize(
        model.sum(costs_matrix[i][j] * x[(i, j)] for i in range(num_vertices) for j in range(num_vertices) if j != i))

    return model, x


def create_cut_set_model(costs_matrix, connected):
    num_vertices = len(costs_matrix)
    model, x = generate_basic_model(costs_matrix)

    if connected:
        # Cut set constrains
        vertices_list = [v for v in range(num_vertices)]
        for subset in utils.generate_subsets(vertices_list):
            arc_list = utils.get_external_subset_acrs(subset, vertices_list)
            model.add_constraint(model.sum(x[(arc['from'], arc['to'])] for arc in arc_list) >= 1)

    return model


def create_subtour_elimination_model(costs_matrix, connected):
    num_vertices = len(costs_matrix)
    model, x = generate_basic_model(costs_matrix)

    if connected:
        # Cut set constrains
        vertices_list = [v for v in range(num_vertices)]
        for subset in utils.generate_subsets(vertices_list):
            arc_list = utils.get_internal_subset_acrs(subset, vertices_list)
            model.add_constraint(model.sum(x[(arc['from'], arc['to'])] for arc in arc_list) <= len(subset) - 1)

    return model


class BranchAndBoundType(Enum):
    BINARY = 0,
    TOTAL = 1


def branch_and_bound(costs_matrix, bb_type):
    num_vertices = len(costs_matrix)

    best_solution = None
    best_objective_value = float('inf')

    stack = [create_cut_set_model(costs_matrix, connected=False)]

    nodes_added = 0

    while stack:
        current_model = stack.pop(0)

        solution = current_model.solve()
        if solution is None:
            continue  # Infeasible solution, backtrack

        objective_value = solution.get_objective_value()

        if objective_value >= best_objective_value:
            continue  # Solution is worse than the best found so far, backtrack

        if utils.count_subtours(solution) == 1:
            # Found a feasible solution with lower objective value
            best_solution = solution
            best_objective_value = objective_value
            continue

        count_added_models = 0
        for i, j in itertools.product(range(num_vertices), repeat=2):
            current_var_value = solution.get_var_value(current_model.get_var_by_name(f'x_{i}_{j}'))
            if i != j and current_var_value == 1:
                new_model = current_model.clone()
                new_model.add_constraint(new_model.get_var_by_name(f'x_{i}_{j}') == 0)
                stack.append(new_model)

                nodes_added += 1
                count_added_models += 1
                if bb_type == BranchAndBoundType.BINARY and count_added_models == 2:
                    break

    if best_solution is None:
        raise Exception("Infeasible")

    print("Nodes added", nodes_added)

    return best_solution
