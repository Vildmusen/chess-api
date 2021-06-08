King_W = '♚'   # 1
Queen_W = '♛'  # 2
Bishop_W = '♝' # 3
Knight_W = '♞' # 4
Rook_W = '♜'   # 5
Pawn_W = '♟︎'   # 6
King_B = '♔'   # 7
Queen_B = '♕'  # 8
Bishop_B = '♗' # 9
Knight_B = '♘' # 10
Rook_B = '♖'   # 11
Pawn_B = '♙'   # 12

pieces = [' ', '♚', '♛', '♝', '♞', '♜', '♟︎', '♔', '♕', '♗', '♘', '♖', '♙']

knight_ranges = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
bishop_ranges = [[1,1], [1,-1], [-1,1], [-1,-1]]
queen_ranges = [[0,1],[0,-1],[1,-1],[1,0],[1,1],[-1,-1],[-1,0],[-1,1]]
rook_ranges = [[0,1],[1,0],[-1,0],[0,-1]]

class Move:
    def __init__(self, start, end, is_enpassant=False):
        self.startpos = start
        self.endpos = end
        self.is_enpassant = is_enpassant

class Piece:
    def __init__(self, pos, val):
        self.pos = pos
        self.piece = pieces[val]
        self.val = val
        self.passantable = False

    def get_piece(self):
        return self.piece


class Board:
    def __init__(self, pieces):
        if(len(pieces) == 0):
            self.pieces = [
                Piece([0,0], 5),
                Piece([1,0], 4),
                Piece([2,0], 3),
                Piece([3,0], 2),
                Piece([4,0], 1),
                Piece([5,0], 3),
                Piece([6,0], 4),
                Piece([7,0], 5),
                Piece([0,1], 6),
                Piece([1,1], 6),
                Piece([2,1], 6),
                Piece([3,1], 6),
                Piece([4,1], 6),
                Piece([5,1], 6),
                Piece([6,1], 6),
                Piece([7,1], 6),
                Piece([0,6], 12),
                Piece([1,6], 12),
                Piece([2,6], 12),
                Piece([3,6], 12),
                Piece([4,6], 12),
                Piece([5,6], 12),
                Piece([6,6], 12),
                Piece([7,6], 12),
                Piece([0,7], 11),
                Piece([1,7], 10),
                Piece([2,7], 9),
                Piece([4,7], 7),
                Piece([3,7], 8),
                Piece([5,7], 9),
                Piece([6,7], 10),
                Piece([7,7], 11)
            ]
        else:
            self.pieces = pieces
        self.captures = []
    
    def get_piece(self, x, y):
        for piece in self.pieces:
            if(piece.pos[0] == x and piece.pos[1] == y):
                return piece
        return Piece(-1, 0)

    def get_piece_on_val(self, val):
        for piece in self.pieces:
            if(piece.val == val):
                return piece
        return Piece(-1, 0)

    def print_board(self):
        print()
        print("   _______________________ ")
        print("  |──|──|──|──|──|──|──|──|")
        
        for i in range(8):
            rank = abs((i)-8)
            print(str(rank) + ' ', end='')
            for j in range(8):
                cur = self.get_piece(j, rank-1)
                print('|' + cur.get_piece() + ' ', end='')
            print("|")        
            print("  |──|──|──|──|──|──|──|──|")
        
        print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
        print("   A  B  C  D  E  F  G  H  ")
        print()

    def empty_square(self, x, y):
        for piece in self.pieces:
            if(piece.pos[0] == x and piece.pos[1] == y):
                return False
        return True

    def danger_squares(self, sign):
        death = []
        for piece in self.pieces:
            x = piece.pos[0]
            y = piece.pos[1]
            if(piece.val == 9-(3*sign)):
                death.append([x-1, y+(1*sign)])
                death.append([x+1, y+(1*sign)])
            if(piece.val == 7-(3*sign)):
                for move_set in knight_ranges:
                    death.append([x+move_set[0], y+move_set[1]])
            if(piece.val == 6-(3*sign)):
                for move_set in bishop_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    while(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        death.append([d_x, d_y])
                        d_x += move_set[0]
                        d_y += move_set[1]
                    death.append([d_x, d_y])
            if(piece.val == 5-(3*sign)):
                for move_set in queen_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    while(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        death.append([d_x, d_y])
                        d_x += move_set[0]
                        d_y += move_set[1]
                    death.append([d_x, d_y])
            if(piece.val == 4-(3*sign)):
                for move_set in queen_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    death.append([d_x, d_y])
            if(piece.val == 8-(3*sign)):
                for move_set in rook_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    while(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        death.append([d_x, d_y])
                        d_x += move_set[0]
                        d_y += move_set[1]
                    death.append([d_x, d_y])
        return death

    def all_legal_moves(self, sign):
        legal_moves = []
        legal_moves_notation = []

        if(sign == -1):
            piece_range = [7,8,9,10,11,12] # black pieces
        else:
            piece_range = [1,2,3,4,5,6] # white pieces

        for piece in self.pieces:
           
            x = piece.pos[0]
            y = piece.pos[1]

            # all pawn moves
            if(piece.val == 9-(3*sign)): # 9 - 3 = 6 = white pawn, 9 + 3 = 12 = black pawn

                if(self.empty_square(x, y+(1*sign))): # one step
                    legal_moves_notation.append(coord_to_letter(x)+str(y+(1*sign)+1))
                    legal_moves.append(Move([x,y],[x,y+(1*sign)]))

                if(y == 3.5-(2.5*sign) and self.empty_square(x, y+(1*sign)) and self.empty_square(x, y+(2*sign))): # two steps
                    legal_moves_notation.append(coord_to_letter(x)+str(y+(2*sign)+1))
                    legal_moves.append(Move([x,y],[x,y+(2*sign)]))

                if(self.get_piece(x+(1*sign), y+(1*sign)).val not in piece_range and self.get_piece(x+(1*sign), y+(1*sign)).val != 0): # capture right
                    legal_moves_notation.append(coord_to_letter(x)+'x'+coord_to_letter(x+(1*sign))+str(y+(1*sign)+1))
                    legal_moves.append(Move([x,y],[x+(1*sign),y+(1*sign)]))
                
                if(self.get_piece(x-(1*sign), y+(1*sign)).val not in piece_range and self.get_piece(x-(1*sign), y+(1*sign)).val != 0): # capture left
                    legal_moves_notation.append(coord_to_letter(x)+'x'+coord_to_letter(x-(1*sign))+str(y+(1*sign)+1))
                    legal_moves.append(Move([x,y],[x-(1*sign),y+(1*sign)]))
                
                if(self.get_piece(x+(1*sign), y+(1*sign)).val == 0 and self.get_piece(x+(1*sign), y).passantable): # passant right
                    legal_moves_notation.append(coord_to_letter(x)+'x'+coord_to_letter(x+(1*sign))+str(y+(1*sign)+1))
                    legal_moves.append(Move([x,y],[x+(1*sign),y+(1*sign)], True))

                if(self.get_piece(x-(1*sign),y+(1*sign)).val == 0 and self.get_piece(x-(1*sign), y).passantable): # passant left
                    legal_moves_notation.append(coord_to_letter(x)+'x'+coord_to_letter(x-(1*sign))+str(y+(1*sign)+1))
                    legal_moves.append(Move([x,y],[x-(1*sign),y+(1*sign)], True))

        
            # all horsie moves
            if(piece.val == 7-(3*sign)): # 7 - 3 = white knight, 7 + 3 = black knight
                for move_set in knight_ranges:
                    if(self.get_piece(x+move_set[0], y+move_set[1]).val not in piece_range and self.get_piece(x+move_set[0], y+move_set[1]).val == 0 and in_range(x+move_set[0],y+move_set[1])):
                        legal_moves_notation.append('N'+coord_to_letter(x+move_set[0])+str(y+move_set[1]+1))
                        legal_moves.append(Move([x,y],[x+move_set[0],y+move_set[1]]))
                    if(self.get_piece(x+move_set[0], y+move_set[1]).val not in piece_range and self.get_piece(x+move_set[0], y+move_set[1]).val != 0 and in_range(x+move_set[0],y+move_set[1])):
                        legal_moves_notation.append('Nx'+coord_to_letter(x+move_set[0])+str(y+move_set[1]+1))
                        legal_moves.append(Move([x,y],[x+move_set[0],y+move_set[1]]))

            # all bishop moves
            if(piece.val == 6-(3*sign)):
                for move_set in bishop_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    while(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        legal_moves_notation.append('B'+coord_to_letter(d_x)+str(d_y+1))
                        legal_moves.append(Move([x,y],[d_x,d_y]))
                        d_x += move_set[0]
                        d_y += move_set[1]
                    if(self.get_piece(d_x, d_y).val not in piece_range and in_range(d_x, d_y)):
                        legal_moves_notation.append('Bx'+coord_to_letter(d_x)+str(d_y+1))  
                        legal_moves.append(Move([x,y],[d_x,d_y]))

            # queen moves
            if(piece.val == 5-(3*sign)):
                for move_set in queen_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    while(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        legal_moves_notation.append('Q'+coord_to_letter(d_x)+str(d_y+1))
                        legal_moves.append(Move([x,y],[d_x,d_y]))
                        d_x += move_set[0]
                        d_y += move_set[1]
                    if(self.get_piece(d_x, d_y).val not in piece_range and in_range(d_x, d_y)):
                        legal_moves_notation.append('Qx'+coord_to_letter(d_x)+str(d_y+1))  
                        legal_moves.append(Move([x,y],[d_x,d_y]))

            # rook moves
            if(piece.val == 8-(3*sign)):
                for move_set in rook_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    while(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        legal_moves_notation.append('R'+coord_to_letter(d_x)+str(d_y+1))
                        legal_moves.append(Move([x,y],[d_x,d_y]))
                        d_x += move_set[0]
                        d_y += move_set[1]
                    if(self.get_piece(d_x, d_y).val not in piece_range and in_range(d_x, d_y)):
                        legal_moves_notation.append('Rx'+coord_to_letter(d_x)+str(d_y+1))
                        legal_moves.append(Move([x,y],[d_x,d_y]))

            # king moves               
            if(piece.val == 4-(3*sign)):
                for move_set in queen_ranges:
                    d_x = x+move_set[0]
                    d_y = y+move_set[1]
                    if(self.get_piece(d_x, d_y).val == 0 and in_range(d_x, d_y)):
                        legal_moves_notation.append('K'+coord_to_letter(d_x)+str(d_y+1))
                        legal_moves.append(Move([x,y],[d_x,d_y]))
                    if(self.get_piece(d_x, d_y).val != 0 and self.get_piece(d_x, d_y).val not in piece_range and in_range(d_x, d_y)):
                        legal_moves_notation.append('Kx'+coord_to_letter(d_x)+str(d_y+1))  
                        legal_moves.append(Move([x,y],[d_x,d_y]))
                                

        # REMOVE DANGEROUS (NON-LEGAL) MOVES
        to_remove_moves = []
        to_remove_notation = []

        for i in range(len(legal_moves)):
            move = legal_moves[i]
            notation = legal_moves_notation[i]
            if(puts_king_in_danger(self, move, sign)):
                to_remove_moves.append(move)
                to_remove_notation.append(notation)
                

        for i in range(len(to_remove_moves)):
            legal_moves.remove(to_remove_moves[i])
            legal_moves_notation.remove(to_remove_notation[i])

        return legal_moves, legal_moves_notation


    def make_move(self, move, sign):
        cur_piece = self.get_piece(move.startpos[0], move.startpos[1])
        target_piece = self.get_piece(move.endpos[0], move.endpos[1])
        if(target_piece.val != 0):
            self.captures.append(target_piece)
            self.pieces.remove(target_piece)
        if(cur_piece.val == 6 and cur_piece.pos[1] == 1 and move.endpos[1] - cur_piece.pos[1] == 2):
            cur_piece.passantable = True
        if(cur_piece.val == 12 and cur_piece.pos[1] == 6 and cur_piece.pos[1] - move.endpos[1] == 2):
            cur_piece.passantable = True
        if(move.is_enpassant):
            self.pieces.remove(self.get_piece(move.endpos[0], move.endpos[1]-(1*sign)))
        cur_piece.pos = move.endpos



# Helpers

def puts_king_in_danger(board, move, sign):
    temp_list = []
    for piece in board.pieces:
        temp_piece = Piece(piece.pos, piece.val)
        temp_list.append(temp_piece)
    temp = Board(temp_list)
    temp.make_move(move, sign)
    if(sign == -1):
        death_squares = temp.danger_squares(1)
    else:
        death_squares = temp.danger_squares(-1)
    return temp.get_piece_on_val(4-(3*sign)).pos in death_squares

def letter_to_coord(coord):
    if(coord == 'a'): return 0
    if(coord == 'b'): return 1
    if(coord == 'c'): return 2
    if(coord == 'd'): return 3
    if(coord == 'e'): return 4
    if(coord == 'f'): return 5
    if(coord == 'g'): return 6
    if(coord == 'h'): return 7
    return -1

def coord_to_letter(num):
    if(num == 0): return 'a'
    if(num == 1): return 'b'
    if(num == 2): return 'c'
    if(num == 3): return 'd'
    if(num == 4): return 'e'
    if(num == 5): return 'f'
    if(num == 6): return 'g'
    if(num == 7): return 'h'
    return 'ö'

def in_range(x,y):
    return x < 8 and x >= 0 and y < 8 and y >= 0