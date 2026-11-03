"""
Task 1 - Breadth-First Search and Depth-First Search
The two functions bfs() and dfs() are the versions given in the manual.
traced_bfs() / traced_dfs() are my own versions that also record every step.
"""
from collections import deque

try:
    from .graphs import graph
except ImportError:
    from graphs import graph


# ---------------- manual code (section 3.2) ----------------
def bfs(start, goal):
    q=deque([(start,[start])]); seen={start}
    while q:
        node,path=q.popleft()
        if node==goal: return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n,path+[n]))

def dfs(start, goal):
    stack=[(start,[start])]; seen=set()
    while stack:
        node,path=stack.pop()
        if node==goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n,path+[n]))


# ---------------- my traced versions ----------------
def join(path):
    return "".join(path)


def traced_bfs(g, start, goal):
    frontier = deque([[start]])
    discovered = {start}
    steps = []
    while frontier:
        path = frontier.popleft()
        node = path[-1]
        if node == goal:
            steps.append((node, join(path), "GOAL", [join(p) for p in frontier]))
            return path, steps
        new = [n for n in g[node] if n not in discovered]
        for n in new:
            discovered.add(n)
            frontier.append(path + [n])
        steps.append((node, join(path), ",".join(new) or "-", [join(p) for p in frontier]))
    return None, steps


def traced_dfs(g, start, goal):
    frontier = [[start]]
    expanded = set()
    steps = []
    while frontier:
        path = frontier.pop()
        node = path[-1]
        if node == goal:
            steps.append((node, join(path), "GOAL", [join(p) for p in frontier]))
            return path, steps
        if node in expanded:
            steps.append((node + "*", join(path), "already expanded", [join(p) for p in frontier]))
            continue
        expanded.add(node)
        kids = list(reversed(g[node]))
        for n in kids:
            frontier.append(path + [n])
        steps.append((node, join(path), ",".join(kids) or "-", [join(p) for p in frontier]))
    return None, steps


def print_steps(name, steps, frontier_name):
    print(f"{name} step-by-step  (frontier = {frontier_name})")
    print("#  | node | path    | added  | frontier")
    for i, (node, path, added, front) in enumerate(steps, start=1):
        print(f"{i:<2} | {node:<4} | {path:<7} | {added:<6} | {front}")


def run():
    print("-" * 70)
    print("Task 1 | BFS and DFS on the manual graph (A -> G)")
    print("-" * 70)
    print("graph:", graph)
    print()
    d_path, d_steps = traced_dfs(graph, "A", "G")
    print_steps("DFS", d_steps, "stack, top = last")
    print("DFS expansion order:", " ".join(s[0] for s in d_steps))
    print("DFS path:", " -> ".join(d_path))
    print()
    b_path, b_steps = traced_bfs(graph, "A", "G")
    print_steps("BFS", b_steps, "queue, front = first")
    print("BFS expansion order:", " ".join(s[0] for s in b_steps))
    print("BFS path:", " -> ".join(b_path))
    print()
    print("Cross-check with the manual functions:")
    print(f"  bfs('A','G') = {bfs('A', 'G')}  same as trace: {bfs('A', 'G') == b_path}")
    print(f"  dfs('A','G') = {dfs('A', 'G')}  same as trace: {dfs('A', 'G') == d_path}")
    print("  BFS expanded 7 nodes, DFS only 5 - but BFS guarantees the fewest edges.")


if __name__ == "__main__":
    run()
