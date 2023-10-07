class Matrix:
    def __init__(self, *args: tuple):
        self.elements = args
        self.size_x = len(args[0])
        self.size_y = len(args)
        self.size = self.size_y * self.size_x
        self._checkMtrx()

    def show(self):
        for i in self.elements:
            print('|', end='\t')
            for j in i:
                print(j, end='\t\t', sep=' ')
            print('|')

    def T(self) -> tuple:
        new_mtrx = []
        for i in range(self.size_x):
            stroke = []
            for j in range(self.size_y):
                stroke.append(self.elements[j][i])
            new_mtrx.append(tuple(stroke))
            
        return tuple(new_mtrx)

    def add_rows(self, row: tuple):
        new_mtrx = tuple((*self.elements, row))

        self._checkMtrx()
        self.elements = new_mtrx

    def add_columns(self, cols: tuple):
        new_mtrx = []
        for i in range(len(cols)):
            new_mtrx.append((*self.elements[i], cols[i]))

        self._checkMtrx()
        self.elements = tuple(new_mtrx)

    def rm_rows(self, num_rows):
        new_mtrx = []
        for i in range(len(self.elements)):
            if i != num_rows:
                new_mtrx.append(self.elements[i])

        return Matrix(*new_mtrx)

    def rm_columns(self, num_cols):
        new_mtrx = []
        for i in range(len(self.elements)):
            new_mtrx.append(list(self.elements[i]))
        for i in range(len(new_mtrx)):
            new_mtrx[i].pop(num_cols)

        return Matrix(*new_mtrx)

    def cross_mtrx_2x2(self):
        return self.elements[0][0] * self.elements[1][1] \
            - self.elements[0][1] * self.elements[1][0]

    def solve_det(self):
        if self.size_x == 2 and self.size_y == 2:
            return self.cross_mtrx_2x2()

        determinant = 0
        for i in range(self.size_x):
            submatrix = self.rm_rows(0).rm_columns(i)
            determinant += self.elements[0][i] * submatrix.solve_det() * ((-1) ** i)
        return determinant

    def solve_alg_addings(self):
        if self.size_x == 2 and self.size_y == 2:
            adding_mtrx = []
            for i in range(self.size_x):
                adding_row = []
                for j in range(self.size_y):
                    m2 = self.rm_rows(i).rm_columns(j)
                    adding_row.append(((-1) ** (j + i)) * m2.cross_mtrx_2x2())
                adding_mtrx.append(tuple(adding_row))
            return Matrix(*adding_mtrx)

        adding_mtrx = []
        for i in range(self.size_x):
            adding_row = []
            for j in range(self.size_y):
                submatrix = self.rm_rows(i).rm_columns(j)
                adding_row.append(((-1) ** (j + i)) * submatrix.solve_det())
            adding_mtrx.append(tuple(adding_row))
        return Matrix(*adding_mtrx)

    def _checkMtrx(self):
        for strings in self.elements:
            if len(strings) != self.size_x:
                raise ValueError("Error: Matrix arguments have inconsistent row lengths")
            for el in strings:
                if type(el) != int and type(el) != float:
                    raise ValueError("Error: Matrix arguments can be int or float")


def solve_SLE(A: Matrix, B: Matrix):
    if A.size_x != B.size_y:
        raise ValueError('Error:The number of columns of matrix A must be equal to the number of rows of matrix B.')
    n, ans = 0, []
    for i in range(A.size_y):
        for j in range(A.size_x):
            n += (A.solve_alg_addings().T()[i][j] * B.elements[0][j])
        ans.append(n / A.solve_det())
        n = 0
    return ans


print('A=')
m = Matrix((1, 1, 2, 3), (1, 2, 3, -1), (3, -1, -1, -2), (2, 3, -1, -1))
b = Matrix((1, -4, -4, -6, 0))
m.show()
print('\nB=')
b.show()
det = m.solve_det()
print('_' * 50)
print('определитель = ', det)
print('обратная матрица алгебраических дополнений = ', end='\n')
m.solve_alg_addings().show()
print('_' * 50)
ans = solve_SLE(m, b)
print('Ответ:', *ans)
