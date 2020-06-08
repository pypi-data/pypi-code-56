from astropy.io import fits
import subprocess
import os
from cadc_iq_checker import storage
from cadc_iq_checker import config


class LDAC(object):
    """
    Source Extractor LDAC file.
    """
    IMHEAD_EXTNAME = "LDAC_IMHEAD"
    HEADER_COLNAME = "Field Header Card"
    CATALOG_EXTNAME = "LDAC_OBJECTS"
    LDAC_EXTENTION = "ldac"

    def __init__(self, observation_id=None):

        self.observation_id = observation_id
        self.ldac_filename = "{}.ldac".format(self.observation_id)
        if not os.access(self.ldac_filename, os.R_OK):
            # try retrieving image and running sExtractor
            self._run_sex()
            if not os.access(self.ldac_filename, os.R_OK):
                raise IOError("Must be supplied with name of LDAC file to ingest")
        self.__header = None
        self.__data = None

    @property
    def header(self):
        """
        Image header extracted from sExtractor LDAC file.
        :return: image header as stored in LDAC file by sExtractor
        :rtype fits.Header
        """

        if self.__header is None:
            with fits.open(self.ldac_filename) as hdulist:
                self.__header = fits.Header.fromstring('\n'.join(hdulist[LDAC.IMHEAD_EXTNAME].
                                                                 data[LDAC.HEADER_COLNAME][0]), sep='\n')

        return self.__header

    def _run_sex(self):
        fits_filename = "{}.fits".format(self.observation_id)
        if not os.access(fits_filename, os.R_OK):
            assert fits_filename == storage.get_observation(self.observation_id)
        args = [config.SEX_EXECUTABLE, fits_filename,
                '-c', config.DEFAULT_SEX,
                '-CATALOG_NAME', self.ldac_filename]
        subprocess.run(args).check_returncode()

    @property
    def data(self):
        """
        sExtactor output catalog as an numpy table.
        :return: np.recarray
        """
        if self.__data is None:
            with fits.open(self.ldac_filename) as hdulist:
                self.__data = hdulist[LDAC.CATALOG_EXTNAME].data
        return self.__data
