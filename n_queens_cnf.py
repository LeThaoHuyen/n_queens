from pysat.solvers import Solver

class Board:
    def __init__(self, N, level):
        self.clauses = []
        self.N = N
        self.level = level

    def cell2int(self, row, col):
        return row*self.N + col + 1

    def generate_all_cnf(self):
        if self.level == 1:
            # each colum have 1 queen
            for c in range(self.N):
                cur_col = []
                for r in range(self.N):
                    cur_col.append(self.cell2int(r, c))
                self.clauses.append(cur_col)
        else:
            # queens can be on any cell
            self.clauses.append([v for v in range(1, self.N*self.N + 1)])

        # queens can not on the same row, diagonal in level 1
        # queens can not on the same row, diagonal, col in level 2
        for r in range(self.N):
            for c in range(self.N):
                v = self.cell2int(r,c)
                # cells on same row with (r,c)
                for j in range(c+1, self.N):
                    self.clauses.append([-v, -self.cell2int(r,j)])
                # cells on same diagonals with (r,c)
                for i, j in zip(range(r+1, self.N), range(c+1, self.N)):
                    self.clauses.append([-v, -self.cell2int(i,j)])
                for i, j in zip(range(r+1, self.N), range(c-1, -1, -1)):
                    self.clauses.append([-v, -self.cell2int(i,j)])

                if self.level == 2:
                    # cells on same col with (r,c)
                    for i in range(r+1, self.N):
                        self.clauses.append([-v, -self.cell2int(i,c)])
    
    def print_all_cnf(self):
        for clause in self.clauses:
            print("(", end="")
            for v in clause:
                if v != clause[-1]: 
                    print(str(v)+" v ", end="")
                else:
                    print(str(v)+")")
        
    def print_solutions(self):
        # print all satisfied sets
        with Solver(bootstrap_with=self.clauses) as s:
            #print(s.solve())
            for m in s.enum_models():
                res = []
                for v in m:
                    if v > 0:
                        res.append(v)
                if len(res) == self.N: # needed for level 2
                    print(res)


if __name__ == "__main__":
    while True:
        print("Please enter level to continue: ")
        print("1: level 1")
        print("2: level 2")
        print("0: quit")
        
        level = input()

        if level == "1" or level == "2":
            board = Board(5, int(level))
            board.generate_all_cnf()
            print("Generated CNFs for level " + level + " (task c):")       
            board.print_all_cnf()
            print("All sets of satisfied values for level " + level + "(task d):")
            board.print_solutions()

        elif level == "0":
            break
        else:
            print("Invalid input")




    
    






