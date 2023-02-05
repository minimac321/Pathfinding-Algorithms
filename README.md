# Pathfinding-Algorithms

Using a simulated environment - implement the following algorithms 
to identify the optimal path between two points.
- [Bread-First Search](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
- [Dijkstra](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/)
- [A*](https://www.geeksforgeeks.org/a-search-algorithm/)

### A-star Solutions
![a_star_best_path.png](images%2Fa_star_best_path.png)

### Dijkstra Solution
![dijkstra_best_path.png](images%2Fdijkstra_best_path.png)

#### Algorithm Comparison to solve
| Algorithm         | A-Star | Dijkstra |
|-------------------|--------|----------|
| Path Cost         | 34     | 34       |
| Time to Find (ms) | 0.572  | 0.767    |
| Nodes Searched    | 160    | 279      |


Grid with different costs for each element:
![img_with_grid.png](images%2Fimg_with_grid.png)

Costs table for each element within image:

| Cost | Element | Color       |
|------|---------|-------------|
| 1    | Road    | brown       |
| 2    | Grass   | light-green |
| 4    | Hedge   | dark-green  |
| 7    | Water   | turquoise   |
| 9    | Rock    | grey        |


## BFS Solution
![bfs_best_path.png](images%2Fbfs_best_path.png)
