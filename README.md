# PDB
Project Title: Partial and Symbolic Pattern Database Implementations  

Description  
  This project implements Partial Pattern Databases (PPDB) and Symbolic Pattern Databases (SPDB) for state-space search problems, such as sliding tile puzzles (e.g., 3x3, 4x4, and 5x5).  

It features two search algorithms:  
  Partial A*: Uses PPDB as heuristics for faster state expansion.  
  Symbolic Search: Utilizes SPDBs and Binary Decision Diagrams (BDDs) to represent large state spaces efficiently.  

This repository includes:    
  PPDB generation using reverse Breadth-First Search.  
  SPDB construction using symbolic operations with BDDs.  
  Search algorithms: Partial A* and Symbolic Search.  

Performance measurements:  
  runtime  
  memory usage  
  solution cost  

Commands for executing the program:  
  pip install pyeda
  python run_experiments.py

Program Breakdown  
1. Run Experiments (run_experiments.py)​  
  a. Initialize Map and States: initial_map, start_state, goal_state  
  b. Run Full Pattern Database (PDB): run_pdb  
  c. Run Partial Pattern Database (PPDB): run_ppdb  
  d. Run Symbolic Pattern Database (SPDB): run_spdb  
  e. Run Partial Symbolic Pattern Database (PSPDB): run_pspdb  
2. Full Pattern Database (apdb.py)
	a. Construct PDB: construct_pdb
	b. Memory Measurement: pdb_memory
	c. Heuristic Computation: heuristic
	d. A* Search Execution: pdb_astar_search
	e. Tile Movement Operations: move_tile
3. Partial Pattern Database (ppdb.py)
	a. Construct PPDB: construct_PPDB
	b. Memory Measurement: ppdb_memory
	c. Heuristic Evaluation: heuristic
	d. Search Execution: ppdb_astar_search
	e. State Operations:
		Move Tile: move_tile
		Valid Moves: valid_move
4. Symbolic Pattern Database (spdb.py)​
 	a. Construct SPDB: construct_SPDB
	b. Memory Measurement: spdb_memory
	c. Heuristic Evaluation: heuristic
	d. Search Execution: symbolic_search
	e. State Operations:
		BDD State: project_state
		Transition Relations: transition
		Swap State Positions: swap
	f. Solution Path Reconstruction: reconstruct_path
5. Partial Symbolic Pattern Database (pspdb.py)​
	a. Construct PSPDB: construct_PSPDB
	b. Memory Measurement: pspdb_memory
	c. Heuristic Evaluation: heuristic
	d. Search Execution: partial_symbolic_search
	e. State Operations:
		BDD State: project_state
		Transition Relations: transition
		Swap State Positions: swap
	f. Solution Path Reconstruction: reconstruct_path
