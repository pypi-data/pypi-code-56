#! python3
# -*- coding: utf-8 -*-

"""Some tests for `xmlsq.py` the Python interface to xmlsq."""

# test_xmlsq.py: version 0.9.0
# $Date: 2020-06-04 21:37:00 $

# ************************** LICENSE *****************************************
# Copyright (C) 2020 David Ireland, DI Management Services Pty Limited.
# <http://www.di-mgt.com.au/contact/> <www.cryptosys.net>
# The code in this module is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
# ****************************************************************************

import xmlsq


def main():
    print("xmlsq.py version =", xmlsq.__version__)
    print("DLL Version = %05d" % xmlsq.Gen.version())
    print("DLL Compile Time =", xmlsq.Gen.compile_time())
    print("Module =", xmlsq.Gen.module_name())
    print("Platform =", xmlsq.Gen.core_platform())

    xml = r"<a><b foo='baz'>hello world</b></a>"
    print("XML:", xml)
    print(xmlsq.get_text(xml, "//b"))  # hello world
    print(xmlsq.full_query(xml, "//b"))  # <b foo="baz">hello world</b>\n
    print(xmlsq.full_query(xml, "//b", xmlsq.Opts.RAW))  # <b foo="baz">hello world</b>
    print(xmlsq.get_text(xml, "//b/@foo"))  # baz
    print(xmlsq.get_text(xml, "/"))
    print(xmlsq.get_text(xml, "/", xmlsq.Opts.RAW))
    print("count =", xmlsq.count(xml, "//b"))  # count = 1
    xml = r"<a><b foo='ratón'>México</b></a>"
    print("XML:", xml)
    print(xmlsq.get_text(xml, "//b"))  # México
    print(xmlsq.full_query(xml, "//b", xmlsq.Opts.RAW))  # <b foo="ratón">México</b>
    print(xmlsq.full_query(xml, "//b", xmlsq.Opts.RAW | xmlsq.Opts.ASCIIFY))  # <b foo="rat&#xF3;n">M&#xE9;xico</b>
    print(xmlsq.get_text(xml, "//b/@foo"))  # ratón
    print(xmlsq.full_query(xml, "boolean(count(//NotThere))"))  # false
    print(xmlsq.full_query(xml, "2+3.5"))  # 5.500000

    # Trim leading and trailing whitespace
    xml = r"<a foo = '   val   de  ri '>  hello   world </a>"
    print("XML:", xml)
    print("'" + xmlsq.get_text(xml, "/a") + "'")  # '  hello   world '
    print("'" + xmlsq.get_text(xml, "/a", xmlsq.Opts.TRIM) + "'")  # 'hello   world'
    print("'" + xmlsq.get_text(xml, "/a/@foo") + "'")  # '   val   de  ri '
    # Attribute values are normalized as well as trimmed
    print("'" + xmlsq.get_text(xml, "/a/@foo", xmlsq.Opts.TRIM) + "'")  # 'val de ri'

    print("ALL DONE.")


if __name__ == "__main__":
    main()
