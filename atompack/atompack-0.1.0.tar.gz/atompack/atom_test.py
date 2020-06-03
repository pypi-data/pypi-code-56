import numpy as np
import pytest

from atompack.atom import Atom, AtomCollection
from atompack.error import PositionOccupiedError, PositionUnoccupiedError


def test_atom_collection_is_iterable():
    atoms = [Atom(position=np.array([0, 0, 0]))]
    collection = AtomCollection(atoms=atoms)
    lst = [atom for atom in collection]
    assert len(lst) == 1


def test_atom_collection_insert_occupied():
    atoms = [Atom(position=np.array([0, 0, 0]))]
    collection = AtomCollection(atoms=atoms)
    new_atom = Atom(position=np.array([0, 0, 0]))
    with pytest.raises(PositionOccupiedError):
        collection.insert(new_atom, 1e-6)


def test_atom_collection_insert_unoccupied():
    atoms = [Atom(position=np.array([0, 0, 0]))]
    collection = AtomCollection(atoms=atoms)
    new_atom = Atom(position=np.array([1, 1, 1]))
    collection.insert(new_atom, 1e-6)
    assert len(collection) == 2


def test_atom_collection_remove_occupied():
    atoms = [Atom(position=np.array([0, 0, 0]), symbol="H")]
    collection = AtomCollection(atoms=atoms)
    position = np.array([0, 0, 0])
    atom = collection.remove(position, 1e-6)
    assert atom.symbol == "H"
    assert len(collection) == 0


def test_atom_collection_remove_unoccupied():
    atoms = [Atom(position=np.array([0, 0, 0]))]
    collection = AtomCollection(atoms=atoms)
    position = np.array([1, 1, 1])
    with pytest.raises(PositionUnoccupiedError):
        collection.remove(position, 1e-6)


def test_atom_collection_select_occupied():
    atoms = [Atom(position=np.array([0, 0, 0]), symbol="H")]
    collection = AtomCollection(atoms=atoms)
    position = np.array([0, 0, 0])
    index = collection.select(position, 1e-6)
    assert collection.atoms[index].symbol == "H"
    assert len(collection) == 1


def test_atom_collection_select_unoccupied():
    atoms = [Atom(position=np.array([0, 0, 0]))]
    collection = AtomCollection(atoms=atoms)
    position = np.array([1, 1, 1])
    with pytest.raises(PositionUnoccupiedError):
        collection.select(position, 1e-6)
