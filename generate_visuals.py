import os
import matplotlib.pyplot as plt
import numpy as np
from maze_solver import Maze, solve_bfs, solve_dfs_backtracking, solve_astar

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9

def render_maze_matrix(maze, path=None, explored=None):
    rows, cols = maze.rows, maze.cols
    img = np.zeros((rows, cols, 3))
    for r in range(rows):
        for c in range(cols):
            if maze.grid[r][c] == '#':
                img[r, c] = [0.15, 0.20, 0.25]  # Pared oscura
            else:
                img[r, c] = [0.95, 0.95, 0.95]  # Pasillo libre
    
    if explored:
        for r, c in explored:
            if (r, c) != maze.start and (r, c) != maze.end:
                img[r, c] = [0.70, 0.85, 0.98]  # Celeste exploración
                
    if path:
        for r, c in path:
            if (r, c) != maze.start and (r, c) != maze.end:
                img[r, c] = [0.15, 0.75, 0.35]  # Verde camino óptimo
                
    img[maze.start[0], maze.start[1]] = [0.20, 0.50, 0.90]  # Azul Inicio
    img[maze.end[0], maze.end[1]] = [0.90, 0.20, 0.20]      # Rojo Meta
    return img

# 1. FIGURA 1: Entrada / carga de laberinto
m1 = Maze.generate(21, 21, seed=101)
fig, ax = plt.subplots(figsize=(6, 6), dpi=200)
img1 = render_maze_matrix(m1)
ax.imshow(img1, interpolation='nearest')
ax.set_title('FIGURA 1: Mapa del Laberinto (21x21)\nAzul: Inicio (1,1) | Rojo: Meta (19,19) | Oscuro: Muros', fontsize=11, fontweight='bold', pad=10)
ax.axis('off')
plt.tight_layout()
plt.savefig('fig1_entrada_laberinto.png', bbox_inches='tight')
plt.close()

# 2. FIGURA 2: Proceso / Comparación de algoritmos (BFS vs DFS vs A*)
res_bfs = solve_bfs(m1)
res_dfs = solve_dfs_backtracking(m1)
res_astar = solve_astar(m1)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=200)

axes[0].imshow(render_maze_matrix(m1, path=res_bfs['path'], explored=res_bfs['visited_order']), interpolation='nearest')
axes[0].set_title(f"BFS (Anchura)\nCeldas exploradas: {res_bfs['explored_count']}\nLongitud camino: {res_bfs['path_length']}\nTiempo: {res_bfs['time_ms']:.2f} ms", fontsize=10, fontweight='bold')
axes[0].axis('off')

axes[1].imshow(render_maze_matrix(m1, path=res_dfs['path'], explored=res_dfs['visited_order']), interpolation='nearest')
axes[1].set_title(f"DFS / Backtracking\nCeldas exploradas: {res_dfs['explored_count']}\nLongitud camino: {res_dfs['path_length']}\nTiempo: {res_dfs['time_ms']:.2f} ms", fontsize=10, fontweight='bold')
axes[1].axis('off')

axes[2].imshow(render_maze_matrix(m1, path=res_astar['path'], explored=res_astar['visited_order']), interpolation='nearest')
axes[2].set_title(f"A* (Heurística Manhattan)\nCeldas exploradas: {res_astar['explored_count']}\nLongitud camino: {res_astar['path_length']}\nTiempo: {res_astar['time_ms']:.2f} ms", fontsize=10, fontweight='bold')
axes[2].axis('off')

plt.suptitle('FIGURA 2: Comparación de Exploración y Eficiencia (Celeste=Explorado, Verde=Camino)', fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('fig2_proceso_comparacion.png', bbox_inches='tight')
plt.close()

# 3. FIGURA 3: Resultado Óptimo con A*
fig, ax = plt.subplots(figsize=(6.5, 6.5), dpi=200)
img3 = render_maze_matrix(m1, path=res_astar['path'])
ax.imshow(img3, interpolation='nearest')
ax.set_title(f"FIGURA 3: Ruta Óptima Resuelta con A*\nLongitud del camino: {res_astar['path_length']} pasos (Óptimo garantizado)", fontsize=11, fontweight='bold', pad=10)
ax.axis('off')
plt.tight_layout()
plt.savefig('fig3_resultado_optimo.png', bbox_inches='tight')
plt.close()

# 4. FIGURA 4: Caso Especial / Adverso (Sin Solución)
grid_blocked = [row[:] for row in m1.grid]
er, ec = m1.end
for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
    nr, nc = er + dr, ec + dc
    if 0 <= nr < m1.rows and 0 <= nc < m1.cols:
        grid_blocked[nr][nc] = '#'
m_blocked = Maze(grid_blocked, m1.start, m1.end)
res_blocked = solve_astar(m_blocked)

fig, ax = plt.subplots(figsize=(6.5, 6.5), dpi=200)
img4 = render_maze_matrix(m_blocked, path=res_blocked['path'], explored=res_blocked['visited_order'])
ax.imshow(img4, interpolation='nearest')
ax.set_title(f"FIGURA 4: Validación de Caso Especial (Sin Solución)\nDestino bloqueado | Espacio explorado: {res_blocked['explored_count']} celdas | Retorno: Sin ruta", fontsize=10, fontweight='bold', pad=10)
ax.axis('off')
plt.tight_layout()
plt.savefig('fig4_caso_especial_sin_solucion.png', bbox_inches='tight')
plt.close()

print('FIGURAS GENERADAS EXITOSAMENTE.')

# 5. BENCHMARK
scenarios = [
    ('Pequeño (11x11)', 11, 11, 10),
    ('Mediano (25x25)', 25, 25, 20),
    ('Grande (51x51)', 51, 51, 30)
]

with open('benchmark_results.txt', 'w', encoding='utf-8') as out:
    for label, r, c, seed in scenarios:
        m = Maze.generate(r, c, seed=seed)
        r_bfs = solve_bfs(m)
        r_dfs = solve_dfs_backtracking(m)
        r_ast = solve_astar(m)
        out.write(f"=== Escenario: {label} ===\n")
        out.write(f"BFS:  Tiempo={r_bfs['time_ms']:.4f} ms | Mem={r_bfs['peak_mem_kb']:.2f} KB | Nodos={r_bfs['explored_count']} | Longitud={r_bfs['path_length']}\n")
        out.write(f"DFS:  Tiempo={r_dfs['time_ms']:.4f} ms | Mem={r_dfs['peak_mem_kb']:.2f} KB | Nodos={r_dfs['explored_count']} | Longitud={r_dfs['path_length']}\n")
        out.write(f"A*:   Tiempo={r_ast['time_ms']:.4f} ms | Mem={r_ast['peak_mem_kb']:.2f} KB | Nodos={r_ast['explored_count']} | Longitud={r_ast['path_length']}\n\n")

print('BENCHMARK FINALIZADO.')
