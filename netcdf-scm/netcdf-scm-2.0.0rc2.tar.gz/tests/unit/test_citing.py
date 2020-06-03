import re

import pytest
from scmdata.run import ScmRun

from netcdf_scm.citing import check_license, get_license_info
from netcdf_scm.errors import NoLicenseInformationError, NonStandardLicenseError


@pytest.fixture
def test_scmdata():
    out = ScmRun(
        data=[1, 2, 3],
        index=[10, 20, 30],
        columns={
            "model": "junk",
            "scenario": "junk",
            "variable": "junk",
            "region": "junk",
            "unit": "junk",
        },
    )

    out.metadata = {"junk key": "junk value"}

    return out


def test_get_license_info_single_key(test_scmdata):
    tlicense_info = "license information here"
    test_scmdata.metadata["license"] = tlicense_info

    res = get_license_info(test_scmdata)

    assert res == [tlicense_info]


def test_get_license_info_two_keys(test_scmdata):
    tlicense_info_1 = "license information here"
    tlicense_info_2 = "license information here"
    test_scmdata.metadata["(child) license"] = tlicense_info_1
    test_scmdata.metadata["(normalisation) license"] = tlicense_info_2

    res = get_license_info(test_scmdata)

    assert set(res) == {tlicense_info_1, tlicense_info_2}


def test_get_license_info_missing_license(test_scmdata):
    error_msg = re.escape("Metadata found: {}".format(test_scmdata.metadata))
    with pytest.raises(NoLicenseInformationError, match=error_msg):
        get_license_info(test_scmdata)


def test_check_license_missing_license(test_scmdata):
    error_msg = re.escape("Metadata found: {}".format(test_scmdata.metadata))
    with pytest.raises(NoLicenseInformationError, match=error_msg):
        check_license(test_scmdata)


VALID_LICENSE_TXT = (
    "Creative Commons Attribution ShareAlike 4.0 International License. "
    "See website for terms of use governing CMIP6 output, including "
    "citation requirements and proper acknowledgment"
)


@pytest.mark.parametrize(
    "txt,exp_error",
    (
        (VALID_LICENSE_TXT, False),
        (
            "Creative Commons Attribution[]-ShareAlike 4.0 International License. "
            "See website for terms of use governing CMIP6 output, including "
            "citation requirements and proper acknowledgment",
            False,
        ),
        (
            "Creative Commons Attribution[]-ShareAlike 4.0 Non-Commercial License. "
            "See website for terms of use governing CMIP6 output, including "
            "citation requirements and proper acknowledgment",
            True,
        ),
        ("Nonsense", True),
    ),
)
def test_check_license_single_key(test_scmdata, txt, exp_error):
    test_scmdata.metadata["license"] = txt
    if exp_error:
        error_msg = re.escape("Non-standard licenses: {}".format({txt}))
        with pytest.raises(NonStandardLicenseError, match=error_msg):
            check_license(test_scmdata)

    else:
        check_license(test_scmdata)


@pytest.mark.parametrize(
    "txt_1,txt_2,exp_error_1,exp_error_2",
    (
        (VALID_LICENSE_TXT, VALID_LICENSE_TXT, False, False),
        ("Nonsense", VALID_LICENSE_TXT, True, False),
        (
            VALID_LICENSE_TXT,
            VALID_LICENSE_TXT.replace("International", "NonCommercial International"),
            False,
            True,
        ),
        (
            VALID_LICENSE_TXT,
            VALID_LICENSE_TXT.replace("Attribution", "Attribution-NonCommercial"),
            False,
            True,
        ),
        ("Nonsense", "More nonsense", True, True),
    ),
)
def test_check_license_multiple_keys(
    test_scmdata, txt_1, txt_2, exp_error_1, exp_error_2
):
    test_scmdata.metadata["(child) license"] = txt_1
    test_scmdata.metadata["(normalisation) license"] = txt_2
    if exp_error_1 or exp_error_2:
        if exp_error_1 and exp_error_2:
            error_msg = re.escape("Non-standard licenses: {}".format({txt_1, txt_2}))
        elif exp_error_1:
            error_msg = re.escape("Non-standard licenses: {}".format({txt_1}))
        else:
            error_msg = re.escape("Non-standard licenses: {}".format({txt_2}))

        with pytest.raises(NonStandardLicenseError, match=error_msg):
            check_license(test_scmdata)

    else:
        check_license(test_scmdata)
