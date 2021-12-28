from pysat.solvers import Solver

class Board:
    def __init__(self, N):
        self.clauses = []
        self.N = N

    def cell2int(self, row, col):
        return row*self.N + col + 1

    def generate_all_cnf(self):
        # each row must have 1 queen
        for r in range(self.N):
            row = []
            for c in range(self.N):
                row.append(self.cell2int(r, c))
            self.clauses.append(row)

        # each column must have 1 queen
        for c in range(self.N):
            col = []
            for r in range(self.N):
                col.append(self.cell2int(r, c))
            self.clauses.append(col)
        
        # queens can not on the same row, column, diagonal
        for r in range(self.N):
            for c in range(self.N):
                v = self.cell2int(r,c)
                # same row with (r,c)
                for j in range(c+1, self.N):
                    self.clauses.append([-v, -self.cell2int(r,j)])
                # same col with (r,c)
                for j in range(r+1, self.N):
                    self.clauses.append([-v, -self.cell2int(j,c)])
                # same diagonals with (r,c)
                i = r + 1
                j = c + 1
                while i < self.N and j < self.N: 
                    self.clauses.append([-v, -self.cell2int(i,j)])
                    i += 1
                    j += 1
                i = r + 1
                j = c - 1
                while i < self.N and j >= 0:
                    self.clauses.append([-v, -self.cell2int(i,j)])
                    i += 1
                    j -= 1

    def print_all_cnf(self):
        print(self.clauses)

    def solve(self):
        #self.generate_all_cnf()
        s = Solver()
        for clause in self.clauses:
            s.add_clause(clause)

        print(s.solve())
        res = []
        for v in s.get_model():
            if v > 0:
                res.append(v)
        print(res)



board = Board(4)
board.generate_all_cnf()
board.print_all_cnf()
board.solve()
print("Done")





