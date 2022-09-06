import argparse
import math
import random
from queue import Queue
import heapq

# This program allows the user to specify a chess piece (Queen, Rook, or Knight) and
#  a position on a standard chess board and will do run one of three modes as chosen
#  by the user. 
#  Standard mode returns a list of all the potential board positions the given piece
#  could advance to, with one move, from the given position, with the assumption
#  there are no other pieces on the board.
#  In Target mode, the program randomly places 8 enemy pawns on the board and prints
#  the minimum set of moves it takes the user's piece to reach the most distant tile
#  from the starting position, capturing pawns if necessary. This mode implements a
#  queue-based Breadth-first search.
#  In Collector mode, the program randomly places 8 enemy pawns on the board and
#  prints the minimum set of moves it takes the user's peice to caputure all of the
#  opposing pawns. This mode implements a priority queue-based Breadth-first search.
#
# @author Marco Bohorquez


# dictionaries for position(column) lookup
chess_columns_aN = {'a': 1,
                 'b': 2,
                 'c': 3,
                 'd': 4,
                 'e': 5,
                 'f': 6,
                 'g': 7,
                 'h': 8
                }

chess_columns_Na = {1: 'a',
                 2: 'b',
                 3: 'c',
                 4: 'd',
                 5: 'e',
                 6: 'f',
                 7: 'g',
                 8: 'h'
                }



# The main method validates user input, creates a chess piece,
#  and will run one of three modes within the program: 
#  Standard, Target, or Collector.
main_method_not_tested = '''
def main():

    # read and parse user input
    parser = argparse.ArgumentParser(description='Process chess input.')
    parser.add_argument('--piece', required=True, help='Type of chess piece')
    parser.add_argument('--position', required=True, help='Starting position of chess piece')

    # create mutually exclusive target and collect modes
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--target', action='store_true', help='Enable Target mode')
    modes.add_argument('--collect', action='store_true', help='Enable Collect mode')
    args = parser.parse_args()

    # create tuple for validating chess piece
    pieces_allowed = ('QUEEN', 'ROOK', 'KNIGHT')

    # validate chess piece
    valid_piece = False
    if vars(args).get('piece').upper() not in pieces_allowed:
        print('Chess piece "{}" not accepted. Please try again.'.format(vars(args).get('piece')))
    else:
        valid_piece = True

    # validate position
    valid_position = is_valid_position( vars(args).get('position') )
    if not valid_position:
        print('Position {} not accepted. Please try again.'.format(vars(args).get('position')))

    # if the piece and postition are both valid, run the program
    if valid_piece and valid_position:

        # create the specified chess piece
        if vars(args).get('piece').upper() == 'QUEEN':
            my_chess_piece = Queen(vars(args).get('position'))
        elif vars(args).get('piece').upper() == 'ROOK':
            my_chess_piece = Rook(vars(args).get('position'))
        elif vars(args).get('piece').upper() == 'KNIGHT':
            my_chess_piece = Knight(vars(args).get('position'))

        # run target or collect mode if specifcied, else run standard mode
        if args.target:
            target_mode(my_chess_piece)
        elif args.collect:
            collector_mode(my_chess_piece)
        else:
            possible_moves = ', '.join(my_chess_piece.calculate_possible_moves())
            print(possible_moves)
'''


# This method runs Target mode where we place our chess piece,
#  place 8 pawns randomly on the board, and calculate the minimum
#  set of moves it takes for our piece to get to the farthest
#  space on the board.
def target_mode(my_piece):
    
    # create a new chessboard
    chessboard = new_board()
    
    # place 'Q','R', or 'K' on the board
    chessboard[my_piece.column-1][my_piece.row-1] = my_piece.icon
    
    # randomly generate 8 pawns and place them on the board
    opp_pieces = set_pawns(chessboard)
    
    print('')
    print_board(chessboard)
    
    # calculate farthest space from current position
    farthest = get_farthest(my_piece)
    print('\nFarthest space from current position: {}\tDistance: {:.2f}'.format(farthest[0], farthest[1]))
    
    # create the start and target spaces for BFS
    start = Space( my_piece.column, my_piece.row, 0)
    target = Space( chess_columns_aN.get(farthest[0][0]), int(farthest[0][1]), -1 )
    
    # calculate and print minimum number of moves from start to target
    number_of_moves = BFS(start, target, my_piece.piece_type, opp_pieces)
    print('Minimum # of {} moves from {} to {}: {}'.format(my_piece.piece_type, my_piece.position, farthest[0], number_of_moves))

    # return 1 after successful run (for testing)
    return 1


# This method runs Collector mode where we place our chess piece,
#  place 8 pawns randomly on the board, and calculate the minimum
#  set of moves it takes for our piece to capture all the opposing
#  pieces.
def collector_mode(my_piece):
    
    # create a new chessboard
    chessboard = new_board()
    
    # place 'Q','R', or 'K' on the board
    chessboard[my_piece.column-1][my_piece.row-1] = my_piece.icon
    
    # randomly generate 8 pawns and place them on the board
    opp_pieces = set_pawns(chessboard)
    
    print('')
    print_board(chessboard)
    
    # create the start space for BFS_pq
    start = Space( my_piece.column, my_piece.row, 0, [], opp_pieces )
    
    # calculate and print minimum moves to capture all opp pieces
    min_moves = BFS_pq(start, my_piece.piece_type, opp_pieces)
    print('Minimum # of {} moves: {}'.format(my_piece.piece_type, min_moves[0]))
    print('Moves: ' + str(min_moves[1]))

    # return 1 after successful run (for testing)
    return 1



# This is a base class for the chess pieces in this program.
# Its attributes are position, column, and row. It has two
# class variables, piece type and icon.
class ChessPiece:

    piece_type = ''
    icon = ''
    
    def __init__(self, position):
        
        # position is a string (ex:'e4')
        self.position = position
        
        # column/row are integers from 1-8
        self.column = chess_columns_aN.get(position[0])
        self.row = int(position[1])


# The Queen can target spaces in its file(column), row, or diagonals.
class Queen(ChessPiece):

    piece_type = 'QUEEN' 
    icon = '\u2655'
    
    def __init__(self, position):
        super().__init__(position)
    
    # This method returns a list of moves that can be targeted by this
    #  Queen. Based on the provided list of opposing pieces, this Queen's
    #  'line of sight' ends if there is an opposing piece in the way.
    def calculate_possible_moves(self, opp_pieces=[]):

        # the list of possible moves to be returned
        moves = []
        
        # add spaces North of Queen until end of board or pawn is reached
        for x in range (self.row+1, 9):
            space = '{}{}'.format( chess_columns_Na.get(self.column), x)
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces NE of Queen until end of board or pawn is reached
        for x in range( 1, 9 - max(self.column, self.row) ) :
            space = '{}{}'.format( chess_columns_Na.get(self.column+x), self.row+x )
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces East of Queen until end of board or pawn is reached
        for x in range (self.column+1, 9):
            space = '{}{}'.format( chess_columns_Na.get(x), self.row )
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces SE of Queen until end of board or pawn is reached
        for x in range( 1, min(8-self.column+1, self.row) ):
            space = '{}{}'.format(chess_columns_Na.get(self.column+x), self.row-x)
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces South of Queen until end of board or pawn is reached
        for x in range (self.row-1, 0, -1):
            space = '{}{}'.format( chess_columns_Na.get(self.column), x)
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces SW of Queen until end of board or pawn is reached
        for x in range( 1, min(self.column, self.row) ):
            space = '{}{}'.format( chess_columns_Na.get(self.column-x), self.row-x)
            moves.append(space)
            if space in opp_pieces:
                break
        
        # add spaces West of Queen until end of board or pawn is reached
        for x in range (self.column-1, 0, -1):
            space = '{}{}'.format( chess_columns_Na.get(x), self.row )
            moves.append(space)
            if space in opp_pieces:
                break
        
        # add spaces NW of Queen until end of board or pawn is reached
        for x in range(1, min(self.column, 9-self.row)):
            space = '{}{}'.format( chess_columns_Na.get(self.column-x), self.row+x)
            moves.append(space)
            if space in opp_pieces:
                break
            
        return moves


# The Rook can target spaces in its file(column) or row.
class Rook(ChessPiece):

    piece_type = 'ROOK'
    icon = '\u2656'
    
    def __init__(self, position):
        super().__init__(position)
    
    # This method returns a list of moves that can be targeted by this
    #  Rook. Based on the provided list of opposing pieces, this Rook's
    #  'line of sight' ends if there is an opposing piece in the way.
    def calculate_possible_moves(self, opp_pieces=[]):

        # the list of possible moves to be returned
        moves = []
        
        # add spaces North of Rook until end of board or pawn is reached
        for x in range (self.row+1,9):
            space = '{}{}'.format( chess_columns_Na.get(self.column), x)
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces East of Rook until end of board or pawn is reached
        for x in range (self.column+1,9):
            space = '{}{}'.format( chess_columns_Na.get(x), self.row )
            moves.append(space)
            if space in opp_pieces:
                break
            
        # add spaces South of Rook until end of board or pawn is reached
        for x in range (self.row-1, 0, -1):
            space = '{}{}'.format( chess_columns_Na.get(self.column), x)
            moves.append(space)
            if space in opp_pieces:
                break
        
        # add spaces West of Rook until end of board or pawn is reached
        for x in range (self.column-1, 0, -1):
            space = '{}{}'.format( chess_columns_Na.get(x), self.row )
            moves.append(space)
            if space in opp_pieces:
                break
            
        return moves


# The Knight can move two squares vertically and one square horizontally
#  or two squares horizontally and one square vertically, jumping over 
#  other pieces.
class Knight(ChessPiece):

    piece_type = 'KNIGHT'
    icon = '\u2658'
    
    def __init__(self, position):
        super().__init__(position)
        
    # This method returns a list of moves that can be targeted by this
    #  Knight. The knight can jump over other pieces so its movement is
    #  not 'blocked' by other pieces.
    def calculate_possible_moves(self, opp_pieces=[]):

        # the list of possible moves to be returned
        moves = []
        
        for r in [-2,2]:
            for c in [-1,+1]:
                space = '{}{}'.format( chess_columns_Na.get(self.column + c), self.row + r )
                if is_valid_position(space):
                    moves.append(space)

        for r in [-1,1]:
            for c in [-2,2]:
                space = '{}{}'.format( chess_columns_Na.get(self.column + c), self.row + r )
                if is_valid_position(space):
                    moves.append(space)
                    
        return moves


# This class represents a space on the chess board for our queue.
#  This stores x and y attributes, a chess position, and the number
#  of moves that have been taken to get to get to this space 
#  from the origin.
#  A list of the spaces reached prior to this one and a list 
#  of opposing pawns on the board can also be provided for
#  use in a priority queue.
class Space:
    
    def __init__(self, x, y, moves, past_spaces=[], pawns=[]):
        self.x = x
        self.y = y
        self.pos = str( chess_columns_Na.get(x)) + str(y)
        self.moves = moves
        self.past_spaces = past_spaces
        self.pawns = pawns
    
    # This method returns a priority value based on whether it is
    #  a "capture" space. "Capture" spaces will be pushed to the
    #  front of the pqueue while non-"capture" spaces get
    #  pushed to the back.
    def prioritize(self, counter):

        # The prioty value is the negative or positive value
        #  of the counter from the BFS loop. This way, no two
        #  spaces end up with the same priority value.
        if self.pos not in self.pawns:
            index = counter
        else:
            index = -counter

        return index


# This method implements a queue and conducts a Breadth-first search 
#  to find the minimum number of moves it takes to get from start to
#  target. This method also takes piece type, and opposing pieces as 
#  parameters. The minimum number of moves is returned as an integer.
def BFS(start, target, piece_type, opp_pieces):
    
    # keep a list of visited spaces
    visited = []
    
    # initialize queue 
    q = Queue()
    
    # add the starting space
    q.put(start)
    
    # begin Breadth-first search
    while(not q.empty()):
        
        # pop first space in queue
        front = q.get()
        
        # make a temp piece to calculate the valid next spaces
        if piece_type == 'QUEEN':
            temp_piece = Queen( chess_columns_Na.get(front.x) + str(front.y) )
            
        if piece_type == 'ROOK':
            temp_piece = Rook( chess_columns_Na.get(front.x) + str(front.y) )
            
        if piece_type == 'KNIGHT':
            temp_piece = Knight( chess_columns_Na.get(front.x) + str(front.y) )
            
        # get valid next spaces for the piece in the current position
        valid_next_spaces = temp_piece.calculate_possible_moves(opp_pieces)
        
        # return # of moves if target position is reached
        if front.x == target.x and front.y == target.y:
            return front.moves
        
        # otherwise, begin traversing all valid next spaces
        for i in range(0, len(valid_next_spaces)):
            
            next_x = chess_columns_aN.get(valid_next_spaces[i][0])
            next_y = int(valid_next_spaces[i][1])
            
            # create string representation of next position
            search = '{}{}'.format(chess_columns_Na.get(next_x), next_y)
            
            # if next space hasn't been visited already and is a valid position, add it to the queue
            if search not in visited and is_valid_position(search):
                
                next = Space(next_x, next_y, front.moves+1)
                q.put(next)
                visited.append(search)
              
    # this line would be reached if the queue gets empty, which it shouldn't  
    return 0


# This method implements a priority queue and conducts a Breadth-first 
#  search to find the minimum number of moves it takes a chess piece 
#  to capture all the opposing pieces on the board. The pqueue
#  prioritizes spaces where a capture is available. The minimum
#  number of moves and the actual list of moves are returned as a tuple.
def BFS_pq(start, piece_type, opp_pieces):
        
    # initialize heap for priority queue
    h = []
    
    # counter used for prioritization
    heap_index = 1

    # add the starting space as a tuple
    heapq.heappush(h, (start.prioritize(heap_index), start) )
    
        
    # begin Breadth-first search
    while(len(h) > 0):
                
        # pop first space in pqueue
        front = heapq.heappop(h)
        
        # update front's list of past spaces to include current space
        past_spaces = front[1].past_spaces.copy()
        past_spaces.append( front[1].pos )
        front[1].past_spaces = past_spaces
        
        # make a temp piece to calculate the valid next spaces
        if piece_type == 'QUEEN':
            temp_piece = Queen( front[1].pos )
            
        if piece_type == 'ROOK':
            temp_piece = Rook( front[1].pos )
            
        if piece_type == 'KNIGHT':
            temp_piece = Knight( front[1].pos )
            
        # remove pawn from front's pawn list if captured
        if front[1].pos in front[1].pawns:
            front[1].pawns.remove(front[1].pos)        
            
        # get valid next spaces for the piece in the current position
        valid_next_spaces = temp_piece.calculate_possible_moves(front[1].pawns)
        
        # return number of moves if all pawn spaces have been reached
        check = all(item in front[1].past_spaces for item in opp_pieces)
        
        if check:
            # return tuple containing # of moves, and list of moves
            return (front[1].moves, front[1].past_spaces)
        
        # otherwise, traverse all valid next spaces
        for i in range(0, len(valid_next_spaces)):
            
            # increment heap index for prioritization
            heap_index = heap_index + 1
            
            # calculate the next target space
            next_x = chess_columns_aN.get(valid_next_spaces[i][0])
            next_y = int(valid_next_spaces[i][1])
            
            # create string representation of next position
            search = '{}{}'.format(chess_columns_Na.get(next_x), next_y)
            
            # if next space hasn't been visited already and is a valid position,, add it to the pqueue
            if search not in front[1].past_spaces and is_valid_position(search):
                next = Space(next_x, next_y, front[1].moves+1, front[1].past_spaces, front[1].pawns.copy())
                heapq.heappush(h, (next.prioritize(heap_index), next) )
       
    # this line would be reached if the heap gets empty, which it shouldn't     
    return 0


# This method checks if a given postion is a real position on the board
def is_valid_position(pos):

    if len(pos) != 2:
        return False

    if pos[0].lower() not in 'abcdefgh' or pos[1] not in '12345678':
        return False

    return True


# This method generates a chessboard and returns a list of lists
#  where all spaces are 'empty' and marked by a '.'
def new_board():
    board = []
    for x in range(0,8):
        board.append( ['.','.','.','.','.','.','.','.'] )
    return board


# This method takes a board parameter and prints out a string
#  representation of the chessboard in its current state.
def print_board(board):
    for row in range(7, -1, -1):    
        row_string = str(row+1) + ' '
        for col in range(0,8):
            row_string = row_string + board[col][row] + ' '
        print(row_string)
    print('  a b c d e f g h')


# This method checks a postion on a board and returns its current value.
#  This value may be a chess piece or '.'
def get_position(board, position):
    return board[ chess_columns_aN.get(position[0])-1 ][ int(position[1])-1 ]


# This method generates 8 pawns and randomly places them on the given board.
#  This method returns a list of the pawns' postions.
def set_pawns(board):

    # the list of pawn positions to be returned
    pawns = []

    # generate random positions for the 8 pawns
    while len(pawns) < 8:
        pos = chess_columns_Na.get(random.randint(1,8)) + str(random.randint(1,8))
        
        # if no other piece is in the position, place the pawn and add its position to the list
        if get_position(board, pos) == '.':
            board[ chess_columns_aN.get(pos[0])-1 ][ int(pos[1])-1 ] = '\u265F'
            pawns.append(pos)
            
    return pawns


# This method calculates and returns the farthest space on the board from the given piece.
def get_farthest(piece):

    # the list to be returned
    farthest = ['',0]

    # calculate the distance between each space and the given piece
    for x in range(1,9):
        for y in range(1,9):
            distance = math.dist( [piece.column, piece.row], [x,y] )
            
            # update the list when this space is farther from the piece than what is 
            #  currently in the list
            if distance > farthest[1]:
                farthest[0] = chess_columns_Na.get(x) + str(y)
                farthest[1] = distance
                
    return farthest


# The __name__method runs automatically when this file is run directly
#  and calls the main method.
name_not_tested = '''
if __name__ == '__main__':
		main()
'''