# A recursive function used by longestPath. See below
# link for details
# https:#www.geeksforgeeks.org/topological-sorting/

from itertools import chain

def get_sorted_graph(graph):
    sorted_graph = []
    visited = [False for _ in range(len(graph))]

    def topological_sort(v_index):
        nonlocal visited
        nonlocal sorted_graph

        if visited[v_index]: return
        visited[v_index] = True

        for adj, _dist in graph[v_index]:
            topological_sort(adj)

        sorted_graph.append(graph[v_index])

    for v_index in range(len(graph)):
        topological_sort(v_index)
    return sorted_graph

def longest_path(start_index, graph):
    inf = 10 ** 9
    distances = [-inf for i in range(len(graph))]
    graph = get_sorted_graph(graph)
    distances[start_index] = 0

    for i, adjs in list(enumerate(graph))[::-1]:
        if distances[i] != inf:
            for adj_index, adj_dist in adjs:
                distances[adj_index] = max(distances[adj_index], distances[i] + adj_dist)

    return ['INF' if dist == -inf else str(dist) for dist in distances]

if __name__ == '__main__':
    graph = [
        [(1, 5), (2, 3)],
        [(3, 6), (2, 2)],
        [(4, 4), (5, 2), (3, 7)],
        [(5, 1), (4, -1)],
        [(5, -2)],
        []
    ]

    start_index = 1
    print(f"Following are longest distances from source vertex index {start_index}")
    print(' '.join(longest_path(start_index, graph)))
