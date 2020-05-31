import numpy as np


W = 4172  # 4 * 7 * 149
H = 1202  # 2 * 601


def cut(np_img, n_s_row_max, n_s_col_max, overlap_w=-1, overlap_h=-1):
    """
    :return the image cut in pieces and the number of images per column.
            The pieces are overlapping, you can set how much with the overlap_w and overlap_h params.
    :param np_img: image as numpy array
    :param n_s_row_max: number of rows expected in each single image returned (it can change in the edge cases)
    :param n_s_col_max: number of columns expected in each single image returned (it can change in the edge cases)
    :param overlap_w: how much the images overlap with each other on the x axis. (it is guaranteed to be constant)
                if it's -1 it is set to half the width of the img
    :param overlap_h: how much the images overlap with each other on the y axis. (it is guaranteed to be constant)
                if it's -1 it is set to half the height of the img
    """
    W = np_img.shape[1]
    H = np_img.shape[0]
    def_overlaps = get_default_overlaps(n_s_row_max, n_s_col_max)
    if overlap_h == -1:
        overlap_h = def_overlaps[0]
    if overlap_w == -1:
        overlap_w = def_overlaps[1]
    n_img_per_col = 0
    # pad tells how much should we move when changing index while looping
    pad_w = n_s_col_max - overlap_w
    pad_h = n_s_row_max - overlap_h
    if overlap_w >= n_s_col_max or overlap_h >= n_s_row_max:
        raise ValueError("overlap is major than the size of the cut img")
    h_rem = get_rem(H, n_s_row_max, pad_h)
    w_rem = get_rem(W, n_s_col_max, pad_w)

    ret_img = []
    # dim_img contains the width and height of each img. it can be useful for reconstruction.
    for i in get_range(H, n_s_row_max, pad_h):
        n_img_per_col += 1
        slice_rows = get_slice(i, n_s_row_max, pad_h)
        for j in get_range(W, n_s_col_max, pad_w):
            slice_cols = get_slice(j, n_s_col_max, pad_w)
            ret_img.append(np_img[slice_rows, slice_cols, :])
        # handle remaining w
        if not (w_rem == 0):
            # There is some w left
            # we have to be sure that overlaps overlap_w
            slice_rows = get_slice(i, n_s_row_max, pad_h)
            ret_img.append(np_img[slice_rows, get_edge_start_slice(w_rem, overlap_w):, :])
    # handle remaining h
    if not (h_rem == 0):
        # There is some h left
        # we have to be sure that overlaps overlap_h
        n_img_per_col += 1
        h_start_slice = get_edge_start_slice(h_rem, overlap_h)
        for j in get_range(W, n_s_col_max, pad_w):
            slice_cols = get_slice(j, n_s_col_max, pad_w)
            ret_img.append(np_img[h_start_slice:, slice_cols, :])
        if not (w_rem == 0):
            # There is some w left
            # we have to be sure that overlaps overlap_w
            ret_img.append(np_img[h_start_slice:, get_edge_start_slice(w_rem, overlap_w):, :])
    return [ret_img, n_img_per_col]


def get_rem(dim, n_s_dim, pad):
    rem = 0
    if ((dim - n_s_dim) // pad) * pad != dim - n_s_dim:
        rem = (dim - n_s_dim) % pad
    return rem


def get_dim_imgs(cut_imgs):
    """
    :param cut_imgs: list of images after the cut
    :return: dimensions of images
    """
    dim = []
    for i in cut_imgs:
        n = i
        dim.append(np.asarray(i).shape)
    return dim


def get_default_overlaps(n_s_row_max, n_s_col_max):
    """
    comfortable for not defining new overlaps every time
    :param n_s_row_max: max number of rows in cut images
    :param n_s_col_max: max number of cols in cut images
    :return: our defined default overlaps
    """
    return [(n_s_row_max // 2), (n_s_col_max // 2)]


def get_slice(index, length, pad):
    """
    Given the index at which we are it returns the slice of the next img.
    (the operation is the same for width and height).
    """
    slice_ret = slice(pad * index, (pad * index) + length)
    return slice_ret


def get_edge_start_slice(rem, overlap):
    """
    :param rem: remaining dim value (W or H)
    :param overlap: overlap value
    :return: return the start point of the slice in the edge case (both in h and w)
    """
    start = (- rem - overlap)
    return start


def get_range(dim_orig_im, n_s_dim_max, pad):
    """
    Useful to give less importance to the remaining value (edge cases).
    """
    r = range(((dim_orig_im - n_s_dim_max) // pad + 1))
    return r