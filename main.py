class Matrix:
    def __init__(self, *args: tuple):
        self.elements = args
        self.size_x = len(args[0])
        self.size_y = len(args)
        self.size = self.size_y * self.size_x
        self._checkMtrx()

    def show(self):
        for i in self.elements:
            for j in i:
                print(j, end='\t', sep='')
            print('')

    def T(self) -> tuple:
        new_mtrx = []
        for i in range(self.size_x):
            stroke = []
            for j in range(self.size_y):
                stroke.append(self.elements[j][i])
            new_mtrx.append(tuple(stroke))

        return tuple(new_mtrx)

    def addRows(self, row: tuple):
        new_mtrx = tuple((*self.elements, row))

        self._checkMtrx()
        self.elements = new_mtrx

    def addCols(self, cols: tuple):
        new_mtrx = []
        for i in range(len(cols)):
            new_mtrx.append((*self.elements[i], cols[i]))

        self._checkMtrx()
        self.elements = tuple(new_mtrx)

    def rmRows(self, num_rows):
        new_mtrx = []
        for i in range(len(self.elements)):
            if i != num_rows:
                new_mtrx.append(self.elements[i])

        return Matrix(*new_mtrx)

    def rmCols(self, num_cols):
        new_mtrx = []
        for i in range(len(self.elements)):
            new_mtrx.append(list(self.elements[i]))
        for i in range(len(new_mtrx)):
            new_mtrx[i].pop(num_cols)

        return Matrix(*new_mtrx)

    def cross_mtrx_2x2(self):
        return self.elements[0][0] * self.elements[1][1]\
            - self.elements[0][1] * self.elements[1][0]

    def solve_det(self): # сделать универсальным
        a, m2 = 0, None
        for i in range(self.size_x):
            for j in range(self.size_y):
                m2 = self.rmRows(0).rmCols(i)
            a += self.elements[0][i] * m2.cross_mtrx_2x2() * ((-1) ** (i))
        return a

    def solve_alg_addings(self): # сделать универсальным

        adding_mtrx = []
        new_mtrx = []

        for i in range(self.size_x):
            for j in range(self.size_y):
                m2 = self.rmRows(i).rmCols(j)
                new_mtrx.append(((-1) ** (j + i)) * m2.cross_mtrx_2x2())
            adding_mtrx.append(tuple(new_mtrx))
            new_mtrx.clear()
        return Matrix(*adding_mtrx)

    def _checkMtrx(self):
        for strings in self.elements:
            if len(strings) != self.size_x:
                raise ValueError("Error: Matrix arguments have inconsistent row lengths")
            for el in strings:
                ...
                if type(el) != int and type(el) != float:
                    raise ValueError("Error: Matrix arguments can be int or float")


def solve_SLE(A: Matrix, B: Matrix):
    n, ans = 0, []
    for i in range(A.size_y):
        for j in range(A.size_x):
            n += (A.solve_alg_addings().T()[i][j] * B.elements[0][j])
        ans.append(n / A.solve_det())
        n = 0
    return ans


m = Matrix((1, 2, 1), (2, -1, 1), (1, 1, 2))
b = Matrix((-1, 3, 0))
ans = solve_SLE(m, b)
m.show()
print(ans)
