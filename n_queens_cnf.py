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
                for i, j in zip(range(r+1, self.N), range(c+1, self.N)):
                    self.clauses.append([-v, -self.cell2int(i,j)])
                for i, j in zip(range(r+1, self.N), range(c-1, -1, -1)):
                    self.clauses.append([-v, -self.cell2int(i,j)])

    def print_all_cnf(self):
        for clause in self.clauses:
            print("(", end="")
            for v in clause:
                if v != clause[-1]: 
                    print(str(v)+" v ", end="")
                else:
                    print(str(v)+")")
        
        #print(self.clauses)

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





