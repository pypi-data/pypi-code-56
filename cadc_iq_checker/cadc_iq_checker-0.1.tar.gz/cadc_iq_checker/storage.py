import os
import vos
from astropy.io import fits
from . import config


def _download_from_vospace(source, dest):
    """
    Download VOSpace file 'source' and place at 'dest'
    """
    c = vos.Client()
    c.copy(source, dest)


def get_model_file(model, base_vospace=config.VOSPACE_MODEL_DIRECTORY, model_directory=os.getenv("TMPDIR")):
    """
    Retreive the ML Model files needed for cadc_iq_checker
    """
    source = os.path.join(base_vospace, model)
    destination = os.path.join(model_directory, model)
    if not os.access(destination, os.R_OK):
        _download_from_vospace(source, destination)
    return destination


def get_observation(observation_id, base_vospace=config.VOSPACE_BASE_DIRECTORY):
    """
    Make a single extension FITS image from a LSST pipeline produce SC_CORR image.

    :param observation_id: ID of the file to be processed.
    :param base_vospace: directory in VOSpace where files are stored.
    :return: fits_filename
    """

    fz_filename = "{}.fits.fz".format(observation_id)
    fits_filename = "{}.fits".format(observation_id)
    if not os.access(fz_filename, os.R_OK):
        c = vos.Client()
        c.copy('{}/{}'.format(base_vospace, fz_filename), ".")
    hdulist = fits.open('{}.fz'.format(fits_filename))
    # Make the Image extension inherit the PrimaryHDU header
    assert hdulist[1].header['EXTTYPE'] == 'IMAGE'
    for key in hdulist[0].header:
        try:
            hdulist[1].header[key] = hdulist[1].header.get(key, hdulist[0].header[key])
        except ValueError:
            pass
    fits.PrimaryHDU(data=hdulist[1].data,
                    header=hdulist[1].header).writeto(fits_filename)
    return fits_filename
