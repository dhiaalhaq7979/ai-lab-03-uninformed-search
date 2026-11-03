"""Graphs used in this lab."""

# Unweighted graph given in the manual (section 3.2)
graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}

# Same graph with weights (Task 3).
# A-B-E-G = 3 and the new corridor C -> G (so A-C-G = 12) follow the manual.
# The manual does not give B->D and C->F, so I chose 5 and 2 myself.
weighted_graph = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 5), ("E", 1)],
    "C": [("F", 2), ("G", 10)],   # C -> G is the added corridor
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}


def with_cycles(g):
    """Copy of the unweighted graph with two back edges (F->A and E->B)."""
    new = {k: list(v) for k, v in g.items()}
    new["F"] = ["A"]
    new["E"] = ["B", "G"]
    return new
