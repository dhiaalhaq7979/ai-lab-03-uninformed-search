"""Entry point for AI Lab 03. Run with:  python run_lab.py"""
import sys

from search import bfs_dfs, depth_limited, uniform_cost


if __name__ == "__main__":
    print("AI Lab 03 - Uninformed Search Strategies")
    print("Student: Dhia Alhaq Saleh Al-Hindrish | BS Software Engineering")
    print(f"Python {sys.version.split()[0]} (standard library only)")
    print()
    bfs_dfs.run()
    print()
    depth_limited.run()
    print()
    uniform_cost.run()
