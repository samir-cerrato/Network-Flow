from collections import deque

def is_valid_molecule(grid):
    r, c = len(grid), len(grid[0])
    valences = {'H': 1, 'O': 2, 'N': 3, 'C': 4, '.': 0}
    graph = [[] for _ in range(r * c + 2)]
    source = r * c
    sink = r * c + 1
    total_valence = 0
    
    for i in range(r):
        for j in range(c):
            node = i * c + j
            total_valence += valences[grid[i][j]]
            
            if (i + j) % 2 == 0:
                graph[source].append((node, valences[grid[i][j]]))
                
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < r and 0 <= nj < c:
                        neighbor = ni * c + nj
                        graph[node].append((neighbor, 1))
            else:
                graph[node].append((sink, valences[grid[i][j]]))

    
    flow = 0
    while True:
        parent = [-1] * (r * c + 2)
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v, capacity in graph[u]:
                if parent[v] == -1 and capacity > 0:
                    parent[v] = u
                    queue.append(v)
        
        if parent[sink] == -1:
            break
        
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            for neighbor, capacity in graph[u]:
                if neighbor == v:
                    path_flow = min(path_flow, capacity)
            v = u
        
        flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            for i in range(len(graph[u])):
                if graph[u][i][0] == v:
                    graph[u][i] = (v, graph[u][i][1] - path_flow)
            found = False
            for i in range(len(graph[v])):
                if graph[v][i][0] == u:
                    graph[v][i] = (u, graph[v][i][1] + path_flow)
                    found = True
                    break
            if not found:
                graph[v].append((u, path_flow))
            v = u
    
    return flow == total_valence / 2

# Read input
r, c = map(int, input().split())
grid = [list(input()) for _ in range(r)]

# Check if the grid represents a valid molecule
if is_valid_molecule(grid):
    print("Valid")
else:
    print("Invalid")

