import copy
from typing import List, Optional

import numpy as np

from atompack.error import PositionOccupiedError, PositionUnoccupiedError
from atompack.internal import search_for_atom


class Atom(object):
    """A flexible data structure which represents an atom.
    
    All kwargs are dynamically set as attributes.
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        s = "atompack.atom.Atom: {"
        for attr in dir(self):
            if not attr.startswith("__"):
                value = getattr(self, attr)
                s += " {} = {},".format(attr, value)
        return s + " }"

    def __str__(self) -> str:
        return self.__repr__()


class AtomCollection(object):
    """A collection of `Atom`s.
    
    Args:
        atoms: The `Atom`s to insert into the collection.
        basis: A 3x3 matrix defining the collection's coordinate system.
    """

    def __init__(self, atoms: Optional[List[Atom]] = None, basis: Optional[np.ndarray] = None) -> None:
        self._iter_index = 0
        if atoms is None:
            atoms = []
        if basis is None:
            basis = np.identity(3)
        self.atoms = atoms
        self.basis = basis

    def insert(self, atom: Atom, tolerance: float) -> None:
        """Inserts an `Atom` into the collection if none exist within the radius of tolerance around the given position.

        Args:
            atom: The `Atom` to insert into the collection.
            tolerance: The radius of tolerance.

        Raises:
            `atompack.error.PositionOccupiedError`: An `Atom` exists within the tolerance radius of the one being inserted.

        Example:
            >>> import numpy as np
            >>> from atompack.atom import Atom, AtomCollection
            >>>
            >>> collection = AtomCollection()
            >>> new_atom = Atom(position=np.array([1.0, 1.0, 1.0]))
            >>> collection.insert(new_atom, 1e-6)
            >>>
            >>> assert len(collection) == 1
        
        Note:
            This method requires that all `Atom`s in the collection and the one being inserted have a `position` attribute which is a 3D vector indicating their positions in the collection.
            This attribute is expected to be of type `numpy.ndarray`.
        """
        res = search_for_atom(self.atoms, atom.position, tolerance)
        if res is None:
            self.atoms.append(atom)
        else:
            raise PositionOccupiedError(atom.position, tolerance)

    def remove(self, position: np.ndarray, tolerance: float) -> Atom:
        """Removes and returns an `Atom` from the collection if one exists within the radius of tolerance around the given position.

        Args:
            position: The location of the `Atom` to remove.
            tolerance: The radius of tolerance.

        Raises:
            `atompack.error.PositionUnoccupiedError`: No `Atom`s exist within the tolerance radius of the given position.

        Example:
            >>> import numpy as np
            >>> from atompack.atom import Atom, AtomCollection
            >>>
            >>> atoms = [Atom(symbol="H", position=np.array([0.0, 0.0, 0.0]))]
            >>> collection = AtomCollection(atoms=atoms)
            >>> position = np.array([0.0, 0.0, 0.0])
            >>> atom = collection.remove(position, 1e-6)
            >>>
            >>> assert atom.symbol == "H"
            >>> assert len(collection) == 0

        Note:
            This method requires that all `Atom`s in the collection and the one being inserted have a `position` attribute which is a 3D vector indicating their positions in the collection.
            This attribute is expected to be of type `numpy.ndarray`.
        """
        res = search_for_atom(self.atoms, position, tolerance)
        if res is None:
            raise PositionUnoccupiedError(position, tolerance)
        else:
            atom = copy.deepcopy(self.atoms[res])
            del self.atoms[res]
            return atom

    def select(self, position: np.ndarray, tolerance: float) -> int:
        """Returns the index of an `Atom` in the collection if one exists within the radius of tolerance around the given position.

        Args:
            position: The location of the `Atom` to remove.
            tolerance: The radius of tolerance.

        Raises:
            `atompack.error.PositionUnoccupiedError`: No `Atom`s exist within the tolerance radius of the given position.
        
        Example:
            >>> import numpy as np
            >>> from atompack.atom import Atom, AtomCollection
            >>>
            >>> atoms = [Atom(symbol="H", position=np.array([0.0, 0.0, 0.0]))]
            >>> collection = AtomCollection(atoms=atoms)
            >>> position = np.array([0.0, 0.0, 0.0])
            >>> index = collection.select(position, 1e-6)
            >>>
            >>> assert collection.atoms[index].symbol == "H"
            >>> assert len(collection) == 1

        Note:
            This method requires that all `Atom`s in the collection and the one being inserted have a `position` attribute which is a 3D vector indicating their positions in the collection.
            This attribute is expected to be of type `numpy.ndarray`.
        """
        res = search_for_atom(self.atoms, position, tolerance)
        if res is None:
            raise PositionUnoccupiedError(position, tolerance)
        else:
            return res

    def __iter__(self) -> 'AtomCollection':
        return self.atoms.__iter__()

    def __len__(self) -> int:
        return len(self.atoms)
