import heapq
import itertools
from collections import deque
import sys

def man_distance(tile, goal):
    a = abs(tile[0] - goal[0])
    b = abs(tile[1] - goal[1])
    return a + b

def construct_ppdb(goal_state, pattern):

    queue = deque([(goal_state, 0)])
    visited = set()
    ppdb = {}

    while queue:
        state, cost = queue.popleft()
        ab_state = ab_state_full(state, pattern)

        #print(f"Processing state at cost {cost}: {ab_state}")

        if ab_state in visited:
            continue
        visited.add(ab_state)
        ppdb[ab_state] = cost

        blank = find_blank(state)
        for move in valid_move(blank):
            nstate = move_tile(state, blank, move)
            queue.append((nstate, cost + 1))

    return ppdb

def ppdb_memory(ppdb):

    memory = 0
    for key, value in ppdb.items():
        memory += sys.getsizeof(key) + sys.getsizeof(value)
    print(f"Total memory used by PPDB: {(memory / 1024):.2f} KB")
    return memory

def ab_state_full(state, pattern):

    ab = []
    for tile in pattern:
        if tile in state:
            ab.append((tile, tuple(state[tile])))
    return tuple(ab)

def find_blank(state):

    for tile, pos in state.items():
        if tile == 0:
            return pos

def move_tile(state, blank, nblank):

    nstate = state.copy()
    tmove = None
    for tile, pos in state.items():
        if pos == nblank:
            tmove = tile
            break
    nstate[tmove], nstate[0] = blank, nblank
    return nstate

def valid_move(blank):

    x, y = blank
    moves = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            moves.append((nx, ny))
    return moves

def heuristic(state, ppdb, pattern, goal_state):

    ab_state = ab_state_full(state, pattern)
    ppdb_cost = ppdb.get(ab_state, float('inf'))
    md_cost = 0
    for tile in state:
        if tile != 0:
            md_cost += man_distance(state[tile], goal_state[tile])
    return max(ppdb_cost, md_cost)


def print_solution(start_state, path):

    curr_state = start_state.copy()
    print("Solution Path:")
    print_grid(curr_state)
    for move in path:
        blank = find_blank(curr_state)
        curr_state = move_tile(curr_state, blank, move)
        print()
        print_grid(curr_state)

def print_grid(state):

    grid = []
    for _ in range(3):
        row = [None for _ in range(3)]
        grid.append(row)
    for tile, pos in state.items():
        x, y = pos
        grid[x][y] = tile
    for row in grid:
        result = []
        for tile in row:
            if tile != 0:
                result.append(str(tile))
            else:
                result.append("0")

        print(" ".join(result))

def ppdb_astar_search(start_state, goal_state, ppdb, pattern):

    open_list = []
    heapq.heappush(open_list, (0, 0, tuple(sorted(start_state.items())), [], None)) 
    visited = set()

    while open_list:
        f, g, state_items, path, parent = heapq.heappop(open_list)
        state = dict(state_items)

        if state == goal_state:
            print_solution(start_state, path)
            return path

        state_t = tuple(sorted(state.items()))
        if state_t in visited:
            continue
        visited.add(state_t)

        blank = find_blank(state)
        for move in valid_move(blank):
            nstate = move_tile(state, blank, move)
            if parent and tuple(sorted(nstate.items())) == parent: 
                continue
            npath = path + [move]
            ng = g + 1
            nf = ng + heuristic(nstate, ppdb, pattern, goal_state)
            heapq.heappush(open_list, (nf, ng, tuple(sorted(nstate.items())), npath, state_t))

    print("No solution found")
    return None