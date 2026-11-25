"""
Proyecto Final: Análisis de Algoritmos y Estrategias de Programación (COMP1303A)
Caso 01: Resolvedor de Laberintos
Implementación y comparación de algoritmos: BFS, DFS/Backtracking y A*
"""

import time
import tracemalloc
import heapq
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

class Maze:
    def __init__(self, grid, start=None, end=None):
        self.grid = [list(row) for row in grid]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = start or (1, 1)
        self.end = end or (self.rows - 2, self.cols - 2)
        # Asegurar start y end libres
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.end[0]][self.end[1]] = 'E'

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != '#'

    def get_neighbors(self, r, c):
        # Arriba, Derecha, Abajo, Izquierda
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                yield nr, nc

    @staticmethod
    def generate(rows, cols, seed=42):
        """Genera un laberinto mediante DFS con retroceso (árbol generador)"""
        if rows % 2 == 0: rows += 1
        if cols % 2 == 0: cols += 1
        import random
        rng = random.Random(seed)
        grid = [['#' for _ in range(cols)] for _ in range(rows)]
        
        stack = [(1, 1)]
        grid[1][1] = '.'
        
        while stack:
            cr, cc = stack[-1]
            neighbors = []
            for dr, dc in [(-2, 0), (0, 2), (2, 0), (0, -2)]:
                nr, nc = cr + dr, cc + dc
                if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and grid[nr][nc] == '#':
                    neighbors.append((nr, nc, cr + dr // 2, cc + dc // 2))
            
            if neighbors:
                nr, nc, mr, mc = rng.choice(neighbors)
                grid[mr][mc] = '.'
                grid[nr][nc] = '.'
                stack.append((nr, nc))
            else:
                stack.pop()
                
        grid[1][1] = 'S'
        grid[rows - 2][cols - 2] = 'E'
        return Maze(grid, (1, 1), (rows - 2, cols - 2))

def solve_bfs(maze):
    start_time = time.perf_counter()
    tracemalloc.start()
    
    queue = deque([maze.start])
    parent = {maze.start: None}
    visited_order = []
    
    found = False
    while queue:
        curr = queue.popleft()
        visited_order.append(curr)
        
        if curr == maze.end:
            found = True
            break
            
        for nbr in maze.get_neighbors(*curr):
            if nbr not in parent:
                parent[nbr] = curr
                queue.append(nbr)
                
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = (time.perf_counter() - start_time) * 1000  # ms
    
    path = []
    if found:
        curr = maze.end
        while curr:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        
    return {
        "algorithm": "BFS (Búsqueda en Anchura)",
        "found": found,
        "path": path,
        "path_length": len(path),
        "explored_count": len(visited_order),
        "visited_order": visited_order,
        "time_ms": elapsed,
        "peak_mem_kb": peak_mem / 1024
    }

def solve_dfs_backtracking(maze):
    start_time = time.perf_counter()
    tracemalloc.start()
    
    stack = [maze.start]
    parent = {maze.start: None}
    visited = {maze.start}
    visited_order = []
    
    found = False
    while stack:
        curr = stack.pop()
        visited_order.append(curr)
        
        if curr == maze.end:
            found = True
            break
            
        for nbr in maze.get_neighbors(*curr):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = curr
                stack.append(nbr)
                
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = (time.perf_counter() - start_time) * 1000
    
    path = []
    if found:
        curr = maze.end
        while curr:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        
    return {
        "algorithm": "DFS / Backtracking",
        "found": found,
        "path": path,
        "path_length": len(path),
        "explored_count": len(visited_order),
        "visited_order": visited_order,
        "time_ms": elapsed,
        "peak_mem_kb": peak_mem / 1024
    }

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve_astar(maze):
    start_time = time.perf_counter()
    tracemalloc.start()
    
    # Priority Queue: (f_score, counter, current_node)
    counter = 0
    open_heap = [(manhattan_distance(maze.start, maze.end), counter, maze.start)]
    parent = {maze.start: None}
    g_score = {maze.start: 0}
    visited_order = []
    closed_set = set()
    
    found = False
    while open_heap:
        f, _, curr = heapq.heappop(open_heap)
        
        if curr in closed_set:
            continue
        closed_set.add(curr)
        visited_order.append(curr)
        
        if curr == maze.end:
            found = True
            break
            
        for nbr in maze.get_neighbors(*curr):
            tentative_g = g_score[curr] + 1
            if nbr not in g_score or tentative_g < g_score[nbr]:
                g_score[nbr] = tentative_g
                parent[nbr] = curr
                h = manhattan_distance(nbr, maze.end)
                f_score = tentative_g + h
                counter += 1
                heapq.heappush(open_heap, (f_score, counter, nbr))
                
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = (time.perf_counter() - start_time) * 1000
    
    path = []
    if found:
        curr = maze.end
        while curr:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        
    return {
        "algorithm": "A* (A-Star)",
        "found": found,
        "path": path,
        "path_length": len(path),
        "explored_count": len(visited_order),
        "visited_order": visited_order,
        "time_ms": elapsed,
        "peak_mem_kb": peak_mem / 1024
    }

if __name__ == '__main__':
    print("Testing Maze Solver...")
    m = Maze.generate(21, 21, seed=42)
    res_bfs = solve_bfs(m)
    res_dfs = solve_dfs_backtracking(m)
    res_astar = solve_astar(m)
    print(f"BFS: Path={res_bfs['path_length']}, Explored={res_bfs['explored_count']}, Time={res_bfs['time_ms']:.3f}ms")
    print(f"DFS: Path={res_dfs['path_length']}, Explored={res_dfs['explored_count']}, Time={res_dfs['time_ms']:.3f}ms")
    print(f"A*:  Path={res_astar['path_length']}, Explored={res_astar['explored_count']}, Time={res_astar['time_ms']:.3f}ms")
