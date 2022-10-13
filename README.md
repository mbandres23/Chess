# pythonTest

Usage

Standard Mode

Run chess.py from the command line with the two parameters noted below to get a list of all the potential board positions the given piece could advance to, with one move, from the given position, with the assumption there are no other pieces on the board.

This program requires at least two parameters:
1. Type of chess piece (Queen, Rook, Knight). Other piece types not supported.
2. Current position on a chess board (for example: d2)

Example:
$ chess.py --piece KNIGHT --position d2

The response would be:  “b1, f1, b3, f3,c4, e4"


Target Mode

Activate target mode by adding "--target" to your command line statement. This will
1. Randomly place 8 (opposing) pieces onto the board tiles.
2. Determine the physically most distant tile from Current position.
3. Calculate and output the minimum set of moves which the given piece Type could take to the most distant tile given that:
    - Opposing pieces do not move.
    - Opposing pieces may be “captured” along the way by moving to the occupied tile.
    - Capturing an opposing piece marks the end of a “move”.
    
Example:
$ chess.py --piece QUEEN --position e4 --target


Collector Mode

Activate collector mode by adding "--collect" to your command line statement. This will
1. Randomly place 8 (opposing) pieces onto the board tiles.
2. Calculate and output the minimum set of moves which the given piece Type could take to capture all opposing pieces.

Example:
$ chess.py --piece QUEEN --position e4 --collect


Highlights on the approach and data structures used:
- Target Mode implements a queue-based breadth-first search.
- Collector Mode implements a priority queue-based breadth first search. We prioritize "capture spaces" to improve efficiency of the search. Although, running Collector Mode can still be slow for the knight since it's movement on the board is non-linear.
- For more detail, see comments in the chess.py file.
