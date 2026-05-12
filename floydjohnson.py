import heapq
import time

from graph_data import graph_list, graph_matrix, V


# -------------------------------------------------------
# GRAPH REPRESENTATION
# -------------------------------------------------------
#
# Structures:
# - Adjacency List
# - Adjacency Matrix
#
# Advantages:
# - Matrix is suitable for dense graphs
# - List is memory efficient
#
# Features:
# - Supports negative edge weights
# - No negative cycles
#
# Suitable for:
# - Floyd-Warshall
# - Johnson's Algorithm
# -------------------------------------------------------


# -------------------------------------------------------
# FLOYD-WARSHALL ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Finds shortest paths between all pairs of nodes
#
# Features:
# - Dynamic Programming approach
# - Supports negative edge weights
# - Uses adjacency matrix representation
#
# -------------------------------------------------------

def floyd_warshall(graph_matrix, V):

    # Copy original matrix
    dist = [row[:] for row in graph_matrix]

    # Dynamic Programming updates
    for k in range(V):

        for i in range(V):

            for j in range(V):

                if dist[i][k] + dist[k][j] < dist[i][j]:

                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# -------------------------------------------------------
# BELLMAN-FORD SUBROUTINE
# -------------------------------------------------------
#
# Purpose:
# Computes node potentials for Johnson's Algorithm
#
# Complexity:
# Time  -> O(V * E)
# Space -> O(V)
# -------------------------------------------------------

def bellman_ford(edges, V, start):

    dist = [float('inf')] * V
    dist[start] = 0

    # Edge relaxation
    for _ in range(V - 1):

        for u, v, w in edges:

            if dist[u] != float('inf') and dist[u] + w < dist[v]:

                dist[v] = dist[u] + w

    return dist


# -------------------------------------------------------
# DIJKSTRA SUBROUTINE
# -------------------------------------------------------
#
# Purpose:
# Computes shortest paths from a source node
#
# -------------------------------------------------------

def dijkstra(graph, V, start):

    dist = [float('inf')] * V
    dist[start] = 0

    # Priority Queue
    pq = [(0, start)]

    while pq:

        d, u = heapq.heappop(pq)

        if d > dist[u]:

            continue

        # Relax adjacent edges
        for v, w in graph[u]:

            if dist[u] + w < dist[v]:

                dist[v] = dist[u] + w

                heapq.heappush(pq, (dist[v], v))

    return dist


# -------------------------------------------------------
# JOHNSON'S ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Finds shortest paths between all pairs of nodes
#
# Features:
# - Combines Bellman-Ford and Dijkstra
# - Efficient for sparse graphs
#
# -------------------------------------------------------

def johnsons_algorithm(graph_list, V):

    edges = []

    # Build edge list
    for u in range(V):

        for v, w in graph_list[u]:

            edges.append((u, v, w))

        # Additional source node
        edges.append((V, u, 0))

    # Compute node potentials
    h = bellman_ford(edges, V + 1, V)

    # Reweight graph
    reweighted_graph = {i: [] for i in range(V)}

    for u in range(V):

        for v, w in graph_list[u]:

            reweighted_graph[u].append(
                (v, w + h[u] - h[v])
            )

    # Run Dijkstra for each node
    apsp_distances = []

    for u in range(V):

        dijkstra_dist = dijkstra(reweighted_graph, V, u)

        original_dist = [

            dijkstra_dist[v] + h[v] - h[u]

            if dijkstra_dist[v] != float('inf')

            else float('inf')

            for v in range(V)
        ]

        apsp_distances.append(original_dist)

    return apsp_distances


# -------------------------------------------------------
# FLOYD-WARSHALL EXECUTION
# -------------------------------------------------------

print("=================================================")
print("FLOYD-WARSHALL RESULTS")
print("=================================================\n")

start = time.perf_counter()

floyd_result = floyd_warshall(
    graph_matrix,
    V
)

fw_time = time.perf_counter() - start


# -------------------------------------------------------
# FLOYD-WARSHALL OUTPUT
# -------------------------------------------------------

for row in floyd_result:

    print(row)

print(f"\nRuntime: {fw_time:.8f} seconds")


# -------------------------------------------------------
# JOHNSON EXECUTION
# -------------------------------------------------------

print("\n=================================================")
print("JOHNSON'S ALGORITHM RESULTS")
print("=================================================\n")

start = time.perf_counter()

johnson_result = johnsons_algorithm(
    graph_list,
    V
)

j_time = time.perf_counter() - start


# -------------------------------------------------------
# JOHNSON OUTPUT
# -------------------------------------------------------

for row in johnson_result:

    print(row)

print(f"\nRuntime: {j_time:.8f} seconds")


# -------------------------------------------------------
# RUNTIME COMPARISON
# -------------------------------------------------------

print("\n=================================================")
print("RUNTIME COMPARISON")
print("=================================================\n")

print(f"Floyd-Warshall Runtime : {fw_time:.8f} seconds")
print(f"Johnson Runtime        : {j_time:.8f} seconds")