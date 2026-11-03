"""
Task 3 - Uniform Cost Search vs BFS on the weighted graph
UCS always expands the cheapest path in the frontier (priority queue on g).
Ties are broken by insertion order using a counter.
"""
import heapq
from collections import deque
from itertools import count

try:
    from .graphs import weighted_graph
except ImportError:
    from graphs import weighted_graph


def uniform_cost(g, start, goal):
    """Return (cost, path, expansion order, log)."""
    tie = count()
    frontier = [(0, next(tie), [start])]
    best_g = {start: 0}
    expansion, log = [], []
    while frontier:
        g_cost, _, path = heapq.heappop(frontier)
        node = path[-1]
        if g_cost > best_g.get(node, float("inf")):
            log.append((node, g_cost, "".join(path), "outdated, skipped", ""))
            continue
        expansion.append(node)
        if node == goal:
            log.append((node, g_cost, "".join(path), "GOAL", show(frontier)))
            return g_cost, path, expansion, log
        added = []
        for nxt, w in g.get(node, []):
            new_g = g_cost + w
            if new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                heapq.heappush(frontier, (new_g, next(tie), path + [nxt]))
                added.append(f"{nxt}={new_g}")
        log.append((node, g_cost, "".join(path), " ".join(added) or "-", show(frontier)))
    return None, None, expansion, log


def show(frontier):
    return "{" + ", ".join(f"{''.join(p)}:{c}" for c, _, p in sorted(frontier)) + "}"


def bfs_hops(g, start, goal):
    """BFS that ignores the weights (fewest edges)."""
    queue, seen, order = deque([[start]]), {start}, []
    while queue:
        path = queue.popleft()
        order.append(path[-1])
        if path[-1] == goal:
            return path, order
        for nxt, _w in g[path[-1]]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + [nxt])
    return None, order


def cost_of(g, path):
    pieces = [(u, v, dict(g[u])[v]) for u, v in zip(path, path[1:])]
    return sum(w for *_, w in pieces), " + ".join(f"{u}{v}({w})" for u, v, w in pieces)


def run():
    print("-" * 70)
    print("Task 3 | Uniform Cost Search vs BFS (weighted graph)")
    print("-" * 70)
    print("Edges:")
    for u, edges in weighted_graph.items():
        for v, w in edges:
            note = "  <- new corridor" if (u, v) == ("C", "G") else ""
            print(f"  {u}->{v} = {w}{note}")
    print()
    cost, path, order, log = uniform_cost(weighted_graph, "A", "G")
    print("UCS log:")
    print("# | node | g  | path | added (node=g) | frontier after")
    for i, (node, g_cost, p, added, front) in enumerate(log, start=1):
        print(f"{i} | {node:<4} | {g_cost:<2} | {p:<4} | {added:<14} | {front}")
    total, expr = cost_of(weighted_graph, path)
    print(f"UCS expansion order: {' '.join(order)}")
    print(f"UCS path {'-'.join(path)}, cost {cost}; check: {expr} = {total} -> {'correct' if total == cost else 'MISMATCH'}")
    print()
    b_path, b_order = bfs_hops(weighted_graph, "A", "G")
    b_cost, b_expr = cost_of(weighted_graph, b_path)
    print(f"BFS expansion order: {' '.join(b_order)}")
    print(f"BFS path {'-'.join(b_path)}, {len(b_path) - 1} edges, cost {b_expr} = {b_cost}")
    print()
    print("Comparison:")
    print("method | path    | edges | cost")
    print(f"UCS    | {'-'.join(path):<7} | {len(path) - 1:<5} | {total}")
    print(f"BFS    | {'-'.join(b_path):<7} | {len(b_path) - 1:<5} | {b_cost}")
    print("-> BFS finds the path with fewer edges, UCS finds the cheaper one.")
    print()
    print("Edge cases:")
    c, p, _, _ = uniform_cost(weighted_graph, "F", "G")
    print(f"  unreachable (F->G): cost={c}, path={p}")
    c, p, _, _ = uniform_cost(weighted_graph, "C", "C")
    print(f"  start is goal (C->C): cost={c}, path={p}")
    loopy = {k: list(v) for k, v in weighted_graph.items()}
    loopy["F"] = [("A", 1)]
    loopy["E"] = [("B", 2), ("G", 1)]
    c, p, o, _ = uniform_cost(loopy, "A", "G")
    print(f"  with cycles (F->A, E->B): cost={c}, path={'-'.join(p)}, expanded {' '.join(o)}")


if __name__ == "__main__":
    run()
