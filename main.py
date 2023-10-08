import matplotlib.pyplot as plt


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
                print(j, end='\t\t', sep=' ')
            print()

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

    def transpose(self) -> tuple:
        new_mtrx = []
        for i in range(self.size_x):
            stroke = []
            for j in range(self.size_y):
                stroke.append(self.elements[j][i])
            new_mtrx.append(tuple(stroke))
        return tuple(new_mtrx)

    def cross_mtrx_2x2(self):
        return self.elements[0][0] * self.elements[1][1] \
            - self.elements[0][1] * self.elements[1][0]

    def find_determinant(self):
        if self.size_x == 2 and self.size_y == 2:
            return self.cross_mtrx_2x2()

        determinant = 0
        for i in range(self.size_x):
            submatrix = self.rm_rows(0).rm_columns(i)
            determinant += self.elements[0][i] * submatrix.find_determinant() * ((-1) ** i)# <- тут рекурсия
        return determinant

    def find_mtrx_addition(self):
        if self.size_x == 2 and self.size_y == 2:
            addition_mtrx = []
            for i in range(self.size_x):
                adding_row = []
                for j in range(self.size_y):
                    clean_mtrx = self.rm_rows(i).rm_columns(j)
                    adding_row.append(((-1) ** (j + i)) * clean_mtrx.cross_mtrx_2x2())
                addition_mtrx.append(tuple(adding_row))
            return Matrix(*addition_mtrx)

        addition_mtrx = []
        for i in range(self.size_x):
            adding_row = []
            for j in range(self.size_y):
                submatrix = self.rm_rows(i).rm_columns(j)
                adding_row.append(((-1) ** (j + i)) * submatrix.find_determinant())
            addition_mtrx.append(tuple(adding_row))
        return Matrix(*addition_mtrx)

    def solve_SLE(*self):
        A = self[0]
        B = self[1]
        if A.size_x != B.size_x:
            raise ValueError('Error:The number of columns of matrix A must be equal to the number of rows of matrix B.')
        cell_value, answer_list = 0, []
        for i in range(A.size_y):
            for j in range(A.size_x):
                cell_value += (A.find_mtrx_addition().transpose()[i][j] * B.elements[0][j])
            answer_list.append(cell_value / A.find_determinant())
            cell_value = 0
        return answer_list

    def find_near_square(*self, out_settings=None):

        x = list(*self[0].elements)
        y = list(*self[1].elements)

        x_mean, y_mean = sum(x) / len(x), sum(y) / len(y)
        line_slope = sum((xn - x_mean) * (xn - x_mean) for xn, yn in zip(x, y)) / sum((xn - x_mean) ** 2 for xn in x)
        line_offset = y_mean - line_slope * x_mean

        if out_settings == 's':
            print(f'SLOPE {line_slope}, OFFSET {line_offset}')
            plt.scatter(x, y)
            plt.plot(x, [line_slope * xi + line_offset for xi in x], 'r')
            plt.show()
        return line_slope, line_offset

    def _checkMtrx(self):
        for strings in self.elements:
            if len(strings) != self.size_x:
                raise ValueError("Error: Matrix arguments have inconsistent row lengths")
            for el in strings:
                if type(el) != int and type(el) != float:
                    raise ValueError("Error: Matrix arguments can be int or float")


# Cистемы Линейных Алгебраических Уравнений
m = Matrix((1, 1, 2, 3), (1, 2, 3, -1), (3, -1, -1, -2), (2, 3, -1, -1))
b = Matrix((1, -4, -4, -6))
m.show()
print('')
b.show()
ans = Matrix.solve_SLE(m, b)
print('\nОтвет:', *ans)

# Метод ближайших квадратов
m2 = Matrix((0, 1, 2, 3))
m3 = Matrix((-1, 0.2, 0.9, 2.1))
Matrix.find_near_square(m2, m3, out_settings='s')
