"""
Usage: md_table.py [OPTIONS]

Options:
  -i, --input PATH            csv file to read
  -fd, --file_delimiter TEXT  csv file delimiter
  -ta, --text_alignment TEXT  alignment of the table text possible values,
                              "left", "right" and "center".This is case
                              insensitive.

  -o, --output TEXT           write markdown table to file
  -om, --output_mode TEXT     output write mode
  --help                      Show this message and exit.

"""
from md_table import *