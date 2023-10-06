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

    def rmRows(self):
        ...

    def rmCols(self):
        ...

    def solve_SLE_2x2(self: tuple = ()):
        return self[0][0] * self[1][1] - self[1][0] * self[0][1]

    def addCols(self, cols: tuple):
        new_mtrx = []
        for i in range(len(cols)):
            new_mtrx.append((*self.elements[i], cols[i]))
        self._checkMtrx()
        self.elements = tuple(new_mtrx)

    def _checkMtrx(self):
        for strings in self.elements:
            if len(strings) != self.size_x:
                raise ValueError("Error: Matrix arguments have inconsistent row lengths")
            for el in strings:
                ...
                if type(el) != int and type(el) != float:
                    raise ValueError("Error: Matrix arguments can be int or float")


m = Matrix((1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12))
m.show()

m.addRows((12, 2.3, 15))
m.show()

m.addCols((12, 13, 15))
m.show()
m2 = Matrix((3, 4), (2, 3))
a = Matrix.solve_SLE_2x2(((3, 4), (3, 1)))
print(a)
