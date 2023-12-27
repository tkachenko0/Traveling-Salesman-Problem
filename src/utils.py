import matplotlib.pyplot as plt
import itertools
import math

NUM_PLANETS = 8


def generate_subsets(set_list):
    """
    Generate all subsets of a set excluding the empty set
    """
    subsets = []
    for r in range(1, len(set_list)):
        subsets.extend(itertools.combinations(set_list, r))
    return subsets


def get_internal_subset_arcs(subset, vertices_list):
    """
    Generates form a subset S of vertices a set of arcs that start from a vertex
    of the subset an ends on a vertex of N \ S
    """
    arc_list = []
    for v in subset:
        for q in vertices_list:
            if q in subset:
                arc_list.append({'from': v, 'to': q})
    return arc_list


def get_external_subset_arcs(subset, vertices_list):
    """
    Generates form a subset S of vertices a set of arcs that start from a vertex
    of the subset an ends on a vertex of N \ S
    """
    arc_list = []
    for v in subset:
        for q in vertices_list:
            if q not in subset:
                arc_list.append({'from': v, 'to': q})
    return arc_list


def extract_subtours(solution, num_vertices):
    visited = [False] * num_vertices
    tours = []

    while True:
        curr_vertex = next((i for i, v in enumerate(visited) if not v), -1)
        if curr_vertex == -1:
            break
        tour = [curr_vertex]

        while True:
            visited[curr_vertex] = True
            next_vertex = [j for j in range(num_vertices) if
                           j != curr_vertex and solution.get_value(f'x_{curr_vertex}_{j}') == 1][0]
            tour.append(next_vertex)
            curr_vertex = next_vertex
            if curr_vertex == tour[0]:
                break

        tours.append(tour)

    return tours


def count_subtours(solution, num_vertices):
    num_vertices = solution.size
    visited = [False] * num_vertices
    count = 0

    while True:
        curr_vertex = next((i for i, v in enumerate(visited) if not v), -1)
        if curr_vertex == -1:
            break
        first_vertex = curr_vertex

        while True:
            visited[curr_vertex] = True
            next_vertex = [j for j in range(num_vertices) if
                           j != curr_vertex and solution.get_value(f'x_{curr_vertex}_{j}') == 1][0]
            curr_vertex = next_vertex
            if curr_vertex == first_vertex:
                break

        count += 1

    return count


def plot_subtours(num_vertices, tours, method_name):
    plt.figure()

    radius = 0.5
    center_x = 0.5
    center_y = 0.5
    angle = 2 * math.pi / num_vertices
    vertices_x = [center_x + radius * math.cos(i * angle) for i in range(num_vertices)]
    vertices_y = [center_y + radius * math.sin(i * angle) for i in range(num_vertices)]

    plt.scatter(vertices_x, vertices_y, color='blue', s=50)

    colors = ['red', 'green', 'orange', 'purple']

    for idx, tour in enumerate(tours):
        color = colors[idx % len(colors)]
        for i in range(len(tour) - 1):
            plt.arrow(
                vertices_x[tour[i]], vertices_y[tour[i]],
                vertices_x[tour[i + 1]] - vertices_x[tour[i]], vertices_y[tour[i + 1]] - vertices_y[tour[i]],
                color=color, width=0.005, length_includes_head=True, alpha=0.5
            )
        plt.arrow(
            vertices_x[tour[-1]], vertices_y[tour[-1]],
            vertices_x[tour[0]] - vertices_x[tour[-1]], vertices_y[tour[0]] - vertices_y[tour[-1]],
            color=color, width=0.005, length_includes_head=True, alpha=0.5
        )

    label_offset = 0.02
    for i in range(num_vertices):
        vertex_name = str(i)
        if num_vertices == NUM_PLANETS:
            vertex_name = planet_names[i]
        plt.annotate(vertex_name, (vertices_x[i] + label_offset, vertices_y[i] + label_offset), color='black',
                     ha='center',
                     va='center', fontsize=12)

    plt.axis('off')
    plt.title(method_name)
    plt.show()


def print_tours(solution, num_vertices, method_name):
    if solution is None:
        raise Exception("Infeasible")

    tours = extract_subtours(solution, num_vertices)
    plot_subtours(num_vertices, tours, method_name)
    print(f"\tNumber of tours: {len(tours)}")

    print("\tTSP tours:")
    for tour in tours:
        print("\t", tour, sep="")