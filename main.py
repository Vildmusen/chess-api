import chess_utils as ch
import os

def main():
    '''
    Runs setup for a clean board and starts the game
    '''
    os.system('cls')

    chess_board = ch.Board([])
    chess_board.print_board()

    run(chess_board)

def run(chess_board):
    game_on = True
    playing = 1
    while(game_on):
        
        if(playing == 1):
            player = "W"
        else:
            player = "B"

        all_moves, all_moves_notation = chess_board.all_legal_moves(playing)
       
        if(len(all_moves) == 0):
            game_on = False
            break

        print("Legal moves:")
        for move in all_moves_notation:
            print(move + ". ", end='')
        print()        
        print()

        # for n in death_squares:
        #     print(str(ch.coord_to_letter(n[0]))+str(n[1]+1)+' - ')

        user_move = input("["+player+"] Make a move... \n")
        while(not user_move in all_moves_notation): # if invalid move
            os.system('cls')
            chess_board.print_board()
            print("Legal moves:")
            for move in all_moves_notation:
                print(move + ". ", end='')
            print()
            print()
            user_move = input("["+player+"] Invalid move, please try again... \n")
        
        chess_board.make_move(all_moves[all_moves_notation.index(user_move)], playing)
        
        os.system('cls')
        chess_board.print_board()
        
        # check if opponent has any legal moves
            # if not - Check mate!
 

        # change player
        if(playing == 1):
            playing = -1
        else:
            playing = 1
    
    print("Game over!")


if __name__ == "__main__":
    main()