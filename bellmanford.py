from collections import deque
import time

from graph_data import graph, nodes, source_node


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
# - Fast neighbor traversal
#
# Contains:
# - Negative edge
# - No negative cycle
#
# Suitable for:
# - Bellman-Ford
# - SPFA
# -------------------------------------------------------


# -------------------------------------------------------
# BELLMAN-FORD ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Finds shortest paths from a source node
#
# Features:
# - Supports negative edge weights
# - Detects negative cycles
#
# Complexity:
# Time  -> O(V * E)
# Space -> O(V)
# -------------------------------------------------------

def bellman_ford(graph, nodes, source):

    distance = {}
    previous = {}

    # Initialize distances
    for node in nodes:

        distance[node] = float('inf')
        previous[node] = None

    distance[source] = 0

    # Edge relaxation
    for i in range(len(nodes) - 1):

        for u in graph:

            for v, w in graph[u]:

                if distance[u] != float('inf') and distance[u] + w < distance[v]:

                    distance[v] = distance[u] + w
                    previous[v] = u

    # Negative cycle detection
    for u in graph:

        for v, w in graph[u]:

            if distance[u] != float('inf') and distance[u] + w < distance[v]:

                print("Negative weight cycle detected")
                return None, None

    return distance, previous


# -------------------------------------------------------
# SPFA ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Optimized version of Bellman-Ford
#
# Features:
# - Queue-based relaxation
# - Faster practical performance
# - Supports negative edge weights
#
# Complexity:
# Average Case -> Faster than Bellman-Ford
# Worst Case   -> O(V * E)
# -------------------------------------------------------

def spfa(graph, nodes, source):

    distance = {node: float('inf') for node in nodes}
    previous = {node: None for node in nodes}

    distance[source] = 0

    # Queue initialization
    queue = deque([source])

    in_queue = {node: False for node in nodes}
    in_queue[source] = True

    while queue:

        u = queue.popleft()
        in_queue[u] = False

        # Relax adjacent edges
        for v, w in graph[u]:

            if distance[u] != float('inf') and distance[u] + w < distance[v]:

                distance[v] = distance[u] + w
                previous[v] = u

                if not in_queue[v]:

                    queue.append(v)
                    in_queue[v] = True

    return distance, previous


# -------------------------------------------------------
# PATH RECONSTRUCTION
# -------------------------------------------------------

def get_path(previous, node):

    path = []

    while node is not None:

        path.append(node)
        node = previous[node]

    path.reverse()

    return path


# -------------------------------------------------------
# BELLMAN-FORD EXECUTION
# -------------------------------------------------------

print("\n==============================")
print("BELLMAN-FORD RESULTS")
print("==============================")

start_time = time.perf_counter()

bf_distance, bf_previous = bellman_ford(graph, nodes, source_node)

end_time = time.perf_counter()

bf_runtime = end_time - start_time


# -------------------------------------------------------
# BELLMAN-FORD OUTPUT
# -------------------------------------------------------

if bf_distance is not None:

    print("\nDistances:")
    print(bf_distance)

    print("\nPaths:")

    for node in nodes:

        print(
            node,
            ":",
            get_path(bf_previous, node),
            "| Cost:",
            bf_distance[node]
        )

    print(f"\nRuntime: {bf_runtime:.8f} seconds")


# -------------------------------------------------------
# SPFA EXECUTION
# -------------------------------------------------------

print("\n==============================")
print("SPFA RESULTS")
print("==============================")

start_time = time.perf_counter()

spfa_distance, spfa_previous = spfa(graph, nodes, source_node)

end_time = time.perf_counter()

spfa_runtime = end_time - start_time


# -------------------------------------------------------
# SPFA OUTPUT
# -------------------------------------------------------

print("\nDistances:")
print(spfa_distance)

print("\nPaths:")

for node in nodes:

    print(
        node,
        ":",
        get_path(spfa_previous, node),
        "| Cost:",
        spfa_distance[node]
    )

print(f"\nRuntime: {spfa_runtime:.8f} seconds")


# -------------------------------------------------------
# RUNTIME COMPARISON
# -------------------------------------------------------

print("\n==============================")
print("RUNTIME COMPARISON")
print("==============================")

print(f"Bellman-Ford Runtime : {bf_runtime:.8f} seconds")
print(f"SPFA Runtime         : {spfa_runtime:.8f} seconds")