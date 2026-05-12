from collections import defaultdict
import time


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
    dist[start] = 0

    # Relax edges in topological order
    for u in order:

        if dist[u] != float('inf'):

            for v, w in graph[u]:

                if dist[u] + w < dist[v]:

                    dist[v] = dist[u] + w

    return dist


# =========================================================
# TEST GRAPH


V = 6

graph = defaultdict(list)

graph[0].append((1, 5))
graph[0].append((2, 3))

graph[1].append((3, 6))
graph[1].append((2, 2))

graph[2].append((4, 4))
graph[2].append((5, 2))
graph[2].append((3, 7))

graph[3].append((4, -1))

graph[4].append((5, -2))



# EXECUTION

start_node = 1

start_time = time.perf_counter()

distances = dag_shortest_path(graph, V, start_node)

end_time = time.perf_counter()



# OUTPUT

for i in range(V):

    print(f"Distance from node {start_node} to node {i}: {distances[i]}")

print(f"\nRuntime: {end_time - start_time:.8f} seconds")