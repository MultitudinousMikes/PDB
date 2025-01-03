from pyeda.inter import *
from collections import deque
import itertools
import sys

class PartialSymbolicPatternDatabase:
    def __init__(self, pattern, goal_state):
 
        self.pattern = pattern
        self.n = 3 
        self.goal_state = goal_state
        self.transit_re = self.transition()
        self.bdd_states = {}

    def transition(self):

        tr = {}
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

        for row in range(self.n):
            for col in range(self.n):
                vmove = []
                for dr, dc in dir:
                    nrow, ncol = row + dr, col + dc
                    if 0 <= nrow < self.n and 0 <= ncol < self.n:
                        vmove.append((row, col, nrow, ncol))
                tr[(row, col)] = vmove
        return tr

    def project_state(self, state, pattern):

        proj = set()
        for tile, pos in state.items():
            if tile in pattern or tile == 0:
                proj.add((tile, pos))
        return frozenset(proj)

    def construct_pspdb(self, pattern):

        front = deque([(self.project_state(self.goal_state, pattern), 0)])
        visited = set()
        count = 0 

        while front:
            state, cost = front.popleft()

            if state in visited:
                continue
            visited.add(state)
            count += 1

            if cost not in self.bdd_states:
                self.bdd_states[cost] = set()
            self.bdd_states[cost].add(state)

            #print(f"Processing state at cost {cost}: {state}")

            erow, ecol = dict(state)[0] 
            for row, col, nrow, ncol in self.transit_re[(erow, ecol)]:
                nstate = self.swap(dict(state), (nrow, ncol), (erow, ecol))
                proj = self.project_state(nstate, pattern)
                if proj not in visited:
                    front.append((proj, cost + 1))

        print(f"Total entries expanded: {count}")

    def pspdb_memory(self):

        memory = 0
        for cost, states in self.bdd_states.items():
            memory += sys.getsizeof(states)

            ssize = 0
            for state in states:
                ssize += sys.getsizeof(state)
            memory += ssize
        print(f"Total memory used by PSPDB: {(memory / 1024):.2f} KB")

    def swap(self, state, pos1, pos2):

        nstate = dict(state)
        for tile, position in state.items():
            if position == pos1:
                nstate[tile] = pos2
            elif position == pos2:
                nstate[tile] = pos1
        return nstate

    def heuristic(self, curr_state, pattern):

        state_key = self.project_state(curr_state, pattern)
        for cost, states in sorted(self.bdd_states.items()):
            if state_key in states:
                return cost
        return float('inf')

    def partial_symbolic_search(self, start_state, pattern):
    
        open_list = deque([(self.project_state(start_state, pattern), frozenset(start_state.items()), 0)])
        visited = set()
        pmap = {}

        while open_list:
            proj, fstate, cost = open_list.popleft()


            if proj == self.project_state(self.goal_state, pattern):
                print(f"Goal reached with cost: {cost}")
                self.reconstruct_path(pmap, fstate, pattern)
                return

            if proj in visited:
                continue
            visited.add(proj)


            erow, ecol = dict(fstate)[0] 
            for row, col, nrow, ncol in self.transit_re[(erow, ecol)]:
                nf_state = self.swap(dict(fstate), (nrow, ncol), (erow, ecol))

                nf_state = frozenset(nf_state.items())  
                nproj = self.project_state(dict(nf_state), pattern)

                if nproj not in visited:

                    pmap[nf_state] = fstate 
                    open_list.append((nproj, nf_state, cost + 1))

        print("No solution found.")


    def reconstruct_path(self, pmap, fstate, pattern):

        path = []
        curr_state = fstate

        while curr_state in pmap:

            path.append(dict(curr_state))
            curr_state = pmap[curr_state] 


        path.append(dict(curr_state)) 
        print("Solution Path:")
        for state in reversed(path):
            self.board_print(state)

    def board_print(self, state):
 
        board = []
        for _ in range(self.n):
            row = [' '] * self.n
            board.append(row)
        for tile, (row, col) in state.items():
            board[row][col] = str(tile)
        for row in board:
            print(' '.join(row))
        print()