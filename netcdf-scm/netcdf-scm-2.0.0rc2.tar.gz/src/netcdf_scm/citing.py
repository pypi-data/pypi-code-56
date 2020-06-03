"""
Helper tools for citing `Coupled Model Intercomparison Project <https://www.wcrp-climate.org/wgcm-cmip>`_ data
"""
from .errors import NoLicenseInformationError, NonStandardLicenseError


def check_license(scmdata):
    """
    Check the license information of a dataset

    Parameters
    ----------
    scmdata : :obj:`scmdata.ScmRun`
        Dataset of which to check the license information

    Raises
    ------
    NonStandardLicenseError
        The dataset's license is non-standard i.e. is not a
        `Creative Commons Attribution ShareAlike 4.0 International License <https://creativecommons.org/licenses/by-sa/4.0/>`_

    NoLicenseInformationError
        No license information could be found in ``scmdata.metadata``
    """
    licenses = get_license_info(scmdata)

    non_ccas4 = {
        license
        for license in licenses
        if not (
            ("Creative Commons Attribution" in license)
            and ("ShareAlike 4.0 International License" in license)
            and (
                "for terms of use governing CMIP6 output, including citation requirements and proper acknowledgment"
                in license
            )
            and ("NonCommercial" not in license)
        )
    }
    if non_ccas4:
        error_msg = "Non-standard licenses: {}".format(non_ccas4)
        raise NonStandardLicenseError(error_msg)


def get_license_info(scmdata):
    """
    Get the license information from a dataset's metadata.

    Parameters
    ----------
    scmdata : :obj:`scmdata.ScmRun`
        Dataset from which to get the license information

    Raises
    ------
    NoLicenseInformationError
        No license information could be found in ``scmdata.metadata``
    """
    licenses = [v for k, v in scmdata.metadata.items() if "license" in k]

    if not licenses:
        raise NoLicenseInformationError("Metadata found: {}".format(scmdata.metadata))

    return licenses
