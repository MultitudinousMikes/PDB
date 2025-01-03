#!/usr/bin/python
import sys
from ppdb import construct_ppdb, ppdb_memory, ppdb_astar_search
from spdb import SymbolicPatternDatabase
from pspdb import PartialSymbolicPatternDatabase
from time import perf_counter_ns
from apdb import construct_pdb, pdb_memory, pdb_astar_search

def initial_map(size):
    m = []
    for _ in range(size):
        m.append([False] * size)
    return m

def run_pdb(start_state, goal_state, pattern):
    print("Building PDB")
    startC_time = perf_counter_ns()
    pdb = construct_pdb(goal_state, pattern)
    stopC_time = perf_counter_ns()

    print(f"PDB built with {len(pdb)} entries")
    pdb_memory(pdb)
    print(f"Time for PDB construction: {((stopC_time - startC_time) / 1000000): .2f} ms")

    print("Running A* Search")
    startS_time = perf_counter_ns()
    solution = pdb_astar_search(start_state, goal_state)
    stopS_time = perf_counter_ns()
    print(f"Time for astar serach: {((stopS_time - startS_time) / 1000000): .2f} ms")
    if solution != -1:
        print(f"Solution found in {solution} steps.")
    else:
        print("No solution found.")

def run_ppdb(start_state, goal_state, pattern):
    
    print("Building PPDB")
    startC_time = perf_counter_ns()
    ppdb = construct_ppdb(goal_state, pattern)
    stopC_time = perf_counter_ns()
    print(f"PPDB built with {len(ppdb)} entries")
    ppdb_memory(ppdb)
    print(f"Time for PPDB construction: {((stopC_time - startC_time) / 1000000): .2f} ms")
    print("Running A* Search")
    startS_time = perf_counter_ns()
    ppdb_astar_search(start_state, goal_state, ppdb, pattern)
    stopS_time = perf_counter_ns()
    print(f"Time for astar serach: {((stopS_time - startS_time) / 1000000): .2f} ms")


def run_spdb(start_state, pattern, goal_state):

    spdb = SymbolicPatternDatabase(pattern, goal_state)

    print("Constructing SPDB")
    startC_time = perf_counter_ns()
    spdb.construct_spdb()
    stopC_time = perf_counter_ns()
    spdb.spdb_memory()
    print(f"Time for SPDB construction: {((stopC_time - startC_time) / 1000000): .2f} ms")
    print("Performing Symbolic Search")
    startS_time = perf_counter_ns()
    spdb.symbolic_search(start_state)
    stopS_time = perf_counter_ns()
    print(f"Time for Symbolic Search: {((stopS_time - startS_time) / 1000000): .2f} ms")
    h_value = spdb.heuristic(start_state)
    print(f"Heuristic value for start state: {h_value}")

def run_pspdb(start_state, pattern, goal_state):

    pspdb = PartialSymbolicPatternDatabase(pattern, goal_state)

    print("Constructing PSPDB")
    startC_time = perf_counter_ns()
    pspdb.construct_pspdb(pattern)
    stopC_time = perf_counter_ns()
    pspdb.pspdb_memory()
    print(f"Time for PSPDB construction: {((stopC_time - startC_time) / 1000000): .2f} ms")
    print("Performing Partial Symbolic Search")
    startS_time = perf_counter_ns()
    pspdb.partial_symbolic_search(start_state, pattern)
    stopS_time = perf_counter_ns()
    print(f"Time for Partial Symbolic Search: {((stopS_time - startS_time) / 1000000): .2f} ms")
    h_value = pspdb.heuristic(start_state, pattern)
    print(f"Heuristic value for start state: {h_value}")

if __name__ == '__main__':

    my_map = initial_map(4)

    start_state = {1: (0, 0), 2: (0, 1), 5: (0, 2),
                   3: (1, 0), 7: (1, 1), 4: (1, 2),
                   6: (2, 0), 0: (2, 1), 8: (2, 2)}

    goal_state = {0: (0, 0), 1: (0, 1), 2: (0, 2),
                  3: (1, 0), 4: (1, 1), 5: (1, 2),
                  6: (2, 0), 7: (2, 1), 8: (2, 2)}
    '''
    abstract_map = {
        0: "A", 1: "A", 2: "A", 3: "A",
        4: "B", 5: "B", 6: "B", 7: "B",
        8: "C", 9: "C", 10: "C", 11: "C",
        12: "D", 13: "D", 14: "D", 15: "D",
    }
    '''

    full_pattern = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    half_pattern = [0, 1, 2, 3, 4]


    run_pdb(start_state, goal_state, full_pattern)
    run_ppdb(start_state, goal_state, half_pattern)
    run_spdb(start_state, full_pattern, goal_state)
    run_pspdb(start_state, half_pattern, goal_state)
    

    
