#! python3
# -*- coding: utf-8 -*-

"""A Python interface to xmlsq <https://www.cryptosys.net/xmlsq/>."""

# $Id: xmlsq.py $
# $Date: 2020-06-04 20:57:00 $

# ************************** LICENSE *****************************************
# Copyright (C) 2020 David Ireland, DI Management Services Pty Limited.
# <www.di-mgt.com.au> <www.cryptosys.net>
# This code is provided 'as-is' without any express or implied warranty.
# Free license is hereby granted to use this code as part of an application
# provided this license notice is left intact. You are *not* licensed to
# share any of this code in any form of mass distribution, including, but not
# limited to, reposting on other web sites or in any source code repository.
# ****************************************************************************

# Requires `xmlsq` to be installed on your system,
# available from <https://www.cryptosys.net/xmlsq/>.

from ctypes import windll, create_string_buffer, c_char_p, c_int

__version__ = "0.9.0"

# OUR EXPORTED CLASSES
__all__ = (
    'Gen',
    'Error',
    'Opts',
    'get_text',
    'full_query',
    'count',
)

# Our global DLL object
_didll = windll.diXmlsq

# PROTOTYPES (derived from diXmlsq.h)
# If wrong argument type is passed, these will raise an `ArgumentError` exception
#     ArgumentError: argument 1: <type 'exceptions.TypeError'>: wrong type
_didll.XMLSQ_Gen_Version.argtypes = []
_didll.XMLSQ_Gen_CompileTime.argtypes = [c_char_p, c_int]
_didll.XMLSQ_Gen_ModuleName.argtypes = [c_char_p, c_int, c_int]
_didll.XMLSQ_Gen_Platform.argtypes = [c_char_p, c_int]
_didll.XMLSQ_GetText.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_didll.XMLSQ_FullQuery.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_didll.XMLSQ_Count.argtypes = [c_char_p, c_char_p, c_int]


def _isanint(v):
    try:
        v = int(v)
    except:
        pass
    return isinstance(v, int)


class Error(Exception):
    """Raised when a call to a core library function returns an error, e.g. unable to execute query,
    or some obviously wrong parameter is detected."""

    # Google Python Style Guide: "The base exception for a module should be called Error."

    def __init__(self, value):
        """."""
        self.value = value

    def __str__(self):
        """Behave differently if value is an integer or not."""
        if _isanint(self.value):
            n = int(self.value)
            s1 = "ERROR CODE %d" % n
        else:
            # Error message is passed complete
            s1 = "%s" % self.value
        return "%s" % s1


class Opts:
    """Option flags."""
    DEFAULT = 0  #: Use default options.
    ASCIIFY = 0x1000  #: Asciify the output as XML character references [default=UTF-8-encoded].
    RAW = 0x2000  #: Output nodeset in raw format [default=prettify with tabs and newlines].
    TRIM = 0x4000  #: Trim leading and trailing whitespace (and collapse whitespace for an attribute value).


def get_text(xmlfile, query, opts=Opts.DEFAULT):
    """Extract text from the first matching XML node.

    Args:
        xmlfile (str): Name of input XML file.
        query (str): XPath 1.0 expression to select a node. This must evaluate to a node or node set.
        opts (Opts): Option flags (add with '|' operator).

    Returns:
        str: String containing the extracted text.

    Remarks:
        * If query evaluates to a single element with content, then the text content will be output.
        * If query evaluates to an attribute, then the attribute value will be output.
        * If query evaluates to a node set, then the content of the first matching node will be returned as a string, including any markup.
        * If no matching node is found, an empty string ``""`` is returned.
        * No distinction is made between a match on an empty element and no match at all.
          Use :func:`xmlsq.count` to differentiate between a match on an empty element (returns > 0) and no match at all (returns 0).

    """
    n = _didll.XMLSQ_GetText(None, 0, xmlfile.encode(), query.encode(), opts)
    iserror = False
    if n < 0:
        # There was an error; error message will be output to buf
        n = -n
        iserror = True
    buf = create_string_buffer(n + 1)
    n = _didll.XMLSQ_GetText(buf, n, xmlfile.encode(), query.encode(), opts)
    if iserror:
        raise Error(buf.value.decode())
    return buf.value.decode()


def full_query(xmlfile, query, opts=Opts.DEFAULT):
    """Perform a full XPath query on the XML input outputting the result as a string.

    Args:
        xmlfile (str): Name of input XML file.
        query (str): XPath 1.0 expression.
        opts (Opts): Option flags (add with '|' operator).

    Returns:
        str: The result of the full XPath 1.0 query as a string.

    Remarks:
        ``query`` may be any valid XPath 1.0 expression. The result is always output as a string.
        So, for example, the number 1.5 will be output as the string "1.500000".

    """
    n = _didll.XMLSQ_FullQuery(None, 0, xmlfile.encode(), query.encode(), opts)
    iserror = False
    if n < 0:
        # There was an error; error message will be output to buf
        n = -n
        iserror = True
    buf = create_string_buffer(n + 1)
    n = _didll.XMLSQ_FullQuery(buf, n, xmlfile.encode(), query.encode(), opts)
    if iserror:
        raise Error(buf.value.decode())
    return buf.value.decode()


def count(xmlfile, query):
    """Compute the count for the XPath query.

    Args:
        xmlfile (str): Name of input XML file.
        query (str): XPath 1.0 expression. This must evaluate to a node or node set.

    Returns:
        int: The integer value of ``count(query)``.

    """
    n = _didll.XMLSQ_Count(xmlfile.encode(), query.encode(), 0)
    if n < 0:
        raise Error(n)
    return n


class Gen:
    """General diagnostic info about the core library DLL."""

    @staticmethod
    def version():
        """Return the release version of the core library DLL as an integer value."""
        return _didll.XMLSQ_Gen_Version()

    @staticmethod
    def compile_time():
        """Return date and time the core library DLL was last compiled."""
        nchars = _didll.XMLSQ_Gen_CompileTime(None, 0)
        if nchars < 0: raise Error(nchars)
        buf = create_string_buffer(nchars + 1)
        nchars = _didll.XMLSQ_Gen_CompileTime(buf, nchars)
        return buf.value.decode()

    @staticmethod
    def module_name():
        """Return full path name of the current process's core library DLL."""
        nchars = _didll.XMLSQ_Gen_ModuleName(None, 0, 0)
        if nchars < 0: raise Error(nchars)
        buf = create_string_buffer(nchars + 1)
        nchars = _didll.XMLSQ_Gen_ModuleName(buf, nchars, 0)
        return buf.value.decode()

    @staticmethod
    def core_platform():
        """Return the platform for which the core library DLL was compiled: ``Win32`` or ``Win64``."""
        nchars = _didll.XMLSQ_Gen_Platform(None, 0)
        if nchars < 0: raise Error(nchars)
        buf = create_string_buffer(nchars + 1)
        nchars = _didll.XMLSQ_Gen_Platform(buf, nchars)
        return buf.value.decode()
