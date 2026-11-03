"""
Task 2 - Depth-Limited Search (DLS) and Iterative Deepening (IDS)
- the start node has depth 0, every edge adds 1
- cycle check: a node is skipped if it is already on the CURRENT path
- result is one of: FOUND, CUTOFF (the limit stopped us), FAILURE (nothing left)
"""
try:
    from .graphs import graph, with_cycles
except ImportError:
    from graphs import graph, with_cycles

FOUND, CUTOFF, FAILURE = "FOUND", "CUTOFF", "FAILURE"


def depth_limited(g, start, goal, limit):
    """Return (status, path or None, list of expanded nodes)."""
    expanded = []

    def explore(path, depth):
        node = path[-1]
        expanded.append(node)
        if node == goal:
            return FOUND, path
        next_nodes = [n for n in g.get(node, []) if n not in path]
        if depth == limit:
            # we are at the limit; it is only a cutoff if deeper nodes exist
            return (CUTOFF if next_nodes else FAILURE), None
        hit_limit = False
        for n in next_nodes:
            status, found = explore(path + [n], depth + 1)
            if status == FOUND:
                return status, found
            hit_limit = hit_limit or status == CUTOFF
        return (CUTOFF if hit_limit else FAILURE), None

    status, path = explore([start], 0)
    return status, path, expanded


def iterative_deepening(g, start, goal, max_limit):
    """Run DLS with limit 0, 1, 2 ... max_limit. Returns (status, path, rounds)."""
    rounds = []
    for limit in range(max_limit + 1):
        status, path, expanded = depth_limited(g, start, goal, limit)
        rounds.append((limit, status, expanded))
        if status != CUTOFF:          # FOUND, or FAILURE (a larger limit cannot help)
            return status, path, rounds
    return CUTOFF, None, rounds


def fmt(path):
    return "->".join(path) if path else "none"


def run():
    print("-" * 70)
    print("Task 2 | Depth-Limited Search and Iterative Deepening")
    print("-" * 70)
    print("DLS from A to G:")
    print("limit | result  | path       | #expanded | expanded nodes")
    for limit in (4, 3, 2, 1):
        status, path, expanded = depth_limited(graph, "A", "G", limit)
        print(f"{limit:<5} | {status:<7} | {fmt(path):<10} | {len(expanded):<9} | {' '.join(expanded)}")
    print()
    print("IDS from A to G with different maximum limits:")
    print("max | result  | path       | rounds (limit:result:#nodes)      | total expanded")
    for max_limit in (1, 2, 3, 4):
        status, path, rounds = iterative_deepening(graph, "A", "G", max_limit)
        summary = " ".join(f"{l}:{s}:{len(e)}" for l, s, e in rounds)
        total = sum(len(e) for _, _, e in rounds)
        print(f"{max_limit:<3} | {status:<7} | {fmt(path):<10} | {summary:<33} | {total}")
    print()
    print("Repeated work inside IDS (max limit 3):")
    for limit, status, expanded in iterative_deepening(graph, "A", "G", 3)[2]:
        print(f"  round {limit}: {' '.join(expanded)}  [{status}]")
    print()
    print("Edge cases:")
    status, path, expanded = depth_limited(graph, "D", "G", 5)
    print(f"  goal not reachable (D->G, limit 5): {status}, expanded {expanded}")
    status, path, expanded = depth_limited(graph, "A", "A", 0)
    print(f"  start is the goal (A->A, limit 0): {status} {fmt(path)}")
    loopy = with_cycles(graph)
    print(f"  graph with cycles (F->A, E->B): {loopy}")
    for limit in (1, 3, 8):
        status, path, expanded = depth_limited(loopy, "A", "G", limit)
        print(f"    limit {limit}: {status} {fmt(path)}, {len(expanded)} nodes expanded - terminates")
    status, _, _ = depth_limited(loopy, "A", "X", 12)
    print(f"    missing goal X, limit 12: {status} - the path check stops the loops")


if __name__ == "__main__":
    run()
