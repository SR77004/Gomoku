
import tkinter as tk
from tkinter import messagebox
import numpy as np
from functools import partial


from minimax import minimax
from heuristic import hasWinnerSeq, calculateHeuristic



class State(object):

    def __init__(self, board, player):
        self.board = board
        self.player = player

    @property
    def heuristic_value(self):
        self._heuristic_value = calculateHeuristic(self.board, self.player)
        return self._heuristic_value

    @property
    def available_moves(self):
        height = self.board.shape[0]
        width = self.board.shape[1]
        proximityBoard = self.board.copy()
        radius = 3
        proximityMatrix = np.ones((radius, radius))*3
        temp = np.count_nonzero(proximityBoard)
        if (temp > 1):
            for row in range(height - radius + 1):
                for col in range(width - radius + 1):
                    if np.any(self.board[row:row + radius, col:col + radius]):
                        proximityBoard[row:row + radius, col:col + radius] += proximityMatrix
        elif temp == 1 and self.board[int(height/2), int(width/2)] == 0:
            proximityBoard[int(height/2), int(width/2)] = 3
        elif temp == 1 and self.board[int(height/2), int(width/2)] != 0:
            proximityBoard[int(height/2) - 1, int(width/2) - 1] = 3
        elif temp == 0:
            proximityBoard[int(height/2), int(width/2)] = 3

        self._available_moves = []
        diffToCenterHeight = abs(np.arange(height) - int(height/2))
        centerToBorderHeight = np.argsort(diffToCenterHeight)
        diffToCenterWidth = abs(np.arange(width) - int(width/2))
        centerToBorderWidth = np.argsort(diffToCenterWidth)
        for row in centerToBorderHeight:
            for col in centerToBorderWidth:
                if (proximityBoard[row][col] % 3 == 0 and proximityBoard[row][col] > 0):
                    move = (row, col)
                    self._available_moves.append(move)

        return self._available_moves

    def is_terminal(self):

        if not (0 in self.board):
            return True
        if hasWinnerSeq(self.board, self.player):
            return True
        else:
            return False

    def next_state(self, move):
        next_board = np.copy(self.board)
        next_board[move] = self.player
        next_player = -1*self.player
        return State(next_board, next_player)



class Game:

    def __init__(self, height=15, width=15):


        self.root = tk.Tk()
        self.root.geometry('840x680+250+0')
        self.root.title('Gomoku Game')

        self.height = height
        self.width = width
        self.bottomFrame = tk.Frame(self.root)
        self.bottomFrame.grid(row=15, columnspan=155)
        self.btn = tk.Button(self.bottomFrame, text='My text')
        self.btn.config(state='disabled', relief=tk.SUNKEN)

        self.quitBtn = tk.Button(self.bottomFrame,
                                 text='Quit',
                                 command=self.quit)
        self.quitBtn.grid(row=18, columnspan=5)
        reset_with_arg = partial(self.reset)
        self.Reset = tk.Button(self.bottomFrame,
                               text='Reset Game',
                               command=reset_with_arg)
        self.Reset.grid(row=19, columnspan=5)



        self.createButtons(self.root)
        initial_board = np.zeros((height, width))
        player_one = 1
        self.current_state = State(initial_board, player_one)
        self.isPlayerOneHuman = self.isHuman('One')
        self.isPlayerTwoHuman = self.isHuman('Two')


        if (not self.isPlayerOneHuman) and self.current_state.player == 1:
            self.PCMove()



    def PCMove(self):

        print('The PC will play! Fasten your seats belts!')
        move = minimax(self.current_state)
        print(move)
        btn = self.buttons[self.findBt(move)][0]
        if (self.current_state.player == 1):
            btn.config(bg='black')
            btn.config(state='disabled', relief=tk.SUNKEN)
            print('Black moved.')
        else:
            btn.config(bg='white')
            btn.config(state='disabled', relief=tk.SUNKEN)
            print('White moved.')
        self.current_state = self.current_state.next_state(move)
        self.root.update()

        if (self.is_gameover() and self.isPlayerTwoHuman):
            if self.playAgain('One'):
                self.Reset.invoke()
                return 1
            else:
                self.quitBtn.invoke()
                return 1

        elif (self.is_gameover() and self.isPlayerOneHuman):
            if self.playAgain('Two'):
                self.Reset.invoke()
                return 1
            else:
                self.quitBtn.invoke()
                return 1


        if (not self.isPlayerOneHuman) and (not self.isPlayerTwoHuman):
            self.PCMove()
        print('Waiting a move...')



    def createButtons(self, parent):
        self.buttons = {}
        row = 0
        col = 0
        for x in range(0, 15*15):
            id = str(row) + '-' + str(col)
            self.buttons[x] = [tk.Button(parent,
                                         bg='#24a3c9',
                                         height=2,
                                         width=4),
                               id,  # 'row-col'
                               row,
                               col] # Populating the dictionary

            self.buttons[x][0].bind('<Button-1>', self.leftClick_w(x))


            col += 1
            if col == 15:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row=self.buttons[k][2],
                                        column=self.buttons[k][3])


    def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)



    def leftClick(self, btn):


        if (self.current_state.player == 1 and self.current_state.board[self.buttons
                                                                        [btn][2]][self.buttons
                                                                        [btn][3]] == 0):
            self.buttons[btn][0].config(bg='black')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.current_state.board[self.buttons[btn][2]][self.buttons[btn][3]] = 1
            self.root.update()
            if (self.is_gameover()):
                if self.playAgain('One'):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1

            print('BLACK!')

            self.current_state.player = -1

            if not self.isPlayerTwoHuman:
                self.PCMove()
            print('Are you ready?')

        elif (self.current_state.player == -1 and self.current_state.board[self.buttons
                                                                        [btn][2]][self.buttons
                                                                        [btn][3]] == 0):
            self.buttons[btn][0].config(bg='white')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.current_state.board[self.buttons[btn][2]][self.buttons[btn][3]] = -1
            self.root.update()
            if (self.is_gameover()):
                if self.playAgain('Two'):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1

            print('WHITE!')

            self.current_state.player = 1

            if not self.isPlayerOneHuman:
                self.PCMove()
            print('Are you ready?')



    def isHuman(self, number):
        '''
            Function to choose wether the player is human or not.
        '''
        msg = 'Is Player {} a human?'.format(number)
        return messagebox.askyesno('Human or PC', msg)



    def playAgain(self, number):
        msg = 'Player {} is the winner! \nDo you want to play again?'.format(number)
        return messagebox.askyesno('Play again', msg)


    def is_gameover(self):

        return self.current_state.is_terminal()


    def findBt(self, move):
        for b in self.buttons.keys():
            if (self.buttons[b][2] == move[0] and
               self.buttons[b][3] == move[1]):
                return b

    def quit(self):
        self.root.destroy()

    def reset(self):
        print('--------------------')
        initial_board = np.zeros((self.height, self.width))
        player_one = 1
        self.current_state = State(initial_board, player_one)
        for btn in self.buttons.keys():
            self.buttons[btn][0].destroy()


        self.createButtons(self.root) #|3rd.|
        initial_board = np.zeros((self.height, self.width))
        player_one = 1
        self.current_state = State(initial_board, player_one)
        self.isPlayerOneHuman = self.isHuman('One')
        self.isPlayerTwoHuman = self.isHuman('Two')


        if (not self.isPlayerOneHuman) and (self.isPlayerTwoHuman) and self.current_state.player == 1:
            self.PCMove()




    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    gomoku = Game()
    gomoku.run()