import numpy as np
import random
import time
from tkinter import *


def getwinmove(board, playernum=4):
    totalcheck = playernum*2      # 2 if player 1, 8 if player 4
    winmove = []
    # check rows
    for row in range(3):
        if sum(board[row, :]) == totalcheck:
            for col in range(3):
                if board[row, col] == 0:
                    winmove.append((row, col))
    # check columns
    for col in range(3):
        if sum(board[:, col]) == totalcheck:
            for row in range(3):
                if board[row, col] == 0:
                    winmove.append((row, col))
    # check top-left to bottom-right
    if board[0, 0]+board[1, 1]+board[2, 2] == totalcheck:
        for i in range(3):
            if board[i, i] == 0:
                winmove.append((i, i))
    # check top-right to bottom-left
    if board[0, 2]+board[1, 1]+board[2, 0] == totalcheck:
        for i in range(3):
            if board[i, 2-i] == 0:
                winmove.append((i, 2-i))
    return winmove


def getblockmove(board, playernum=4):
    totalcheck = (5-playernum)*2      # 2 for player 4, 8 for player 1
    blockmove = []
    # check rows
    for row in range(3):
        if sum(board[row, :]) == totalcheck:
            for col in range(3):
                if board[row, col] == 0:
                    blockmove.append((row, col))
                    # break
    # check columns
    for col in range(3):
        if sum(board[:, col]) == totalcheck:
            for row in range(3):
                if board[row, col] == 0:
                    blockmove.append((row, col))
                    # break
    # check top-left to bottom-right
    if board[0, 0]+board[1, 1]+board[2, 2] == totalcheck:
        for i in range(3):
            if board[i, i] == 0:
                blockmove.append((i, i))
    # check top-right to bottom-left
    if board[0, 2]+board[1, 1]+board[2, 0] == totalcheck:
        for i in range(3):
            if board[i, 2-i] == 0:
                blockmove.append((i, 2-i))
    return blockmove


def getforkmove(board, playernum=4):
    forkmove = []
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                tempboard = np.copy(board)
                tempboard[row, col] = playernum
                if len(getwinmove(tempboard, playernum)) > 1:
                    forkmove.append((row, col))
    return forkmove


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
        if board[1, 1] == 1:        # did player go in center?
            # go in a random corner
            return (random.randint(0, 1)*2, random.randint(0, 1)*2)
        else:
            # otherwise go in center
            return (1, 1)           
    # 5. do we have a fork move (i.e. a move that results in 2 winning moves for us)?
    move = getforkmove(board)
    if len(move) > 0:
        return random.choice(move)
    # 6. any available move that leaves us a winning move, and blocking doesn't leave the player more than 1 winning move
    move = []
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                tempboard = np.copy(board)
                tempboard[row, col] = 4
                # does it leave us a winning move? (there can only be 1, otherwise we would've seen it as a fork move)
                aiwin = getwinmove(tempboard)
                if len(aiwin) > 0:
                    tempboard[aiwin[0][0], aiwin[0][1]] = 1
                    # make sure the player has less than 2 winning moves after blocking us
                    if len(getwinmove(tempboard, 1)) < 2:
                        move.append((row, col))
    if len(move) > 0:
        return random.choice(move)
    # 7. any available move that doesn't leave a fork move for the player
    # apparently we never even get here?
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                tempboard = np.copy(board)
                tempboard[row, col] = 4
                if len(getforkmove(tempboard, 1)) == 0:
                    move.append((row, col))
    if len(move) > 0:
        return random.choice(move)
    # otherwise: any random available move
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                move.append((row, col))
    if len(move) > 0:
        return random.choice(move)


def playagain(event):
    global board
    global gameover
    cv.unbind('<Button-1>')
    cv.create_rectangle(0, 0, 500, 500, outline='black', fill='black')
    # draw the board lines
    cv.create_line(25, 175, 475, 175, width=10, fill='white')
    cv.create_line(25, 325, 475, 325, width=10, fill='white')
    cv.create_line(175, 25, 175, 475, width=10, fill='white')
    cv.create_line(325, 25, 325, 475, width=10, fill='white')
    #
    label2['text'] = ''
    gameover = False
    board = np.zeros((3, 3), dtype=np.int8)
    if (playerwin+aiwin+draw) % 2 == 1:         # computer goes first on odd games
        # get computer move
        move = getaimove(board)
        # draw O for computer:
        cv.create_oval(move[0]*150+50, move[1]*150+50, move[0]
                       * 150+150, move[1]*150+150, width=5, outline='blue')
        board[move] = 4
    cv.bind('<Button-1>', gameloop)


def gameloop(event):
    global board
    global gameover
    global playerwin, aiwin, draw
    cv.unbind('<Button-1>')
    label2['text']=''
    if event.x < 175:
        row = 0
    elif event.x < 325:
        row = 1
    else:
        row = 2
    if event.y < 175:
        col = 0
    elif event.y < 325:
        col = 1
    else:
        col = 2
    if board[row, col] == 0:        # is move valid?
        # draw X for player:
        cv.create_line(row*150+50, col*150+50, row*150+150,
                       col*150+150, width=5, fill='red')
        cv.create_line(row*150+150, col*150+50, row*150 +
                       50, col*150+150, width=5, fill='red')
        board[row, col] = 1
        # see if player won:
        if sum(board[0, :]) == 3 or \
                sum(board[1, :]) == 3 or \
                sum(board[2, :]) == 3 or \
                sum(board[:, 0]) == 3 or \
                sum(board[:, 1]) == 3 or \
                sum(board[:, 2]) == 3 or \
                sum(board[i,i] for i in range(3)) == 3 or \
                sum(board[i,2-i] for i in range(3)) == 3:
            playerwin += 1
            label1['text'] = 'Win/Lose/Draw: {}/{}/{}'.format(
                playerwin, aiwin, draw)
            label2['text'] = 'You won!  Click the board to play again'
            gameover = True
        # or if game ended in a draw:
        elif np.count_nonzero(board) == 9:
            draw += 1
            label1['text'] = 'Win/Lose/Draw: {}/{}/{}'.format(
                playerwin, aiwin, draw)
            label2['text'] = 'The game ends in a draw.  Click the board to play again'
            gameover = True
        else:
            # get computer move
            ## this part doesn't work as expected:
            label2['text'] = 'Computer thinking...'
            time.sleep(0.5)
            label2['text'] = ''
            ##
            move = getaimove(board)
            # draw O for computer:
            cv.create_oval(move[0]*150+50, move[1]*150+50, move[0]
                           * 150+150, move[1]*150+150, width=5, outline='blue')
            board[move] = 4
            # see if AI won:
            if sum(board[0, :]) == 12 or \
                    sum(board[1, :]) == 12 or \
                    sum(board[2, :]) == 12 or \
                    sum(board[:, 0]) == 12 or \
                    sum(board[:, 1]) == 12 or \
                    sum(board[:, 2]) == 12 or \
                    sum(board[i,i] for i in range(3)) == 12 or \
                    sum(board[i,2-i] for i in range(3)) == 12:
                aiwin += 1
                label1['text'] = 'Win/Lose/Draw: {}/{}/{}'.format(
                    playerwin, aiwin, draw)
                label2['text'] = 'The computer won.  Click the board to play again'
                gameover = True
            elif np.count_nonzero(board) == 9:
                draw += 1
                label1['text'] = 'Win/Lose/Draw: {}/{}/{}'.format(
                    playerwin, aiwin, draw)
                label2['text'] = 'The game ends in a draw.  Click the board to play again'
                gameover = True
    if gameover:
        cv.bind('<Button-1>', playagain)
    else:
        cv.bind('<Button-1>', gameloop)


root = Tk()

cvwidth = 500
cvheight = 500
cv = Canvas(root, bg='black', width=cvwidth, height=cvheight)
cv.pack(side=TOP)
# draw the board lines
cv.create_line(25, 175, 475, 175, width=10, fill='white')
cv.create_line(25, 325, 475, 325, width=10, fill='white')
cv.create_line(175, 25, 175, 475, width=10, fill='white')
cv.create_line(325, 25, 325, 475, width=10, fill='white')

frame = Frame(root)
frame.pack(side=BOTTOM, fill=BOTH)
label1 = Label(frame, text='Win/Lose/Draw: 0/0/0')
label2 = Label(frame, text='Click the board to play!')
label1.pack()
label2.pack()

playerwin, aiwin, draw = 0, 0, 0

gameover = False
board = np.zeros((3, 3), dtype=np.int8)

cv.bind('<Button-1>', gameloop)
root.mainloop()
