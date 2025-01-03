from collections import deque
import itertools
import sys
import heapq

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def valid(x, y):
    if 0 <= x < 3 and 0 <= y < 3:
        return True
    return False

def state_to_key(positions):

    if isinstance(positions, tuple):
        positions = dict(positions) 
    t = []
    for tile in positions:
        t.append((tile, positions[tile]))

    result = tuple(sorted(t))
    
    return result

def construct_pdb(goal_state, pattern):
    pdb = {}
    queue = deque()
    goal_pos = {}
    for tile in pattern:
        goal_pos[tile] = goal_state[tile]

    blank = goal_state[0]
    ini_state = (goal_pos, blank)
    queue.append((ini_state, 0))

    visited = set()
    visited.add(state_to_key(goal_pos))
    
    while queue:
        (curr_pos, blank_pos), dist = queue.popleft()
        state_key = state_to_key(curr_pos)
        pdb[state_key] = dist

        #print(f"Processing state at cost {dist}: {state_key}")
        for dx, dy in directions:
            nblank = (blank_pos[0] + dx, blank_pos[1] + dy)
            if valid(*nblank):
                npos, up_blank = move_tile(curr_pos, blank_pos, nblank)
                nstate_key = state_to_key(npos) 
                if nstate_key not in visited:
                    visited.add(nstate_key)
                    queue.append(((npos, nblank), dist + 1))

    return pdb


def move_tile(positions, blank_pos, nblank):

    npos = positions.copy()
    for tile, pos in positions.items():
        if pos == nblank:
            npos[tile] = blank_pos
            break
    npos[0] = nblank 
    return npos, nblank

def heuristic(positions, goal_state):
    dis = 0
    for tile, pos in positions.items():
        if tile != 0:
            goal_pos = goal_state[tile]
            dis += abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])
    return dis

def pdb_memory(pdb):
    memory = 0
    for key, value in pdb.items():
        memory += sys.getsizeof(key) + sys.getsizeof(value)
    print(f"Total PDB memory usage: {(memory / 1024):.2f} KB")
    return memory

def pdb_astar_search(start_state, goal_state):

    ini_pos = start_state.copy()
    blank_pos = start_state[0]

    start_key = state_to_key(ini_pos)
    prior = []
    heapq.heappush(prior, (0, 0, start_key, blank_pos, []))

    visited = set()
    visited.add(start_key)

    while prior:
        f, g, current_key, blank_pos, path = heapq.heappop(prior)
        curr_pos = {tile: pos for tile, pos in current_key}

        if curr_pos == goal_state:
            print("Solution path:")
            print_solution(path + [current_key])
            return g


        for dx, dy in directions:
            nblank = (blank_pos[0] + dx, blank_pos[1] + dy)
            if valid(*nblank):
                npos, up_blank = move_tile(curr_pos, blank_pos, nblank)
                new_key = state_to_key(npos)
                if new_key not in visited:
                    visited.add(new_key)
                    h = heuristic(npos, goal_state)
                    heapq.heappush(prior, (g + 1 + h, g + 1, new_key, up_blank, path + [current_key]))
    return -1

def print_solution(path):
    for step, state in enumerate(path):
        grid = []
        for _ in range(3):
            row = [' ' for _ in range(3)]
            grid.append(row)
        for tile, pos in state:
            x, y = pos
            grid[x][y] = str(tile) if tile != 0 else '0'
        for row in grid:
            print(" ".join(row))
        print()