import os
from collections import Counter
from .storage import get_model_file
import numpy as np
import sompy
from astropy.io import fits
from astropy.nddata.utils import Cutout2D
from keras.models import load_model

from . import config
from .catalog import LDAC


class ImageQualityModel(object):
    """
    A class to hold the various parts of the image quality model.
    """
    def __init__(self, obs_id, ccd,
                 deep_model=config.DEEP_MODEL,
                 som_model=config.SOM_MODEL, som_labels=config.SOM_LABELS,
                 basename='SC_CORR'):
        """

        :param obs_id: Image to classify
        :param ccd: ccd of that image to classify.
        :param deep_model: .h5 formatted keras model that classifies based on image cutouts
        :param som_model: A self organizing map that classifies based on sExtractor measures of sources
        :param som_labels: labels assigned to clusters within the som_model
        """
        self.observation_id = "{}-{:07d}-{:03d}".format(basename,
                                                        obs_id,
                                                        ccd)
        try:
            self.ldac = LDAC(self.observation_id)
        except Exception as ex:
            raise IOError("Failed to open LDAC file for: {}, error: {}".format(self.observation_id, ex))

        self.fits_filename = self.ldac.header['FITSFILE']
        try:
            self.fits_hdulist = fits.open(self.fits_filename)
        except Exception as ex:
            raise IOError("Failed to open file assocaited with LDAC: {}, error: {}".format(self.fits_filename,
                                                                                           ex))
        if not os.access(deep_model, os.R_OK):
            deep_model = get_model_file(os.path.basename(deep_model))
        self.deep_model = load_model(deep_model, compile=False)
        if not os.access(som_model,os.R_OK):
            som_model = get_model_file(os.path.basename(som_model))
        self.som_model = np.load(som_model, allow_pickle=True)[0]
        if not isinstance(self.som_model, sompy.sompy.SOM):
            raise ValueError("MODEL FILE PROVIDED IS NOT A SOM MODEL.")
        if not os.access(som_labels, os.R_OK):
            som_labels = get_model_file(os.path.basename(som_labels))
        self.som_labels = np.load(som_labels, allow_pickle=True)[0]

        self.som_model_sex_params = ["ISO0", "ELLIPTICITY", "CLASS_STAR", "EXPN", "BGN"]
        self._cat_data = self._map = self._project_data = self._map_data = self._repr_sources = None
        self._model_input_data = self._rep_sources_xy = None
        self.cutout_dimensions = (25, 25)

    @property
    def project_data(self):
        """
        Project source measurements in ldac file onto the SOM.

        Returns a map of the frequency versus map value (heat map of data on this map).
        :return:
        """
        if self._project_data is None:
            self._project_data = self.som_model.project_data(self.map_data)
        return self._project_data

    @property
    def map(self):
        """
        Return a density map of ldac projected onto the SOM.

        Returns a map of the frequency versus map value (heat map of data on this map).
        :return:
        """
        if self._map is None:
            _cv = Counter(self.project_data)
            self._map = np.zeros(self.som_model.codebook.mapsize[0] * self.som_model.codebook.mapsize[1])
            self._map[list(_cv.keys())] = list(_cv.values())
        return self._map

    @property
    def map_data(self):
        """
        Return those parts of the catalog used for the mapping.

        These data array parts are referenced by array column number, not labels.
        :return: map_data
        :rtype np.array
        """
        if self._map_data is None:
            self._map_data = self.cat_data[:, [0, 1, 2, 3, 4]]
        return self._map_data

    @property
    def cat_data(self):
        """
        Extract from the LDAC catalog the sources and values used for classification.

        The catalog values are engineered based on fixed rules appropriate to the SOM being mapped onto.

        :return: cat_data
        :rtype np.array
        """

        if self._cat_data is None:
            exptime = float(self.ldac.header.get("EXPTIME", 30))
            naxis1 = int(self.ldac.header.get("NAXIS1", 2100))
            naxis2 = int(self.ldac.header.get("NAXIS2", 4600))
            dx = self.cutout_dimensions[0]//2
            dy = self.cutout_dimensions[1]//2
            tps = self.ldac.data
            padding = 5
            tps = tps[(tps['X_IMAGE'] > dx + padding) & \
                      (tps['Y_IMAGE'] > dy + padding) & \
                      (tps['X_IMAGE'] < naxis1 - dx - padding) & \
                      (tps['Y_IMAGE'] < naxis2 - dy - padding) & \
                      (tps['FLAGs'] < 5)]

            iso0 = tps['ISO0'] + 0.5
            mean_background = tps['BACKGROUND'].mean()
            ellipticity = tps['ELLIPTICITY'].clip(1E-5, 1)
            normalized_background = ((tps['BACKGROUND'] - mean_background) / mean_background).clip(-2, 2)
            normalized_exposure_time = np.log10((np.abs(exptime * (tps['BACKGROUND'] / mean_background))).
                                                clip(1e-5, 30))
            normalized_iso0 = np.log10(iso0.clip(0.00001, 10000))
            self._cat_data = np.array([normalized_iso0,
                                       ellipticity,
                                       tps['CLASS_STAR'],
                                       normalized_exposure_time,
                                       normalized_background,
                                       tps['X_IMAGE'],
                                       tps['Y_IMAGE']]).T
        return self._cat_data

    @property
    def median_background(self):
        return np.median(self.ldac.data['BACKGROUND'])

    @property
    def representative_sources(self):
        """
        Return a list of representative sources from the ldac catalog.
        :return:
        """
        iqm = self
        if self._rep_sources_xy is None:
            # loop over all labels in this som_model
            self._rep_sources_xy = []
            for label in np.unique(iqm.som_labels):
                label_cat_data = iqm.cat_data[iqm.som_labels[iqm.project_data] == label]
                if len(label_cat_data) > 0:
                    sorted_source_args = np.argsort(label_cat_data[:, 0], axis=0)
                    example_source = label_cat_data[sorted_source_args[-1]]
                    self._rep_sources_xy.append(np.array(example_source[5:7]))
                else:
                    self._rep_sources_xy.append([])
        return np.array(self._rep_sources_xy)

    @property
    def model_input_data(self):
        """
        retrieve data array sections for each
        :return:
        """
        if self._model_input_data is None:
            self._model_input_data = [np.log10(self.map+1).reshape(1,  225), ]
            all_cutout_data = None
            for source in self.representative_sources:
                if len(source) == 2:
                    cutout_data = Cutout2D(self.fits_hdulist[self.ldac.header['FITSEXT'] - 1].data,
                                           source, self.cutout_dimensions).data
                    cutout_data -= self.median_background
                else:
                    cutout_data = np.ones(self.cutout_dimensions)
                if all_cutout_data is None:
                    all_cutout_data = cutout_data
                else:
                    all_cutout_data = np.concatenate((all_cutout_data, cutout_data), axis=1)
            self._model_input_data.append(np.log10(np.where(all_cutout_data <= 0, 1, all_cutout_data)).
                                          reshape(1,
                                                  self.cutout_dimensions[0],
                                                  self.cutout_dimensions[1]*len(self.representative_sources),
                                                  1))
        return self._model_input_data

    def compute_image_quality(self):
        probs = self.deep_model.predict([self.model_input_data[1], self._model_input_data[0]])[0]
        return {'GOOD': probs[0], "TRAILED": probs[1], "TRACKING_ERROR": probs[2],
                "POOR_IQ": probs[3], "ILLUMINATION_PROBLEM": probs[4]}
