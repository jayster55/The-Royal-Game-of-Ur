import math
from agent import Piece

DEBUG = False

def winGame(state):
    # needs to determine if the board is a win-state or not
    # search through board array, set boolean values
    board = state[0]
    win = False
    blackEmpty = False #No more captured pieces
    whiteEmpty = False #No more captured pieces

    unplayedBlackPices = state[1]
    unplayedWhitePices = state[2]


    if unplayedBlackPices == 0:
        blackEmpty = True
    if unplayedWhitePices == 0:
        whiteEmpty = True


    boardEmptyOfBlackTiles = True
    boardEmptyOfWhiteTiles = True

    # Finds any pieces on board
    for i in board:
        if i == Piece.Black:
            boardEmptyOfBlackTiles = False
        elif i == Piece.White:
            boardEmptyOfWhiteTiles = False

    if blackEmpty and boardEmptyOfBlackTiles:
        win = True
        if DEBUG: print("Black Won")
    elif whiteEmpty and boardEmptyOfWhiteTiles:
        if DEBUG: print("White Won")
        win = True
    else: #no win
        # if(DEBUG): print("No Winner Yet")
        win = False

    return win
