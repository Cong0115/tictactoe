import numpy as np
import random
import time


def iif(cond, t, f):
    if cond:
        return t
    else:
        return f


def printboard(board):
    marker = ["", "X", "", "", "O"]
    boardout = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])
    for row in range(3):
        for col in range(3):
            if board[row, col] != 0:
                boardout[row, col] = marker[board[row, col]]
    print('------------------')
    print(" {} | {} | {}".format(
        boardout[0, 0], boardout[0, 1], boardout[0, 2]))
    print("-----------")
    print(" {} | {} | {}".format(
        boardout[1, 0], boardout[1, 1], boardout[1, 2]))
    print("-----------")
    print(" {} | {} | {}".format(
        boardout[2, 0], boardout[2, 1], boardout[2, 2]))
    print('------------------')


def getwinmove(board):
    winmove = []
    # check rows
    for row in range(3):
        if np.sum(board[row, :]) == 8:
            for col in range(3):
                if board[row, col] == 0:
                    winmove.append((row, col))
                    # break
    # check columns
    for col in range(3):
        if np.sum(board[:, col]) == 8:
            for row in range(3):
                if board[row, col] == 0:
                    winmove.append((row, col))
                    # break
    # check top-left to bottom-right
    if board[0, 0]+board[1, 1]+board[2, 2] == 8:
        for i in range(3):
            if board[i, i] == 0:
                winmove.append((i, i))
    # check top-right to bottom-left
    if board[0, 2]+board[1, 1]+board[2, 0] == 8:
        for i in range(3):
            if board[i, 2-i] == 0:
                winmove.append((i, 2-i))
    return winmove


def getblockmove(board):
    blockmove = []
    # check rows
    for row in range(3):
        if np.sum(board[row, :]) == 2:
            for col in range(3):
                if board[row, col] == 0:
                    blockmove.append((row, col))
                    # break
    # check columns
    for col in range(3):
        if np.sum(board[:, col]) == 2:
            for row in range(3):
                if board[row, col] == 0:
                    blockmove.append((row, col))
                    # break
    # check top-left to bottom-right
    if board[0, 0]+board[1, 1]+board[2, 2] == 2:
        for i in range(3):
            if board[i, i] == 0:
                blockmove.append((i, i))
    # check top-right to bottom-left
    if board[0, 2]+board[1, 1]+board[2, 0] == 2:
        for i in range(3):
            if board[i, 2-i] == 0:
                blockmove.append((i, 2-i))
    return blockmove


def getforkmove(board):
    forkmove = []
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                tempboard = np.copy(board)
                tempboard[row, col] = 4
                if len(getwinmove(tempboard)) > 1:
                    forkmove.append((row, col))
    return forkmove


def getplayermove(board):
    while True:
        pm = int(input('Your move (1-9)? '))
        if pm in range(1, 10):
            row = (pm-1)//3
            col = ((pm-1) % 3)
            if board[row, col] == 0:
                return (row, col)


def getadjacent(board, row, col):
    adj = 0
    if row > 0:
        adj += iif(board[row-1, col] == 1, 1, 0)
    if row < 2:
        adj += iif(board[row+1, col] == 1, 1, 0)
    if col > 0:
        adj += iif(board[row, col-1] == 1, 1, 0)
    if col < 2:
        adj += iif(board[row, col+1] == 1, 1, 0)
    return adj


def getaimove(board):
    # 1. win if possible
    move = getwinmove(board)
    if len(move) > 0:
        return random.choice(move)
    # 2. block if necessary
    move = getblockmove(board)
    if len(move) > 0:
        return random.choice(move)
    # 3. are we going first?
    if np.count_nonzero(board) == 0:
        return (1, 1)  # go in center
    # 4. are we going second?
    if np.count_nonzero(board) == 1:
        if board[1, 1] == 1:  # did player go in center?
            # go in a random corner
            return (random.randint(0, 1)*2, random.randint(0, 1)*2)
        else:
            return (1, 1)  # otherwise go in center
    # 5. do we have a fork move (i.e. a move that results in 2 winning moves for us)?
    move = getforkmove(board)
    if len(move) > 0:
        return random.choice(move)
    # 6. otherwise: go next to a player space, with a winning move if possible
    move = []
    # first check for moves that result in a winning move
    # we know that no moves will give us more than 1 winning move, because we would've caught it as a fork move
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0 and getadjacent(board, row, col) > 0:
                tempboard = np.copy(board)
                tempboard[row, col] = 4
                if len(getwinmove(tempboard)) > 0:
                    move.append((row, col))
    if len(move) > 0:
        return random.choice(move)
    # settle for move that doesn't result in a winning move
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0 and getadjacent(board, row, col) > 0:
                move.append((row, col))
    if len(move) > 0:
        return random.choice(move)
    # we shouldn't get here
    print('We shouldn\'t get here...')


playerwin, aiwin, draw = 0, 0, 0
playagain = True

while playagain:
    gameover = False
    # player=1, ai=4. first player is random
    curplayer = random.choice([1, 4])
    board = np.zeros((3, 3), dtype=np.int8)
    printboard(board)
    # game loop
    while not gameover:
        if curplayer == 1:
            move = getplayermove(board)
        else:
            move = getaimove(board)
            time.sleep(0.5)
            print('Computer moves to: {}'.format(move[0]*3+move[1]+1))
        board[move] = curplayer
        printboard(board)
        # see if player won:
        if np.sum(board[0, :]) == 3 or \
                np.sum(board[1, :]) == 3 or \
                np.sum(board[2, :]) == 3 or \
                np.sum(board[:, 0]) == 3 or \
                np.sum(board[:, 1]) == 3 or \
                np.sum(board[:, 2]) == 3 or \
                board[0, 0] + board[1, 1]+board[2, 2] == 3 or \
                board[0, 2] + board[1, 1]+board[2, 0] == 3:
            print('You won!')
            playerwin += 1
            gameover = True
        # see if AI won:
        if np.sum(board[0, :]) == 12 or \
                np.sum(board[1, :]) == 12 or \
                np.sum(board[2, :]) == 12 or \
                np.sum(board[:, 0]) == 12 or \
                np.sum(board[:, 1]) == 12 or \
                np.sum(board[:, 2]) == 12 or \
                board[0, 0] + board[1, 1]+board[2, 2] == 12 or \
                board[0, 2] + board[1, 1]+board[2, 0] == 12:
            print('The computer won :/')
            aiwin += 1
            gameover = True
        # see if we ended in a draw:
        if np.count_nonzero(board) == 9:
            print('The game ends in a draw......')
            draw += 1
            gameover = True
        curplayer = 5-curplayer
    print('Win: {}   Lose: {}   Draw: {}'.format(playerwin, aiwin, draw))
    time.sleep(1.0)
