# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

import multiprocessing as mp
import numpy as np
import time
from functools import partial

from sklearn.decomposition import IncrementalPCA
from tqdm import tqdm

from fototex import R_SPECTRA_PG_DESCRIPTION, R_SPECTRA_SECTOR_PG_DESCRIPTION, INC_PCA_PG_DESCRIPTION, \
    REDUCED_R_SPECTRA_PG_DESCRIPTION, PCA_PG_DESCRIPTION
from fototex._numba import get_radius, get_sectors, get_valid_values, get_valid_values_3d
from fototex.foto_tools import rspectrum, split_into_chunks, pca, standard_deviation, rspectrum_per_sector


def incremental_pca(chunks, n_components, no_data_value, axis, population_mean=None, population_std=None,
                    nb_sectors=None):
    """ Incremental PCA

    :param chunks: iterator over data chunks
    :param n_components: number of dimensions for PCA
    :param no_data_value: no data value
    :param axis: r-spectra axis in data chunks
    :param population_mean: mean of the entire population from which is extracted each chunk
    :param population_std: std of the entire population from which is extracted each chunk
    :param nb_sectors: number of sectors (if None, no sectors)
    :return:
    """
    if nb_sectors is None:
        ipca = IncrementalPCA(n_components=n_components)
    else:
        ipca = [IncrementalPCA(n_components=n_components)] * nb_sectors

    for chunk in chunks:

        if chunk.ndim == 2:
            chunk = get_valid_values(chunk, no_data_value)
        else:
            chunk = get_valid_values_3d(chunk, no_data_value)

        if population_mean is None:
            chunk -= np.expand_dims(chunk.mean(axis=axis), axis=axis)
        else:
            chunk -= np.expand_dims(population_mean, axis=axis)

        if population_std is None:
            chunk /= np.expand_dims(chunk.std(axis=axis), axis=axis)
        else:
            chunk /= np.expand_dims(population_std, axis=axis)

        if nb_sectors:
            ipca = [ipca_.partial_fit(sub_chunk) for ipca_, sub_chunk in zip(ipca, chunk)]
        else:
            ipca.partial_fit(chunk)

    return ipca


def pca_transform(h5, eigen_vectors, chunk_size):
    """ Transform R-spectra to R-spectra reduced using given PCA eigen vectors

    :param h5: H5File with "r-spectra" dataset
    :param eigen_vectors: eigen vectors (numpy array)
    :param chunk_size: size of each chunk to be read and written
    :return:
    """
    nb_chunks = h5["r-spectra"].shape[0] // chunk_size + min(1, h5["r-spectra"].shape[0] % chunk_size)
    h5.reset_dataset("r-spectra-reduced", shape=(h5["r-spectra"].shape[0], eigen_vectors.shape[1]))
    for chunk in tqdm(h5.read("r-spectra", chunk_size), total=nb_chunks, desc="Reduce R-spectra"):
        h5.append("r-spectra-reduced", np.dot(chunk, eigen_vectors))


def pca_transform_sector():
    pass


def mp_h5_r_spectra(foto, nb_processes):
    """ Parallel processing of r-spectra with hdf5 storage

    """
    nb_sample = foto.nb_sampled_frequencies
    foto.h5.reset_dataset("r-spectra", (foto.nb_windows, nb_sample))

    # Pixel coordinates within window
    y, x = np.indices((foto.window_size, foto.window_size))
    radius = get_radius(x, y)

    # For statistics computation (population mean and std)
    sum_of_values = np.zeros(nb_sample)
    sum_of_square_values = np.zeros(nb_sample)
    nb_valid_r_spectra = 0

    # Compute r-spectra chunk by chunk
    pg = tqdm(total=foto.nb_windows // foto.chunk_size + 1, desc=R_SPECTRA_PG_DESCRIPTION)
    for chk_nb, window_generator in enumerate(split_into_chunks(foto.get_window_generator(), foto.chunk_size)):
        with mp.Pool(processes=nb_processes) as pool:
            r_spectra = np.asarray(list(pool.map(partial(rspectrum, radius=radius, window_size=foto.window_size,
                                                         nb_sample=nb_sample, standardize=foto.standardize,
                                                         keep_dc_component=foto.keep_dc_component,
                                                         no_data_value=foto.gdal_no_data_value), window_generator,
                                                 chunksize=500)))
        valid_r_spectra = get_valid_values(r_spectra, foto.no_data_value)
        nb_valid_r_spectra += valid_r_spectra.shape[foto.r_spectra_axis]
        sum_of_values += np.sum(valid_r_spectra, axis=foto.r_spectra_axis)
        sum_of_square_values += np.sum(valid_r_spectra**2, axis=foto.r_spectra_axis)
        foto.h5.append("r-spectra", r_spectra)
        pg.update(1)
    pg.close()

    # Write dataset statistics to attributes
    foto.h5["r-spectra"].attrs['mean'] = sum_of_values / nb_valid_r_spectra
    foto.h5["r-spectra"].attrs['std'] = standard_deviation(nb_valid_r_spectra, sum_of_values, sum_of_square_values)

    # TODO: see if chunksize for Pool.map should not be fixed (500 here)


def mp_h5_r_spectra_sector(foto, nb_processes):
    """ Parallel processing of anisotropic r-spectra with hdf5 storage

    """
    nb_sample = foto.nb_sampled_frequencies

    foto.h5.reset_dataset("r-spectra", (foto.nb_sectors, foto.nb_windows, nb_sample))
    y, x = np.indices((foto.window_size, foto.window_size))
    radius = get_radius(x, y)
    sectors = get_sectors(x, y, foto.nb_sectors, foto.start_sector)

    # Data used for population statistics
    sum_of_values = np.zeros((foto.nb_sectors, nb_sample))
    sum_of_square_values = np.zeros((foto.nb_sectors, nb_sample))
    nb_valid_r_spectra = 0

    # Compute r-spectra chunk by chunk
    pg = tqdm(total=foto.nb_windows // foto.chunk_size + 1, desc=R_SPECTRA_SECTOR_PG_DESCRIPTION)
    # desc=f"Compute anisotropic R-spectra for {foto.nb_sectors} sectors, starting from "
    #      f" {foto.start_sector * 180 / np.pi:.0f}° ({degrees_to_cardinal(foto.start_sector * 180 / np.pi)})")

    for chk_nb, window_generator in enumerate(split_into_chunks(foto.get_window_generator(), foto.chunk_size)):
        with mp.Pool(processes=nb_processes) as pool:
            r_spectra = list(pool.map(partial(rspectrum_per_sector, radius=radius, sectors=sectors,
                                              window_size=foto.window_size, nb_sample=nb_sample,
                                              nb_sectors=foto.nb_sectors, standardize=foto.standardize,
                                              keep_dc_component=foto.keep_dc_component,
                                              no_data_value=foto.gdal_no_data_value), window_generator, chunksize=500))
        r_spectra = np.transpose(np.asarray(r_spectra), (1, 0, 2))
        valid_r_spectra = get_valid_values_3d(r_spectra, foto.no_data_value)
        nb_valid_r_spectra += valid_r_spectra.shape[foto.r_spectra_axis]
        sum_of_values += np.sum(valid_r_spectra, axis=foto.r_spectra_axis)
        sum_of_square_values += np.sum(valid_r_spectra ** 2, axis=foto.r_spectra_axis)
        foto.h5.append("r-spectra", r_spectra, axis=foto.r_spectra_axis)
        pg.update(1)
    pg.close()

    # Write dataset statistics to attributes
    foto.h5["r-spectra"].attrs['mean'] = sum_of_values / nb_valid_r_spectra
    foto.h5["r-spectra"].attrs['std'] = standard_deviation(nb_valid_r_spectra, sum_of_values, sum_of_square_values)


def mp_r_spectra(foto, nb_processes):
    """ Parallel processing of isotropic r-spectra in memory

    """
    nb_sample = foto.nb_sampled_frequencies

    # Pixel coordinates within window
    y, x = np.indices((foto.window_size, foto.window_size))
    radius = get_radius(x, y)

    # Parallel computation of r-spectra
    with mp.Pool(processes=nb_processes) as pool:
        r_spectra = list(tqdm(pool.imap(partial(rspectrum, radius=radius, window_size=foto.window_size,
                                                nb_sample=nb_sample, standardize=foto.standardize,
                                                keep_dc_component=foto.keep_dc_component,
                                                no_data_value=foto.gdal_no_data_value), foto.get_window_generator(),
                                        chunksize=500), total=foto.nb_windows, unit_scale=True,
                              desc=R_SPECTRA_PG_DESCRIPTION))

    return np.asarray(r_spectra)


def mp_r_spectra_sector(foto, nb_processes):
    """ Parallel processing of r-spectra

    """
    nb_sample = foto.nb_sampled_frequencies

    # Get radius and sectors within window
    y, x = np.indices((foto.window_size, foto.window_size))
    radius = get_radius(x, y)
    sectors = get_sectors(x, y, foto.nb_sectors, foto.start_sector)

    # Parallel computation of r-spectra
    with mp.Pool(processes=nb_processes) as pool:
        r_spectra = list(tqdm(pool.imap(partial(rspectrum_per_sector, radius=radius, sectors=sectors,
                                                window_size=foto.window_size, nb_sample=nb_sample,
                                                nb_sectors=foto.nb_sectors, standardize=foto.standardize,
                                                keep_dc_component=foto.keep_dc_component,
                                                no_data_value=foto.gdal_no_data_value), foto.get_window_generator(),
                                        chunksize=500), total=foto.nb_windows, unit_scale=True,
                              desc=R_SPECTRA_SECTOR_PG_DESCRIPTION))
        r_spectra = np.transpose(np.asarray(r_spectra), (1, 0, 2))

    return r_spectra


def h5_incremental_pca(foto, at_random, batch_size, max_iter):
    """ Incremental PCA based on hdf5 dataset chunks

    """
    nb_chunks = foto.nb_windows // foto.chunk_size + min(1, foto.nb_windows % foto.chunk_size)
    population_mean = foto.h5["r-spectra"].attrs["mean"]
    population_std = foto.h5["r-spectra"].attrs["std"]

    if at_random:
        if batch_size is None:
            batch_size = foto.nb_sampled_frequencies * 2**3
        r_spectra_generator = foto.h5.read_at_random("r-spectra", batch_size)
        nb_iterations = max_iter
    else:
        r_spectra_generator = foto.h5.read("r-spectra", foto.chunk_size)
        nb_iterations = nb_chunks

    # Incremental PCA
    # Read R-spectra by chunk or batch (if at random) and partial fit
    chunks = tqdm(r_spectra_generator, total=nb_iterations, desc=INC_PCA_PG_DESCRIPTION)
    ipca = incremental_pca(chunks, foto.nb_pca_components, foto.no_data_value, foto.r_spectra_axis,
                           population_mean, population_std)

    # Finalization
    # Write R-spectra reduced to hdf5 dataset
    foto.h5.reset_dataset("r-spectra-reduced", shape=(foto.nb_windows, foto.nb_pca_components))
    for r_spectra in tqdm(foto.h5.read("r-spectra", foto.chunk_size), total=nb_chunks,
                          desc=REDUCED_R_SPECTRA_PG_DESCRIPTION):
        r_spectra_reduced = np.full((r_spectra.shape[0], foto.nb_pca_components), foto.no_data_value,
                                    dtype=r_spectra.dtype)
        valid_r_spectra = (get_valid_values(r_spectra, foto.no_data_value) - population_mean) / population_std
        r_spectra_reduced[r_spectra[:, 0] != foto.no_data_value, :] = ipca.transform(valid_r_spectra)
        foto.h5.append("r-spectra-reduced", r_spectra_reduced)

    return ipca.components_.T


def h5_incremental_pca_sector(foto, at_random, batch_size, max_iter):
    """ Apply incremental PCA for anisotropic r-spectra based on H5 datasets

    """
    nb_chunks = foto.nb_windows // foto.chunk_size + min(1, foto.nb_windows % foto.chunk_size)
    population_mean = foto.h5["r-spectra"].attrs["mean"]
    population_std = foto.h5["r-spectra"].attrs["std"]

    if at_random:
        if batch_size is None:
            batch_size = foto.nb_sampled_frequencies * 2**3
        r_spectra_generator = foto.h5.read_at_random("r-spectra", batch_size, axis=foto.r_spectra_axis)
        nb_iterations = max_iter
    else:
        r_spectra_generator = foto.h5.read("r-spectra", foto.chunk_size, axis=foto.r_spectra_axis)
        nb_iterations = nb_chunks

    # Incremental PCA
    # Read R-spectra by chunk or batch (if at random) and partial fit
    chunks = tqdm(r_spectra_generator, total=nb_iterations, desc=INC_PCA_PG_DESCRIPTION)
    ipca = incremental_pca(chunks, foto.nb_pca_components, foto.no_data_value, foto.r_spectra_axis,
                           population_mean, population_std, foto.nb_sectors)

    # Finalization
    # Write R-spectra reduced to hdf5 dataset
    foto.h5.reset_dataset("r-spectra-reduced", shape=(foto.nb_sectors, foto.nb_windows, foto.nb_pca_components))
    for r_spectra in tqdm(foto.h5.read("r-spectra", foto.chunk_size, axis=foto.r_spectra_axis),
                          total=nb_chunks, desc=REDUCED_R_SPECTRA_PG_DESCRIPTION):
        r_spectra_reduced = np.full((foto.nb_sectors, r_spectra.shape[1], foto.nb_pca_components),
                                    foto.no_data_value, dtype=r_spectra.dtype)
        valid_r_spectra = get_valid_values_3d(r_spectra, foto.no_data_value)
        valid_r_spectra -= np.expand_dims(population_mean, axis=foto.r_spectra_axis)
        valid_r_spectra /= np.expand_dims(population_std, axis=foto.r_spectra_axis)
        ipca_transform = np.asarray([ipca_.transform(sector_r_spectra)
                                     for ipca_, sector_r_spectra in zip(ipca, valid_r_spectra)])
        r_spectra_reduced[:, r_spectra[0, :, 0] != foto.no_data_value, :] = ipca_transform
        foto.h5.append("r-spectra-reduced", r_spectra_reduced, axis=foto.r_spectra_axis)

    return [ipca_.components_.T for ipca_ in ipca]


def normal_pca(foto):
    """ Normal PCA

    """
    valid_r_spectra = get_valid_values(foto.r_spectra, foto.no_data_value)

    def _tqdm_pca():
        bar_length = valid_r_spectra.size // 100
        pg = tqdm(total=bar_length, desc=PCA_PG_DESCRIPTION, unit_scale=True)
        for i in range(int(bar_length)):
            pg.update(1)
            time.sleep(0.0001)
            if quit_process.is_set():
                break
        pg.n = bar_length
        pg.refresh()
        pg.close()

    quit_process = mp.Event()
    p = mp.Process(target=_tqdm_pca)
    p.start()

    r_spectra_reduced = np.full((foto.nb_windows, foto.nb_pca_components), foto.no_data_value,
                                dtype=foto.r_spectra.dtype)
    eigen_vectors, r_spectra_reduced[foto.r_spectra[:, 0] != foto.no_data_value, :] = \
        pca(valid_r_spectra, foto.nb_pca_components)
    # eigen_vectors, r_spectra_reduced = pca(foto.r_spectra, foto.nb_pca_components)

    # Stop PCA process
    quit_process.set()
    p.join()

    return eigen_vectors, r_spectra_reduced


def normal_pca_sector(foto):
    """ Compute PCA for each quadrant

    """
    valid_r_spectra = get_valid_values_3d(foto.r_spectra, foto.no_data_value)

    def _tqdm_pca():
        bar_length = foto.nb_sectors * valid_r_spectra.size // 100
        pg = tqdm(total=bar_length, desc=PCA_PG_DESCRIPTION, unit_scale=True)
        for i in range(int(bar_length)):
            pg.update(1)
            time.sleep(0.0001)
            if quit_process.is_set():
                break
        pg.n = bar_length
        pg.refresh()
        pg.close()

    quit_process = mp.Event()
    p = mp.Process(target=_tqdm_pca)
    p.start()

    r_spectra_reduced = np.full((foto.nb_sectors, foto.nb_windows, foto.nb_pca_components),
                                foto.no_data_value, dtype=foto.r_spectra.dtype)
    results = [pca(rspec, foto.nb_pca_components) for rspec in valid_r_spectra]
    eigen_vectors = np.asarray([result[0] for result in results])
    r_spectra_reduced[:, foto.r_spectra[0, :, 0] != foto.no_data_value, :] = np.asarray([result[1]
                                                                                         for result in results])

    # Stop PCA process
    quit_process.set()
    p.join()

    return eigen_vectors, r_spectra_reduced
