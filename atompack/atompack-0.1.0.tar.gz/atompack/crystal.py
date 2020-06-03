import copy
from typing import List, Optional, Tuple

import numpy as np
from scipy.spatial.transform import Rotation

from atompack.atom import Atom, AtomCollection
from atompack.error import (InvalidHexagonalError, InvalidMonoclinicError, InvalidOrthorhombicError,
                            InvalidRhombohedralError, InvalidTetragonalError, InvalidTriclinicError)
from atompack.internal import metric_tensor, search_for_atom


class Crystal(AtomCollection):
    """A crystalline lattice.

    Args:
        a: The \\(a\\) distance lattice parameter.
        b: The \\(b\\) distance lattice parameter.
        c: The \\(c\\) distance lattice parameter.
        alpha: The \\(\\alpha\\) angle lattice parameter.
        beta: The \\(\\beta\\) angle lattice parameter.
        gamma: The \\(\\gamma\\) angle lattice parameter.
        unit_cell: A template of atoms and their basis sites to be repeated during construction.
        orientation: The orientation of the basis.
        rotation: A rotation matrix which rotates the final structure.
        size: The number of units to repeat in each spatial direction.
    """

    def __init__(self,
                 a: float = 0,
                 b: float = 0,
                 c: float = 0,
                 alpha: float = 0,
                 beta: float = 0,
                 gamma: float = 0,
                 unit_cell: Optional[List[Tuple[Atom, np.ndarray]]] = None,
                 orientation: Optional[np.ndarray] = None,
                 rotation: Optional[np.ndarray] = None,
                 size: Optional[Tuple[int, int, int]] = None) -> None:
        self._a, self._b, self._c = a, b, c
        self._alpha, self._beta, self._gamma = alpha, beta, gamma
        self._unit_cell = unit_cell
        self._orientation = orientation
        self._rotation = rotation
        self._size = size
        atoms, basis = self._build()
        super().__init__(atoms=atoms, basis=basis)

    @classmethod
    def triclinic(cls,
                  a: float,
                  b: float,
                  c: float,
                  alpha: float,
                  beta: float,
                  gamma: float,
                  unit_cell: List[Tuple[Atom, np.ndarray]],
                  orientation: Optional[np.ndarray] = None,
                  rotation: Optional[np.ndarray] = None,
                  size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with triclinic constraints.
        
        Raises:
            `atompack.error.InvalidTriclinicError`: Triclinic constraints are not satisfied.
        """
        if not (a != b != c):
            raise InvalidTriclinicError(a, b, c, alpha, beta, gamma)
        if not (alpha != beta != gamma):
            raise InvalidTriclinicError(a, b, c, alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    @classmethod
    def monoclinic(cls,
                   a: float,
                   b: float,
                   c: float,
                   beta: float,
                   unit_cell: List[Tuple[Atom, np.ndarray]],
                   orientation: Optional[np.ndarray] = None,
                   rotation: Optional[np.ndarray] = None,
                   size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with monoclinic constraints.
        
        Raises:
            `atompack.error.InvalidMonoclinicError`: Monoclinic constraints are not satisfied.
        """
        alpha, gamma = np.pi / 2, np.pi / 2
        if not (a != b != c):
            raise InvalidMonoclinicError(a, b, c, alpha, beta, gamma)
        if beta == np.pi / 2:
            raise InvalidMonoclinicError(a, b, c, alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    @classmethod
    def orthorhombic(cls,
                     a: float,
                     b: float,
                     c: float,
                     unit_cell: List[Tuple[Atom, np.ndarray]],
                     orientation: Optional[np.ndarray] = None,
                     rotation: Optional[np.ndarray] = None,
                     size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with orthorhombic constraints.
        
        Raises:
            `atompack.error.InvalidOrthorhombicError`: Orthorhombic constraints are not satisfied.
        """
        alpha, beta, gamma = np.pi / 2, np.pi / 2, np.pi / 2
        if not (a != b != c):
            raise InvalidOrthorhombicError(a, b, c, alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    @classmethod
    def tetragonal(cls,
                   a: float,
                   c: float,
                   unit_cell: List[Tuple[Atom, np.ndarray]],
                   orientation: Optional[np.ndarray] = None,
                   rotation: Optional[np.ndarray] = None,
                   size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with tetragonal constraints.
        
        Raises:
            `atompack.error.InvalidTetragonalError`: Tetragonal constraints are not satisfied.
        """
        b = a
        alpha, beta, gamma = np.pi / 2, np.pi / 2, np.pi / 2
        if a == c:
            raise InvalidTetragonalError(a, b, c, alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    @classmethod
    def rhombohedral(cls,
                     a: float,
                     alpha: float,
                     unit_cell: List[Tuple[Atom, np.ndarray]],
                     orientation: Optional[np.ndarray] = None,
                     rotation: Optional[np.ndarray] = None,
                     size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with rhombohedral constraints.
        
        Raises:
            `atompack.error.InvalidRhombohedralError`: Rhombohedral constraints are not satisfied.
        """
        b, c = a, a
        beta, gamma = alpha, alpha
        if alpha == np.pi / 2:
            raise InvalidRhombohedralError(a, b, c, alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    @classmethod
    def hexagonal(cls,
                  a: float,
                  c: float,
                  unit_cell: List[Tuple[Atom, np.ndarray]],
                  orientation: Optional[np.ndarray] = None,
                  rotation: Optional[np.ndarray] = None,
                  size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with hexagonal constraints.
        
        Raises:
            `atompack.error.InvalidHexagonalError`: Hexagonal constraints are not satisfied.
        """
        b = a
        alpha, beta, gamma = np.pi / 2, 120 * np.pi / 180, np.pi / 2
        if a == c:
            raise InvalidHexagonalError(a, b, c, alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    @classmethod
    def cubic(cls,
              a: float,
              unit_cell: List[Tuple[Atom, np.ndarray]],
              orientation: Optional[np.ndarray] = None,
              rotation: Optional[np.ndarray] = None,
              size: Optional[Tuple[int, int, int]] = None) -> 'Crystal':
        """Initializes a `Crystal` with cubic constraints."""
        b, c = a, a
        alpha, beta, gamma = np.pi / 2, np.pi / 2, np.pi / 2
        return cls(a, b, c, alpha, beta, gamma, unit_cell, orientation, rotation, size)

    def _build(self) -> Tuple[List[Atom], np.ndarray]:
        # generate lattice vectors from metric tensor
        lattice_vectors = np.sqrt(metric_tensor(self._a, self._b, self._c, self._alpha, self._beta, self._gamma))

        # process attributes
        if self._unit_cell is None:
            self._unit_cell = [(Atom(), np.zeros((3,)))]
        if self._orientation is None:
            self._orientation = lattice_vectors
        if self._rotation is None:
            self._rotation = np.identity(3)
        else:
            raise NotImplementedError()
        if self._size is None:
            self._size = (1, 1, 1)

        # generate the rotation between the lattice vectors and new orientation
        rotation = Rotation.align_vectors(lattice_vectors, self._orientation)[0]

        # align lattice vectors with orientation
        oriented_lattice_vectors = np.matmul(self._orientation, lattice_vectors)

        # use QR decomposition to determine an orthogonal representation of the oriented lattice vectors
        _, r = np.linalg.qr(oriented_lattice_vectors.T)
        oriented_lattice_vectors = np.abs(r) * np.array(self._size)
        oriented_lattice_magnitudes = np.linalg.norm(oriented_lattice_vectors, axis=0)

        # determine the smallest required orthogonal cell
        # TODO: determine optimal scaling factor
        scaling_factor = 2
        minimum_orthogonal_size = (np.ceil(np.linalg.norm(r, axis=0)) *
                                   np.array(self._size)).astype(int) * scaling_factor

        # place atoms on the oriented lattice vectors
        atoms: List[Atom] = []
        for xsize in range(minimum_orthogonal_size[0]):
            for ysize in range(minimum_orthogonal_size[1]):
                for zsize in range(minimum_orthogonal_size[2]):
                    offset = np.matmul(np.array([xsize, ysize, zsize]), lattice_vectors)
                    for atom, relative_position in self._unit_cell:

                        # assign the cartesian position
                        position = np.matmul(relative_position, lattice_vectors) + offset
                        position = rotation.apply(position)

                        # transform the position back into the bounding box
                        for i in range(3):
                            if position[i] < -1e-6:
                                new_position = position[i]
                                while new_position < -1e-6:
                                    new_position += oriented_lattice_magnitudes[i]
                                position[i] = new_position
                            elif position[i] >= oriented_lattice_magnitudes[i] - 1e-6:
                                new_position = position[i]
                                while new_position >= oriented_lattice_magnitudes[i] - 1e-6:
                                    new_position -= oriented_lattice_magnitudes[i]
                                position[i] = new_position

                        # accept the atom if the position is not occupied
                        res = search_for_atom(atoms, position, 1e-6)
                        if res is None:
                            new_atom = copy.deepcopy(atom)
                            new_atom.position = position
                            atoms.append(new_atom)

        # TODO: implement rotation
        return atoms, oriented_lattice_vectors
