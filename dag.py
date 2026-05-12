import time

from graph_data import graph_list, V


# -------------------------------------------------------
# GRAPH REPRESENTATION
# -------------------------------------------------------
#
# Structure:
# Adjacency List
#
# Advantages:
# - Memory efficient
# - Suitable for sparse graphs
# - Fast edge traversal
#
# Features:
# - Directed graph
# - No cycles
# - Supports negative edge weights
#
# Suitable for:
# - DAG Shortest Path
# - Topological Sorting
# -------------------------------------------------------


# -------------------------------------------------------
# TOPOLOGICAL SORT
# -------------------------------------------------------
#
# Purpose:
# Produces a valid processing order for DAG nodes
#
# Technique:
# Depth-First Search (DFS)
# -------------------------------------------------------

def topological_sort(graph, V):

    visited = [False] * V
    stack = []

    def dfs(node):

        visited[node] = True

        # Visit adjacent nodes
        for neighbor, weight in graph[node]:

            if not visited[neighbor]:
                dfs(neighbor)

        # Store node in topological order
        stack.append(node)

    for i in range(V):

        if not visited[i]:
            dfs(i)

    stack.reverse()

    return stack


# -------------------------------------------------------
# DAG SHORTEST PATH ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Finds shortest paths in a Directed Acyclic Graph (DAG)
#
# Features:
# - Uses Topological Sorting
# - Supports negative edge weights
# - Requires acyclic graph structure
#
# Complexity:
# Time  -> O(V + E)
# Space -> O(V + E)
# -------------------------------------------------------

def dag_shortest_path(graph, V, start):

    # Generate topological order
    order = topological_sort(graph, V)

    # Initialize distances
    dist = [float('inf')] * V
    previous = [None] * V

    dist[start] = 0

    # Relax edges in topological order
    for u in order:

        if dist[u] != float('inf'):

            for v, w in graph[u]:

                if dist[u] + w < dist[v]:

                    dist[v] = dist[u] + w
                    previous[v] = u

    return dist, previous


# -------------------------------------------------------
# PATH RECONSTRUCTION
# -------------------------------------------------------

def get_path(previous, target):

    path = []

    while target is not None:

        path.append(target)
        target = previous[target]

    path.reverse()

    return path


# -------------------------------------------------------
# EXECUTION
# -------------------------------------------------------

start_node = 0

print("\n==============================")
print("DAG SHORTEST PATH RESULTS")
print("==============================")

start_time = time.perf_counter()

distances, previous = dag_shortest_path(
    graph_list,
    V,
    start_node
)

end_time = time.perf_counter()

runtime = end_time - start_time


# -------------------------------------------------------
# OUTPUT
# -------------------------------------------------------

print("\nDistances:")

for i in range(V):

    print(f"Node {i}: {distances[i]}")

print("\nPaths:")

for i in range(V):

    print(
        f"{start_node} -> {i}:",
        get_path(previous, i),
        "| Cost:",
        distances[i]
    )

print(f"\nRuntime: {runtime:.8f} seconds")