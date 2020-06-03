import numpy as np

from atompack.atom import Atom
from atompack.internal import (is_point_in_polyhedron, metric_tensor, search_for_atom)


def test_is_point_in_polyhedron_inside():
    point = [0.5, 0.5, 0.5]
    polyhedron = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert is_point_in_polyhedron(point, polyhedron)


def test_is_point_in_polyhedron_surface():
    point = [0.5, 0.5, 1]
    polyhedron = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert is_point_in_polyhedron(point, polyhedron)


def test_is_point_in_polyhedron_outside():
    point = [1.5, 1.5, 1.5]
    polyhedron = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert not is_point_in_polyhedron(point, polyhedron)


def test_search_for_atom_occupied():
    atoms = [Atom(position=np.array([0, 0, 0]))]
    position = np.array([0, 0, 0])
    res = search_for_atom(atoms, position, 1e-6)
    assert res == 0


def test_search_for_atom_unoccupied():
    atoms = []
    position = np.array([0, 0, 0])
    res = search_for_atom(atoms, position, 1e-6)
    assert res is None


def test_metric_tensor_cubic():
    a, b, c = 2, 2, 2
    alpha, beta, gamma = np.pi / 2, np.pi / 2, np.pi / 2
    tensor = metric_tensor(a, b, c, alpha, beta, gamma)
    assert np.allclose(tensor, np.array([[4, 0, 0], [0, 4, 0], [0, 0, 4]]))
