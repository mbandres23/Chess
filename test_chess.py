import unittest
from chess import Queen, Rook, Knight, Space, is_valid_position, get_farthest, target_mode, collector_mode

# This class tests the different chess piece and space objects in chess.py,
#  as well as some of the helper methods and "run modes" in the program.
#
# @author Marco Bohorquez 
class TestChess(unittest.TestCase):

    # Test Queen initialization
    def test_Queen_0(self):

        positions = []

        for i in range(4):

            # initialize a Queen
            pos = 'e' + str(i)
            test_queen = Queen( pos )

            # store the position into the list variable
            positions.append(pos)
            
            # check if the queen's attributes were properly initiated
            self.assertIsNotNone( test_queen.piece_type )
            self.assertIsNotNone( test_queen.position )

            self.assertEqual( test_queen.piece_type, 'QUEEN' )
            self.assertEqual( test_queen.position, positions[i] )

            self.assertEqual( test_queen.icon, '\u2655' )


    # Test Queen's calculate_possible_moves method on an empty board
    def test_Queen_1(self):

        # these are some positions around the board with the expected number of moves
        #  available for the queen, assuming no other pieces are on the board
        positions = {'e4': 27,
                     'a1': 21, 
                     'a8': 21,
                     'h1': 21,
                     'h8': 21,
                     'b2': 23,
                     'b7': 23,
                     'g2': 23,
                     'g7': 23
                     }

        # create a queen for each position
        for pos in positions.keys():

            test_queen = Queen( pos )

            # check the number of moves calculated against our dictionary
            moves = test_queen.calculate_possible_moves()
            self.assertEqual( len(moves), positions.get(pos) )


    # Test Queen's calculate_possible_moves method on a board with pawns
    def test_Queen_2(self):

        # create some positions surrounded by pawns with the expected number
        #  of moves available for the queen
        positions = {'e4': [ ['e5','f5','f4','f3','e3','d3','d4','d5'], 8 ],
                     'a1': [ ['a2','b2','b1'], 3], 
                     'a8': [ ['b8','b7','a7'], 3],
                     'h1': [ ['g1','g2','h2'], 3],
                     'h8': [ ['g8','g7','h7'], 3]
                     }

        # create a queen for each position
        for pos in positions.keys():

            test_queen = Queen( pos )

            # check the number of moves calculated against our dictionary
            moves = test_queen.calculate_possible_moves( positions.get(pos)[0] )
            self.assertEqual( len(moves), positions.get(pos)[1] )


    # Test Rook initialization
    def test_Rook_0(self):

        positions = []

        for i in range(4):

            # initialize a Rook
            pos = 'e' + str(i)
            test_rook = Rook( pos )

            # store the position into the list variable
            positions.append(pos)
            
            # check if the rook's attributes were properly initiated
            self.assertIsNotNone( test_rook.piece_type )
            self.assertIsNotNone( test_rook.position )

            self.assertEqual( test_rook.piece_type, 'ROOK' )
            self.assertEqual( test_rook.position, positions[i] )

            self.assertEqual( test_rook.icon, '\u2656' )


    # Test Rook's calculate_possible_moves method on an empty board
    def test_Rook_1(self):

        # these are some positions around the board with the expected number of moves
        #  available for the rook, assuming no other pieces are on the board
        positions = {'e4': 14,
                     'a1': 14, 
                     'a8': 14,
                     'h1': 14,
                     'h8': 14,
                     'b2': 14,
                     'b7': 14,
                     'g2': 14,
                     'g7': 14
                     }

        # create a rook for each position
        for pos in positions.keys():

            test_rook = Rook( pos )

            # check the number of moves calculated against our dictionary
            moves = test_rook.calculate_possible_moves()
            self.assertEqual( len(moves), positions.get(pos) )


    # Test Rook's calculate_possible_moves method on a board with pawns
    def test_Rook_2(self):

        # create some positions surrounded by pawns with the expected number
        #  of moves available for the rook
        positions = {'e4': [ ['e5','f4','e3','d4'], 4 ],
                     'a1': [ ['a2','b1'], 2], 
                     'a8': [ ['b8','a7'], 2],
                     'h1': [ ['g1','h2'], 2],
                     'h8': [ ['g8','h7'], 2]
                     }

        # create a rook for each position
        for pos in positions.keys():

            test_rook = Rook( pos )

            # check the number of moves calculated against our dictionary
            moves = test_rook.calculate_possible_moves( positions.get(pos)[0] )
            self.assertEqual( len(moves), positions.get(pos)[1] )


    # Test Knight initialization
    def test_Knight_0(self):

        positions = []

        for i in range(4):

            # initialize a Knight
            pos = 'e' + str(i)
            test_knight = Knight( pos )

            # store the position into the list variable
            positions.append(pos)
            
            # check if the knight's attributes were properly initiated
            self.assertIsNotNone( test_knight.piece_type )
            self.assertIsNotNone( test_knight.position )

            self.assertEqual( test_knight.piece_type, 'KNIGHT' )
            self.assertEqual( test_knight.position, positions[i] )

            self.assertEqual( test_knight.icon, '\u2658' )


    # Test Knight's calculate_possible_moves method on an empty board
    def test_Knight_1(self):

        # these are some positions around the board with the expected number of moves
        #  available for the knight, assuming no other pieces are on the board
        positions = {'e4': 8,
                     'a1': 2, 
                     'a8': 2,
                     'h1': 2,
                     'h8': 2,
                     'b2': 4,
                     'b7': 4,
                     'g2': 4,
                     'g7': 4
                     }

        # create a knight for each position
        for pos in positions.keys():

            test_knight = Knight( pos )

            # check the number of moves calculated against our dictionary
            moves = test_knight.calculate_possible_moves()
            self.assertEqual( len(moves), positions.get(pos) )


    # Test Knight's calculate_possible_moves method on a board with pawns
    def test_Knight_2(self):

        # create some positions surrounded by pawns with the expected number
        #  of moves available for the knight
        positions = {'e4': [ ['d6','f6','c5','g5','c3','g3','d2','f2'], 8 ],
                     'a1': [ ['b3','c2'], 2], 
                     'a8': [ ['b6','c7'], 2],
                     'h1': [ ['f2','g3'], 2],
                     'h8': [ ['f7','g6'], 2]
                     }

        # create a knight for each position
        for pos in positions.keys():

            test_knight = Knight( pos )

            # check the number of moves calculated against our dictionary
            moves = test_knight.calculate_possible_moves( positions.get(pos)[0] )
            self.assertEqual( len(moves), positions.get(pos)[1] )


    # Test Space initialization with required parameters only
    def test_Space_0(self):

        # test all possible x,y coordinates on the chess board
        x_coordinates = []
        y_coordinates = []

        for x in '12345678':
            for y in '12345678':
                x_coordinates.append(int(x))
                y_coordinates.append(int(y))

        # test the pos attribute of each space against of list of
        #  every chess position
        valid_positions = []

        for x in 'abcdefgh':
            for y in '12345678':
                valid_positions.append(x+y)


        # check if space's attributes were properly initiated
        for i in range(64):
            test_space = Space( x_coordinates[i], y_coordinates[i], [] )

            self.assertIsNotNone( test_space.x )
            self.assertIsNotNone( test_space.y )
            self.assertIsNotNone( test_space.pos )
            self.assertIsNotNone( test_space.moves )

            self.assertEqual( test_space.x, x_coordinates[i] )
            self.assertEqual( test_space.y, y_coordinates[i] )
            self.assertEqual( test_space.pos, valid_positions[i] )
            self.assertEqual( test_space.moves, [] )            


    # Test Space initialization with and without its optional parameters
    def test_Space_1(self):

        # test with empty parameters
        test_space0 = Space( 5, 4, 2 )

        self.assertIsNotNone( test_space0.past_spaces )
        self.assertIsNotNone( test_space0.pawns )

        self.assertEqual( test_space0.past_spaces, [] )
        self.assertEqual( test_space0.pawns, [] )


        # test with non-empty parameters
        test_spaces = ['a1', 'b1', 'c1']
        test_pawns = ['h1', 'h2', 'h3']

        test_space1 = Space( 5, 4, 2, test_spaces, test_pawns )

        self.assertIsNotNone( test_space1.past_spaces )
        self.assertIsNotNone( test_space1.pawns )

        self.assertEqual( test_space1.past_spaces, test_spaces )
        self.assertEqual( test_space1.pawns, test_pawns )


    # Test Space's prioritize method used for the priority queue
    def test_Space_2(self):

        # mimics the counter during BFS_pq traversal
        test_counter = 5

        test_pawns0 = []
        test_pawns1 = ['e1','e2','e3','e4','e5','e6','e7','e8']


        # test prioritize() with no pawns (current pos is g7)
        test_space0 = Space( 7, 7, 2, ['g5','g6','g7'], test_pawns0 )
        self.assertEqual( test_space0.prioritize(test_counter), 5 )


        # test prioritize() with pawns, space is on a pawn square (current pos is e4)
        test_space1 = Space( 5, 4, 2, ['g4','f4','e4'], test_pawns1 )
        self.assertEqual( test_space1.prioritize(test_counter), -5 )


        # test prioritize() with pawns, space is not on a pawn square (current pos is b3)
        test_space2 = Space( 6, 3, 2, ['d3','e3','f3'], test_pawns1 )
        self.assertEqual( test_space2.prioritize(test_counter), 5 )


    def test_is_valid_position(self):

        # test all valid chess positions
        valid_positions = []

        for x in 'abcdefghABCDEFGH':
            for y in '12345678':
                valid_positions.append(x+y)

        for pos in valid_positions:
            self.assertTrue( is_valid_position(pos) )
        

        # test some different invalid inputs
        invalid_positions = [ '', ' ', '  ', 'e43', '~!','a0', '66', 'a9', 'e4 ', '6', 'e!' ]
        
        for pos in invalid_positions:
            self.assertFalse( is_valid_position(pos) )


    def test_get_farthest(self):

        # test a few positions on the board with their known farthest space
        positions = {'a1': 'h8',
                     'a8': 'h1',
                     'h1': 'a8',
                     'h8': 'a1',
                     'd4': 'h8',
                     'e4': 'a8',
                     'd5': 'h1',
                     'e5': 'a1'
                    }

        for test_pos in positions.keys():
            test_piece = Queen(test_pos)
            self.assertEqual( get_farthest(test_piece)[0], positions.get(test_piece.position) )


    # Test Target Mode with every piece type
    def test_target_mode_0(self):

        # run 10 tests with every chess position
        for x in 'abcdefgh':
            for y in '12345678':
                test_position = x + y

                for i in range(10):

                    test_queen = Queen(test_position)
                    test_rook = Rook(test_position)
                    test_knight = Knight(test_position)

                    run_output0 = target_mode( test_queen )
                    self.assertEqual( run_output0, 1 )

                    run_output1 = target_mode( test_rook )
                    self.assertEqual( run_output1, 1 )

                    run_output2 = target_mode( test_knight )
                    self.assertEqual( run_output2, 1 )


    # Test Collector Mode with every piece type
    def test_collector_mode_0(self):

        # run tests with a few chess positions
        test_positions = ['e4','a1', 'g7']

        for pos in test_positions:

            test_queen = Queen(pos)
            test_rook = Rook(pos)
            test_knight = Knight(pos)

            run_output0 = collector_mode( test_queen )
            self.assertEqual( run_output0, 1 )

            run_output1 = collector_mode( test_rook )
            self.assertEqual( run_output1, 1 )

            run_output2 = collector_mode( test_knight )
            self.assertEqual( run_output2, 1 )


if __name__ == '__main__':
	unittest.main()
