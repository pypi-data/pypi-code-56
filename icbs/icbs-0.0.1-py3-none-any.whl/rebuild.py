import numpy as np
import statistics


def reorder_cut_img(images, n_img_per_col):
    """
    :param images: list of 3d images
    :param n_img_per_col: number of images per col
    :return: a matrix of images [n_img_per_col][len(images) - n_img_per_col]
    """
    print("rebuilding preparation")
    m_img = []
    test = len(images)
    n_img_per_row = len(images) // n_img_per_col
    for r in range(n_img_per_col):
        # new row
        m_img.append([])
        for c in range(n_img_per_row):
            # we are at the image: r * n_img_per_row + c
            m_img[r].append(images[r * n_img_per_row + c])
    # now we should have each image in the right place (as in sol of the tests for cut)
    return m_img


def step1_to_rebuild(m_images, n_s_row_max, n_s_col_max, overlap_w, overlap_h, W=4172, H=1202):
    """
    :param m_images: matrix of images
    :param n_s_row_max: number of rows max for each img
    :param n_s_col_max: number of cols max for each img
    :param overlap_w:
    :param overlap_h:
    :param W: width of the original img
    :param H: height of the original img
    :return: a matrix of list of pixels as big as the original image
    """
    print("start step 1 rebuilding")
    img_step1 = [[[] for i in range(W)] for j in range(H)]
    for r in range(len(m_images)):
        for c in range(len(m_images[r])):
            c_in_step_2, r_in_step_2 = get_start_index(r, c, overlap_w, overlap_h, n_s_row_max, n_s_col_max)

            # To handle easily edge cases
            if c == len(m_images[r]) - 1:
                c_in_step_2 = W - len(m_images[r][c][0])
            if r == len(m_images) - 1:
                r_in_step_2 = H - len(m_images[r][c])

            # print("c: ", c_in_step_2, " w: ", r_in_step_2)

            for r1 in m_images[r][c]:
                tmp = c_in_step_2
                for c1 in r1:
                    img_step1[r_in_step_2][tmp].append(c1)
                    tmp += 1
                r_in_step_2 += 1
    return img_step1


def get_start_index(r, c, overlap_w, overlap_h, n_s_row_max, n_s_col_max):
    # It does not handle edge cases
    pad_h = n_s_row_max - overlap_h
    pad_w = n_s_col_max - overlap_w
    return c * pad_w, r * pad_h


def final_step_rebuild(img_step1, interpolator=lambda x: mean(x)):
    """
    :param img_step1: return image of step1_to_rebuild
    :param interpolator: function which decide how to handle the overlapped value of the pixels
    :return: starting image
    """
    print("start rebuilding")
    img_final = []
    for r in range(len(img_step1)):
        # add row
        img_final.append([])
        for c in range(len(img_step1[r])):
            param = [[] for i in range(len(img_step1[r][c][0]))]
            for p in range(len(img_step1[r][c])):
                for v in range(len(img_step1[r][c][p])):
                    param[v].append(img_step1[r][c][p][v])
            pix_to_add = []
            for l_to_int in param:
                pix_to_add.append(interpolator(l_to_int))
            # add pix
            img_final[r].append(pix_to_add)
    print("rebuilt")
    return img_final


def mean(l):
    return statistics.mean(l)


def median(l):
    return statistics.median(l)


def rebuild(images, n_img_per_col, n_s_row_max, n_s_col_max, overlap_w, overlap_h,
            W=4172, H=1202, interpolator=lambda x: mean(x)):
    """
    :param images: list of images
    :param n_img_per_col: number of images per col (regarding original img)
    :param n_s_row_max: max number of rows for single image
    :param n_s_col_max: max number of cols for single image
    :param overlap_w: overlap value on w
    :param overlap_h: overlap value on h
    :param W: W of original image in pix
    :param H: H of original image in pix
    :param interpolator: function which decide how to handle the overlapped value of the pixels
    :return: image rebuilt
    """
    m_images = reorder_cut_img(images, n_img_per_col)
    step1 = step1_to_rebuild(m_images, n_s_row_max, n_s_col_max, overlap_w, overlap_h, W, H)
    return final_step_rebuild(step1, interpolator)
