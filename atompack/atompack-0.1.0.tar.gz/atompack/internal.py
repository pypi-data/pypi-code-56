import numpy as np


def search_for_atom(atoms, position, tolerance):
    index = None
    for i, atom in enumerate(atoms):
        if np.linalg.norm(atom.position - position) < tolerance:
            index = i
            break
    return index


def metric_tensor(a, b, c, alpha, beta, gamma):
    return np.array([[a * a, a * b * np.cos(gamma), a * c * np.cos(beta)],
                     [a * b * np.cos(gamma), b * b, b * c * np.cos(alpha)],
                     [a * c * np.cos(beta), b * c * np.cos(alpha), c * c]])


# This function is not used but I spent so long figuring out how to do it that I refuse to delete it.
def is_point_in_polyhedron(point, poly):
    for face, normal in zip(_polyhedron_faces(poly), _polyhedron_normals(poly)):
        p2f = face[0] - point
        d = np.dot(p2f, normal / np.linalg.norm(p2f))
        if d < -1e-6:
            return False
    return True


def _polyhedron_vertices(poly):
    return np.array([
        [0.0, 0.0, 0.0],  # origin
        poly[0],  # x corner
        poly[1],  # y corner
        poly[2],  # z corner
        [
            poly[0][0] + poly[1][0],
            poly[0][1] + poly[1][1],
            poly[0][2] + poly[1][2],
        ],  # xy corner
        [
            poly[0][0] + poly[2][0],
            poly[0][1] + poly[2][1],
            poly[0][2] + poly[2][2],
        ],  # xz corner
        [
            poly[1][0] + poly[2][0],
            poly[1][1] + poly[2][1],
            poly[1][2] + poly[2][2],
        ],  # yz corner
        [
            poly[0][0] + poly[1][0] + poly[2][0],
            poly[0][1] + poly[1][1] + poly[2][1],
            poly[0][2] + poly[1][2] + poly[2][2],
        ],  # xyz corner
    ])


def _polyhedron_faces(poly):
    vertices = _polyhedron_vertices(poly)
    return np.array([
        [vertices[4], vertices[1], vertices[2]],  # lower xy
        [vertices[7], vertices[6], vertices[5]],  # upper xy
        [vertices[5], vertices[3], vertices[1]],  # rear xz
        [vertices[2], vertices[6], vertices[4]],  # front xz
        [vertices[6], vertices[2], vertices[3]],  # left yz
        [vertices[1], vertices[4], vertices[5]],  # right yz
    ])


def _polyhedron_normals(poly):
    faces = _polyhedron_faces(poly)
    normals = np.zeros((6, 3))
    for i, face in enumerate(faces):
        a = face[1] - face[0]
        b = face[2] - face[0]
        n = np.cross(a, b)
        d = np.linalg.norm(n)
        normals[i] = n / d
    return normals
