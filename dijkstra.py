from collections import defaultdict
import heapq
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

class Graph:

    def __init__(self):

        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)

    def add_edge(self, u, v, w):

        # Forward edge
        self.graph[u].append((v, w))

        # Reverse edge for Bidirectional Dijkstra
        self.reverse_graph[v].append((u, w))


# -------------------------------------------------------
# STANDARD DIJKSTRA ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Finds shortest paths from a source node
# to all other nodes
#
# Features:
# - Greedy shortest path strategy
# - Uses Priority Queue (Min Heap)
# - Requires non-negative edge weights
#
# Complexity:
# Time  -> O((V + E) log V)
# Space -> O(V + E)
# -------------------------------------------------------

def dijkstra(graph, start):

    # Initialize distances
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0

    # Min Heap
    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip outdated paths
        if current_distance > distances[current_node]:
            continue

        # Relax adjacent edges
        for neighbor, weight in graph[current_node]:

            distance = current_distance + weight

            if distance < distances[neighbor]:

                distances[neighbor] = distance

                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


# -------------------------------------------------------
# BIDIRECTIONAL DIJKSTRA ALGORITHM
# -------------------------------------------------------
#
# Purpose:
# Finds shortest path between source and target
#
# Features:
# - Simultaneous forward and backward search
# - Reduced search space
# - Faster practical performance
#
# Complexity:
# Worst Case Time  -> O((V + E) log V)
# Space            -> O(V + E)
# -------------------------------------------------------

def bidirectional_dijkstra(graph, reverse_graph, start, target):

    # Distance arrays
    forward_dist = defaultdict(lambda: float('inf'))
    backward_dist = defaultdict(lambda: float('inf'))

    forward_dist[start] = 0
    backward_dist[target] = 0

    # Priority queues
    forward_pq = [(0, start)]
    backward_pq = [(0, target)]

    # Visited nodes
    forward_visited = set()
    backward_visited = set()

    best_distance = float('inf')

    while forward_pq and backward_pq:

       
        # FORWARD SEARCH
       
        current_forward_dist, current_forward_node = heapq.heappop(forward_pq)

        if current_forward_node not in forward_visited:

            forward_visited.add(current_forward_node)

            # Relax adjacent edges
            for neighbor, weight in graph[current_forward_node]:

                distance = current_forward_dist + weight

                if distance < forward_dist[neighbor]:

                    forward_dist[neighbor] = distance

                    heapq.heappush(forward_pq, (distance, neighbor))


        # BACKWARD SEARCH
        
        current_backward_dist, current_backward_node = heapq.heappop(backward_pq)

        if current_backward_node not in backward_visited:

            backward_visited.add(current_backward_node)

            # Relax reverse edges
            for neighbor, weight in reverse_graph[current_backward_node]:

                distance = current_backward_dist + weight

                if distance < backward_dist[neighbor]:

                    backward_dist[neighbor] = distance

                    heapq.heappush(backward_pq, (distance, neighbor))

       
        # MEETING POINT

        common_nodes = forward_visited.intersection(backward_visited)

        if common_nodes:

            for node in common_nodes:

                total_distance = (
                    forward_dist[node] +
                    backward_dist[node]
                )

                best_distance = min(best_distance, total_distance)

    return best_distance



# TEST GRAPH

g = Graph()

graph_data = {

    "nodes": ["A", "B", "C", "D", "E", "F"],

    "edges": [

        {"from": "A", "to": "B", "weight": 4},
        {"from": "A", "to": "C", "weight": 2},
        {"from": "B", "to": "C", "weight": 5},
        {"from": "B", "to": "D", "weight": 10},
        {"from": "C", "to": "D", "weight": 3},
        {"from": "D", "to": "E", "weight": 2},
        {"from": "E", "to": "F", "weight": 5},
        {"from": "A", "to": "E", "weight": 15}

    ]
}

# Build graph
for edge in graph_data["edges"]:

    u = edge["from"]
    v = edge["to"]
    w = edge["weight"]

    g.add_edge(u, v, w)



# STANDARD DIJKSTRA EXECUTION

start_time = time.perf_counter()

dijkstra_result = dijkstra(g.graph, 'A')

end_time = time.perf_counter()

dijkstra_runtime = end_time - start_time



# STANDARD DIJKSTRA OUTPUT


print(dict(dijkstra_result))

print(f"\nRuntime: {dijkstra_runtime:.8f} seconds")



# BIDIRECTIONAL DIJKSTRA EXECUTION

start_time = time.perf_counter()

bidirectional_result = bidirectional_dijkstra(
    g.graph,
    g.reverse_graph,
    'A',
    'F'
)

end_time = time.perf_counter()

bidirectional_runtime = end_time - start_time



# BIDIRECTIONAL DIJKSTRA OUTPUT

print(f"Shortest distance from A to F: {bidirectional_result}")

print(f"\nRuntime: {bidirectional_runtime:.8f} seconds")