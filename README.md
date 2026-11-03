# AI Lab 03 — Uninformed Search Strategies

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-success?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

This lab is about searching a graph **without any heuristic** — the agent only knows the edges, not how close it is to the goal. I implemented and traced four classic algorithms and compared them on the same graph:

- **BFS** – Breadth-First Search (FIFO queue)
- **DFS** – Depth-First Search (LIFO stack)
- **DLS / IDS** – Depth-Limited Search and Iterative Deepening
- **UCS** – Uniform Cost Search (priority queue on path cost)

## Structure

```
ai-lab-03-uninformed-search/
├── run_lab.py              # runs all three tasks
├── search/
│   ├── graphs.py           # the graphs (unweighted + weighted)
│   ├── bfs_dfs.py          # Task 1 – BFS and DFS with step traces
│   ├── depth_limited.py    # Task 2 – DLS and IDS + edge cases
│   └── uniform_cost.py     # Task 3 – UCS vs BFS on the weighted graph
└── results/
    └── sample_run.txt
```

## Run

```bash
python run_lab.py
```

## The graph

```
        A
      /   \
     B     C
    / \     \
   D   E     F
       |
       G
```

## Task 1 — BFS vs DFS (A → G)

| Algorithm | Expansion order | Path | Nodes expanded |
|-----------|-----------------|------|----------------|
| DFS | A B D E G | A → B → E → G | 5 |
| BFS | A B C D E F G | A → B → E → G | 7 |

Both find the same path here, but BFS explores level by level, so it expands more nodes. Its advantage is that it always returns the path with the fewest edges.

## Task 2 — DLS and Iterative Deepening

Depth is counted in edges (A = depth 0). To avoid infinite loops, a node is skipped if it is already on the current path.

| Limit | DLS result | Nodes expanded |
|-------|-----------|----------------|
| 1 | CUTOFF | 3 |
| 2 | CUTOFF | 6 |
| 3 | FOUND A→B→E→G | 5 |
| 4 | FOUND A→B→E→G | 5 |

IDS with a maximum limit of 3 finds the goal after **15** total expansions (1 + 3 + 6 + 5). The shallow levels are repeated every round — that is the price IDS pays for using very little memory.

Edge cases I tested: unreachable goal (D→G gives FAILURE, not CUTOFF), start equal to goal, and a graph with back edges F→A and E→B — the search still terminates at every limit.

## Task 3 — UCS vs BFS on a weighted graph

I added a direct corridor **C → G** with cost 10. The manual gives the A-B-E-G cost (3) and the corridor; I chose B→D = 5 and C→F = 2 myself.

| Method | Path | Edges | Total cost |
|--------|------|-------|------------|
| BFS | A – C – G | 2 | 12 |
| UCS | A – B – E – G | 3 | **3** |

BFS stops at the path with fewer edges, but it is 4× more expensive. UCS expands nodes in order of path cost, so it returns the cheapest route. I also verified the UCS cost by summing the edges independently.

## What I learned

- BFS is optimal only when every edge has the same cost.
- DFS is memory-friendly but can wander deep into the wrong branch.
- IDS combines the low memory of DFS with the completeness of BFS.
- When edges have different costs, UCS is the right uninformed choice.

## Author

**Dhia Alhaq Saleh Al-Hindrish** — BS Software Engineering, Superior University, Lahore
GitHub: [@dhiaalhaq7979](https://github.com/dhiaalhaq7979)

Licensed under the [MIT License](LICENSE).
