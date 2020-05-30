"""
This module provides a JPEG 2000 file reader.
"""
import collections
from xml.etree import cElementTree as ET


from sunpy.io.header import FileHeader
from sunpy.util.xml import xml_to_dict

__all__ = ['read', 'get_header', 'write']

HDPair = collections.namedtuple('HDPair', ['data', 'header'])


def read(filepath, **kwargs):
    """
    Reads a JPEG2000 file.

    Parameters
    ----------
    filepath : `str`
        The file to be read.

    Returns
    -------
    pairs : `list`
        A list of (data, header) tuples.
    """
    # Put import here to speed up sunpy.io import time
    from glymur import Jp2k
    header = get_header(filepath)

    data = Jp2k(filepath).read()[::-1]

    return [HDPair(data, header[0])]


def get_header(filepath):
    """
    Reads the header from the file.

    Parameters
    ----------
    filepath : `str`
        The file to be read.

    Returns
    -------
    headers : list
        A list of headers read from the file.
    """
    # Put import here to speed up sunpy.io import time
    from glymur import Jp2k
    jp2 = Jp2k(filepath)
    xml_box = [box for box in jp2.box if box.box_id == 'xml ']
    xmlstring = ET.tostring(xml_box[0].xml.find('fits'))
    pydict = xml_to_dict(xmlstring)["fits"]

    # Fix types
    for k, v in pydict.items():
        if v.isdigit():
            pydict[k] = int(v)
        elif _is_float(v):
            pydict[k] = float(v)

    # Remove newlines from comment
    if 'comment' in pydict:
        pydict['comment'] = pydict['comment'].replace("\n", "")

    # Is this file a Helioviewer Project JPEG2000 file?
    pydict['helioviewer'] = xml_box[0].xml.find('helioviewer') is not None

    return [FileHeader(pydict)]


def write(fname, data, header):
    """
    Place holder for required file writer.
    """
    raise NotImplementedError("No jp2 writer is implemented.")


def _is_float(s):
    """
    Check to see if a string value is a valid float.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
