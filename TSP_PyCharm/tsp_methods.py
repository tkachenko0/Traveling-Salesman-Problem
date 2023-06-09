import itertools
from docplex.mp.model import Model
import utils
from enum import Enum
import heapq

def create_assignment_problem_model(costs_matrix):
    num_vertices = len(costs_matrix)

    # Create a binary optimization model
    model = Model(name='TSP_AP')

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


def create_MTZ_model(costs_matrix):
    num_vertices = len(costs_matrix)

    model, x = create_assignment_problem_model(costs_matrix)

    # Create variables for ordering of vertices
    u = [model.continuous_var(name=f'u_{i}') for i in range(num_vertices)]
    for i in range(1, num_vertices):
        model.add_constraint(u[i] >= 0, ctname=f'lower_bound_{i}')
        model.add_constraint(u[i] <= num_vertices - 1, ctname=f'upper_bound_{i}')

    # Ensure that there are no subtours
    for i in range(1, num_vertices):
        for j in range(1, num_vertices):
            if i != j:
                model.add_constraint(u[i] - u[j] + (num_vertices - 1) * x[i, j] <= num_vertices - 2,
                                     ctname=f'MTZ_{i}_{j}')

    return model


def create_cut_set_model(costs_matrix, connected):
    num_vertices = len(costs_matrix)
    model, x = create_assignment_problem_model(costs_matrix)

    if connected:
        # Cut set constrains
        vertices_list = [v for v in range(num_vertices)]
        for subset in utils.generate_subsets(vertices_list):
            arc_list = utils.get_external_subset_acrs(subset, vertices_list)
            model.add_constraint(model.sum(x[(arc['from'], arc['to'])] for arc in arc_list) >= 1)

    return model


def create_subtour_elimination_model(costs_matrix, connected):
    num_vertices = len(costs_matrix)
    model, x = create_assignment_problem_model(costs_matrix)

    if connected:
        # Cut set constrains
        vertices_list = [v for v in range(num_vertices)]
        for subset in utils.generate_subsets(vertices_list):
            arc_list = utils.get_internal_subset_acrs(subset, vertices_list)
            model.add_constraint(model.sum(x[(arc['from'], arc['to'])] for arc in arc_list) <= len(subset) - 1)

    return model


def branch_and_bound_total(costs_matrix):
    num_vertices = len(costs_matrix)

    best_solution = None
    best_objective_value = float('inf')

    initial_model, x = create_assignment_problem_model(costs_matrix)

    stack = [initial_model]

    nodes_added = 0

    while stack:
        current_model = stack.pop(0)

        solution = current_model.solve()
        if solution is None:
            continue  # Infeasible solution, backtrack

        objective_value = solution.get_objective_value()

        if objective_value >= best_objective_value:
            continue  # Solution is worse than the best found so far, backtrack

        if utils.count_subtours(solution, num_vertices) == 1:
            # Found a feasible solution with lower objective value
            best_solution = solution
            best_objective_value = objective_value
            continue

        for i, j in itertools.product(range(num_vertices), repeat=2):
            current_var_value = solution.get_var_value(current_model.get_var_by_name(f'x_{i}_{j}'))
            if i != j and current_var_value == 1:
                new_model = current_model.clone()
                new_model.add_constraint(new_model.get_var_by_name(f'x_{i}_{j}') == 0)
                stack.append(new_model)
                nodes_added += 1

    if best_solution is None:
        raise Exception("Infeasible")

    print("\tNodes added:", nodes_added)

    return best_solution


def branch_and_bound_binary(costs_matrix):
    num_vertices = len(costs_matrix)

    best_solution = None
    best_objective_value = float('inf')

    initial_model, x = create_assignment_problem_model(costs_matrix)

    stack = [initial_model]

    nodes_added = 0

    while stack:
        current_model = stack.pop(0)

        solution = current_model.solve()
        if solution is None:
            continue  # Infeasible solution, backtrack

        objective_value = solution.get_objective_value()

        if objective_value >= best_objective_value:
            continue  # Solution is worse than the best found so far, backtrack

        if utils.count_subtours(solution, num_vertices) == 1:
            # Found a feasible solution with lower objective value
            best_solution = solution
            best_objective_value = objective_value
            continue

        # select the most expensive arcs of the current solution
        max_heap = []
        for var_name, var_value in solution.iter_var_values():
            var_name = str(var_name)
            if var_value == 1:
                i, j = map(int, var_name.split('_')[1:])
                current_cost = costs_matrix[i][j]
                heapq.heappush(max_heap, (-current_cost, i, j))

        # Get the indices of the two most expensive variables
        (_, i1, j1) = heapq.heappop(max_heap)
        (_, i2, j2) = heapq.heappop(max_heap)

        left_child = current_model.clone()
        left_child.add_constraint(left_child.get_var_by_name(f'x_{i1}_{j1}') == 0)
        stack.append(left_child)

        right_child = current_model.clone()
        right_child.add_constraint(right_child.get_var_by_name(f'x_{i2}_{j2}') == 0)
        stack.append(right_child)

        nodes_added += 2

    if best_solution is None:
        raise Exception("Infeasible")

    print("\tNodes added:", nodes_added)

    return best_solution
