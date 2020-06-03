class BasePositionError(Exception):
    """The base class for errors which handle positions."""

    def __init__(self, position, tolerance):
        self.position = position
        self.tolerance = tolerance


class PositionOccupiedError(BasePositionError):
    """The error raised when a position is occupied but should not be."""

    def __init__(self, position, tolerance):
        super().__init__(position, tolerance)

    def __str__(self):
        return "There is an `Atom` within the tolerance radius '{}' of position '{}'.".format(
            self.tolerance, self.position)


class PositionUnoccupiedError(BasePositionError):
    """The error raised when a position is not occupied but should be."""

    def __init__(self, position, tolerance):
        super().__init__(position, tolerance)

    def __str__(self):
        return "There are no `Atom`s within the tolerance radius '{}' of position '{}'.".format(
            self.tolerance, self.position)


class BaseCrystallographyError(Exception):
    """The base class for errors which handle crystallography."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        self.a, self.b, self.c = a, b, c
        self.alpha, self.beta, self.gamma = alpha, beta, gamma
        self._str = "Lattice parameters: a = {}, b = {}, c = {}, alpha = {}, beta = {}, gamma = {}".format(
            a, b, c, alpha, beta, gamma)


class InvalidTriclinicError(BaseCrystallographyError):
    """The error raised when a set of lattice parameters do not satisfy the triclinic constraint."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __str__(self):
        return "Triclinic constraint: a != b != c and alpha != beta != gamma\n{}".format(self._str)


class InvalidMonoclinicError(BaseCrystallographyError):
    """The error raised when a set of lattice parameters do not satisfy the monoclinic constraint."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __str__(self):
        return "Monoclinic constraint: a != b != c and alpha == gamma == PI / 2 and beta != PI / 2\n{}".format(
            self._str)


class InvalidOrthorhombicError(BaseCrystallographyError):
    """The error raised when a set of lattice parameters do not satisfy the orthorhombic constraint."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __str__(self):
        return "Orthorhomboc constraint: a != b != c and alpha == beta == gamma == PI / 2\n{}".format(self._str)


class InvalidTetragonalError(BaseCrystallographyError):
    """The error raised when a set of lattice parameters do not satisfy the tetragonal constraint."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __str__(self):
        return "Tetragonal constraint: a == b != c and alpha == beta == gamma == PI / 2\n{}".format(self._str)


class InvalidRhombohedralError(BaseCrystallographyError):
    """The error raised when a set of lattice parameters do not satisfy the rhombohedral constraint."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __str__(self):
        return "Rhombohedral constraint: a == b == c and alpha == beta == gamma != PI / 2\n{}".format(self._str)


class InvalidHexagonalError(BaseCrystallographyError):
    """The error raised when a set of lattice parameters do not satisfy the hexagonal constraint."""

    def __init__(self, a, b, c, alpha, beta, gamma):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __str__(self):
        return "Rhombohedral constraint: a == b != c and alpha == gamma == PI / 2, and beta == 120 * PI / 180\n{}".format(
            self._str)
