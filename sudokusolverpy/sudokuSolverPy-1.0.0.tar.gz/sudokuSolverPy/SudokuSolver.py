class SudokuSolver:
    # Initializing required variables and validate board
    def __init__(self, board, boardSize=9, boxSize=3):
        self.boardSize = boardSize
        self.boxSize = boxSize
        self.board = board
        self.__validateBoard__()

    # Validate if the board is of the proper format else throw an exception
    def __validateBoard__(self):
        if len(self.board) != self.boardSize:
            message = "Incorrect board size: len(board)=" + \
                str(len(self.board))
            raise Exception(message)

        for i in range(len(self.board)):
            if len(self.board[i]) != self.boardSize:
                message = "Incorrect board size: len(board["+str(i) + "]) = " + str(
                    len(self.board[i]))
                raise Exception(message)

    # Check if the number num is valid for given position row, column
    def isValid(self, row, column, num):
        for j in range(self.boardSize):
            if self.board[row][j] == num and j != column:
                return False

        for i in range(self.boardSize):
            if self.board[i][column] == num and i != row:
                return False

        alpha = (row // self.boxSize)*self.boxSize
        beta = (column // self.boxSize)*self.boxSize
        for i in range(alpha, alpha + self.boxSize):
            for j in range(beta, beta + self.boxSize):
                if self.board[i][j] == num and (i != row and j != column):
                    return False
        return True
    
    # Internal function to solve the board
    def __solve__(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == 0:
                    for num in range(1, self.boardSize + 1):
                        if self.isValid(i, j, num):
                            self.board[i][j] = num
                            if (self.__solve__()):
                                return True
                            self.board[i][j] = 0
                    return False
        return True
    
    # Verify that the board is solved
    def verifyBoard(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                num = self.board[i][j]
                if not self.isValid(i, j, num):
                    return False
        return True
                

    # function called by the user to solve the board
    def solve(self):
        isSolved = self.__solve__() and self.verifyBoard()
        if not isSolved:
            raise Exception("Cannot solve the sudoku board")
        return self.board
    
    def getBoard(self):
        return self.board
            
    def printBoard(self, formatted = False):
        if formatted:
            print ("-"*19)
            for i in self.board:
                line = "|"
                for j in i:
                    line += str(j) + "|"
                print (line)
            print ("-"*19)
        else:
            for i in self.board:
                print (i)