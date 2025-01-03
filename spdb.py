from pyeda.inter import *
from collections import deque
import itertools
import sys

class SymbolicPatternDatabase:
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

    def project_state(self, state):

        proj = set()
        for tile, pos in state.items():
            if tile in self.pattern or tile == 0:
                proj.add((tile, pos))
        return frozenset(proj)

    def construct_spdb(self):

        front = deque([(self.project_state(self.goal_state), 0)])
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
            for move in self.transit_re[(erow, ecol)]:
                row, col, nrow, ncol = move
                nstate = self.swap(dict(state), (nrow, ncol), (erow, ecol))
                proj = self.project_state(nstate)
                if proj not in visited:
                    front.append((proj, cost + 1))

        print(f"Total entries expanded: {count}")

    def spdb_memory(self):

        memory = 0
        for cost, states in self.bdd_states.items():
            memory += sys.getsizeof(states)

            ssize = 0
            for state in states:
                ssize += sys.getsizeof(state)
            memory += ssize
        print(f"Total memory used by SPDB: {(memory / 1024):.2f} KB")

    def swap(self, state, pos1, pos2):

        nstate = dict(state)
        for tile, position in state.items():
            if position == pos1:
                nstate[tile] = pos2
            elif position == pos2:
                nstate[tile] = pos1
        return nstate

    def heuristic(self, curr_state):

        state_key = self.project_state(curr_state)
        for cost, states in sorted(self.bdd_states.items()):
            if state_key in states:
                return cost
        return float('inf')

    def symbolic_search(self, start_state):

        open_list = deque([(self.project_state(start_state), 0)]) 
        visited = set()
        pmap = {} 
        step_count = 0  

        while open_list:
            state, cost = open_list.popleft()

            if state == self.project_state(self.goal_state):
                print(f"Goal reached with cost: {cost}")
                self.reconstruct_path(pmap, start_state)
                return

            if state in visited:
                continue
            visited.add(state)

            erow, ecol = dict(state)[0]
            for move in self.transit_re[(erow, ecol)]:
                row, col, nrow, ncol = move
                nstate = self.swap(dict(state), (nrow, ncol), (erow, ecol))
                proj = self.project_state(nstate)
                step_count += 1 

                if proj not in visited:
                    pmap[proj] = state 
                    open_list.append((proj, cost + 1))
        print("No solution found")

    def reconstruct_path(self, pmap, start_state):

        path = []
        curr_state = self.project_state(self.goal_state)

        while curr_state != self.project_state(start_state):
            path.append(curr_state)
            if curr_state not in pmap:
                print("Error: State missing in parent map")
                return
            curr_state = pmap[curr_state]
        path.append(self.project_state(start_state))

        print("Solution Path:")
        for state in reversed(path):
            self.board_print(dict(state))

    def board_print(self, state):

        board = []
        for _ in range(self.n):
            board.append([' '] * self.n)
        for tile, (row, col) in dict(state).items():
            board[row][col] = str(tile)
        for row in board:
            print(' '.join(row))
        print()