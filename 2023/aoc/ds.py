class t(tuple):
    def __add__(self, other):
        return self.__class__(tuple(a + b for a, b in zip(self, other)))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.__class__(tuple(a - b for a, b in zip(self, other)))

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(tuple(a * other for a in self))
        return self.__class__(tuple(a * b for a, b in zip(self, other)))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int):
            return self.__class__(tuple(a / other for a in self))
        return self.__class__(tuple(a / b for a, b in zip(self, other)))

    def __rdiv__(self, other):
        return self / other

    def __floordiv__(self, other):
        if isinstance(other, int):
            return self.__class__(tuple(a // other for a in self))
        return self.__class__(tuple(a // b for a, b in zip(self, other)))

    def __rfloordiv__(self, other):
        return self // other
