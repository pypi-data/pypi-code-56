import cv2
from multiprocessing import Pool


def run_read_img(i, framepath):
    return cv2.imread(framepath)


def parallel_read_img(framepaths, workers=48):
    pool = Pool(workers)
    framelist = pool.starmap(
        run_read_img,
        [(i, framepath) for i, framepath in enumerate(framepaths)])
    return framelist
