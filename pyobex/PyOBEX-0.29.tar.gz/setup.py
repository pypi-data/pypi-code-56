#! /usr/bin/env python3

import setuptools

from PyOBEX import __version__

description = "A package implementing aspects of the Object Exchange (OBEX) protocol."

setuptools.setup(
    name         = "PyOBEX",
    description  = description,
    long_description = description,
    author       = "David Boddie",
    author_email = "david@boddie.org.uk",
    url          = "http://www.boddie.org.uk/david/Projects/Python/PyOBEX/",
    version      = __version__,
    license      = "GPL version 3 (or later)",
    platforms    = "Cross-platform",
    packages     = ["PyOBEX"]
    )
