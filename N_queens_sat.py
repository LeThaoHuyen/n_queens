from pysat.solvers import Solver

class Board:
    def __init__(self, N):
        self.clauses = set()
        self.N = N

    def cell2int(self, row, col):
        return row*self.N + col + 1

    # make constraints on the left parts of two diagonals
    def constraints_on_diagonals_left(self, row, col):
        i = row - 1
        j = col - 1
        while i >= 0 and j >= 0:
            v = self.cell2int(i, j)
            self.clauses.add(-v)
            i -= 1
            j -= 1

        i = row + 1
        j = col - 1
        while i < self.N and j >= 0:
            v = self.cell2int(i, j)
            self.clauses.add(-v)
            i += 1
            j -= 1
        
    # make constraints on the right parts of two diagonals
    def constraints_on_diagonals_right(self, row, col):
        i = row + 1
        j = col + 1
        while i < self.N and j < self.N:
            v = self.cell2int(i, j)
            self.clauses.add(-v)
            i += 1
            j += 1
        
        i = row - 1
        j = col + 1
        while i >= 0 and j < self.N:
            v = self.cell2int(i, j)
            self.clauses.add(-v)
            i -= 1
            j += 1

    # make constraints on the left part of horizontal line
    def constraints_on_horizontal_line_left(self, row, col):
        for j in range(col):
            v = self.cell2int(row, j)
            self.clauses.add(-v)

    # make constraints on the right part of horizontal line
    def constraints_on_horizontal_line_right(self, row, col):
        for j in range(col + 1, self.N):
            v = self.cell2int(row, j)
            self.clauses.add(-v)

    def constraints_on_vertical_line(self, row, col):
        for i in range(self.N):
            if i != row:
                v = self.cell2int(i, col)
                self.clauses.add(-v)

    def place_queen_level1(self, row, col):
        v = self.cell2int(row, col)
        self.clauses.add(v)
        self.constraints_on_diagonals_right(row, col)
        self.constraints_on_horizontal_line_right(row, col)

    def place_queen_level2(self, row, col):
        v = self.cell2int(row, col)
        self.clauses.add(v)
        self.constraints_on_diagonals_left(row, col)
        self.constraints_on_diagonals_right(row, col)
        self.constraints_on_horizontal_line_left(row, col)
        self.constraints_on_horizontal_line_right(row, col)
        self.constraints_on_vertical_line(row, col)

    def solve(self):
        s = Solver()
        for clause in self.clauses:
            s.add_clause([clause])

        if not s.solve():
            return False

        queen_positions = []
        for cell in s.get_model():
            if cell > 0:
                queen_positions.append(cell)

        return queen_positions

if __name__ == "__main__":
    board = Board(4)
    board.place_queen_level1(2,0)
    board.place_queen_level1(0,1)
    board.place_queen_level1(1,3)
    board.place_queen_level1(3,2)
    print(board.solve())

