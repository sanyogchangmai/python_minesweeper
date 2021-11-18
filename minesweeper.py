import random
import re

# ! Creating a class to make a board object for playing minesweeper

class Board:
    def __init__(self, dimensionSize, numberOfBombs):

        # ! keeping track of board dimension and number of bombs
        self.dimensionSize = dimensionSize
        self.numberOfBombs = numberOfBombs

        # ! creating the board
        self.board = self.makeNewBoard()
        self.assign_values_to_board()

        # ! initializes a set to keep track of which locations we've uncovered
        self.dug = set()

    def makeNewBoard(self):

        # ! generating a new board 2D array
        board = [[None for _ in range(self.dimensionSize)] for _ in range(self.dimensionSize)]

        # ! planting the bombs using random numbers
        bombsPlanted = 0
        while bombsPlanted < self.numberOfBombs:
            location = random.randint(0, self.dimensionSize**2 - 1)
            row = location // self.dimensionSize
            column = location % self.dimensionSize

            if board[row][column] == '*':
                continue

            board[row][column] = '*'
            bombsPlanted += 1

        return board

    # ! let's assign a number 0-8 for all the empty spaces
    def assign_values_to_board(self):
        for r in range(self.dimensionSize):
            for c in range(self.dimensionSize):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, column):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dimensionSize-1, row+1)+1):
            for c in range(max(0, column-1), min(self.dimensionSize-1, column+1)+1):
                if r == row and c == column:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    # ! Diging at location returning True if successful dig, False if bomb is dug

    def dig(self, row, column):
        self.dug.add((row, column))

        if self.board[row][column] == '*':
            return False
        elif self.board[row][column] > 0:
            return True

        for r in range(max(0, row-1), min(self.dimensionSize-1, row+1)+1):
            for c in range(max(0, column-1), min(self.dimensionSize-1, column+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    # ! Creating a new array that represents what the user would see

    def __str__(self):
        visible_board = [[None for _ in range(self.dimensionSize)] for _ in range(self.dimensionSize)]
        for row in range(self.dimensionSize):
            for column in range(self.dimensionSize):
                if (row,column) in self.dug:
                    visible_board[row][column] = str(self.board[row][column])
                else:
                    visible_board[row][column] = ' '
        
        string_rep = ''
        widths = []
        for idx in range(self.dimensionSize):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        indices = [i for i in range(self.dimensionSize)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dimensionSize)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# ! Playing the game
def play(dimensionSize=10, numberOfBombs=10):
    # ! Creating the board and plant the bombs
    board = Board(dimensionSize, numberOfBombs)

    # ! Showing the user the board and ask for where they want to dig
    # ! if location is a bomb, show game over message
    # ! If location is not a bomb, dig recursively until each square is at least next to a bomb
    # ! Repeating the above steps until there are no more places to dig -> VICTORY!
    safe = True 

    while len(board.dug) < board.dimensionSize ** 2 - numberOfBombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dimensionSize or col < 0 or col >= dimensionSize:
            print("Invalid location. Try again.")
            continue

        # ! If it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        board.dug = [(r,c) for r in range(board.dimensionSize) for c in range(board.dimensionSize)]
        print(board)

if __name__ == '__main__':
    play()