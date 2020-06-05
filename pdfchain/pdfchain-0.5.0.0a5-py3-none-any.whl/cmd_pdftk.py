# Copyright (C) Martin Singer <martin.singer@web.de>
#
# This file is part of PDF Chain.
#
# PDF Chain is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PDF Chain is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PDF Chain.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Martin Singer


"""
@brief Command Strings.
@details
    Contains the PDF Toolkit command and options as constant strings.
    This module contains constant strings with the escape sequences
    for various colors and styles in the terminal.

@see <https://www.pdflabs.com/docs/pdftk-man-page/>
@see <https://www.pdflabs.com/docs/pdftk-cli-examples/>

@see <https://en.wikipedia.org/wiki/ANSI_escape_code#3/4_bit>
"""


def set_command(path):
    """
    @brief Updating the "pdftk" dictionary entry "command".
    @see preferences._export_values()
    @param path Path of the pdftk command
    """
    pdftk["command"] = path


pdftk = {
        """
        @brief PDFtk command parameter dictionary.
        """

        # Main Command
        "command": "pdftk",  # Default value, becomes overridden

        # General Sub Commands
        "output": "output",


        # Section: Concatenate & Shuffle
        ## Specific Sub Commands
        "concatenate": "cat",
        "shuffle":     "shuffle",

        ## Specific Parameters
        "docid_keep":       "",
        "docid_create_new": "",
        "docid_keep_first": "keep_first_id",
        "docid_keep_final": "keep_final_id",

        "rot_north": "north",  #   0 deg
        "rot_east":  "east",   #  90 deg
        "rot_south": "south",  # 180 deg
        "rot_west":  "west",   # 270 deg

        "filter_all":  "",
        "filter_even": "even",
        "filter_odd":  "odd",

        "password_input": "input_pw",


        # Section: Attachments
        ## Specific Sub Command
        "attach": "attach_files",

        ## Specific Parameter
        "to_page": "to_page",


        # Section: Watermark / Stamp
        ## Specific Sub Commands
        "watermark":       "background",
        "watermark_multi": "multibackground",
        "stamp":           "stamp",
        "stamp_multi":     "multistamp",


        # Section: Burst
        ## Specific Sub Commands
        "burst": "burst",

        ## Specific Parameters: Template
        "template":  "%0",
        "extension": ".pdf",

        "base_oct": "o",
        "base_dec": "d",
        "base_hex": "h",


        # Section: Tools
        ## Specific Sub Commands
        "unpack_files":          "unpack_files",

        "compress":              "compress",
        "uncompress":            "uncompress",

        "dump_data_annots":      "dump_data_annots",
        "dump_data_fields":      "dump_data_fields",
        "dump_data_fields_utf8": "dump_data_fields_utf8",
        "dump_data":             "dump_data",
        "dump_data_utf8":        "dump_data_utf8",

        "update_info":           "update_info",
        "update_info_utf8":      "update_info_utf8",
        "generate_fdf":          "generate_fdf",

        "fill_form":             "fill_form",
        "flatten":               "flatten",
        "need_appearances":      "need_appearances",
        "drop_xfa":              "drop_xfa",


        # Section: Permissions
        ## Specific Sub Commands
        "allow":     "allow",
        "allow_all": "AllFeatures",

        ## Specific Parameters: Restrictions
        "printing":           "Printing",
        "printing_degraded":  "DegradedPrinting",
        "modify_contents":    "ModifyContents",
        "assembly":           "Assembly",
        "copy_contents":      "CopyContents",
        "screenreaders":      "ScreenReaders",
        "modify_annotations": "ModifyAnnotations",
        "fill_in":            "FillIn",

        ## Specific Sub Commands: Passwords
        "password_owner": "owner_pw",
        "password_user":  "user_pw",

        ## Specific Sub Commands: Encryptions
        # "encrypt_none":   "",
        "encrypt_40bit":  "encrypt_40bit",
        "encrypt_128bit": "encrypt_128bit",
        }
