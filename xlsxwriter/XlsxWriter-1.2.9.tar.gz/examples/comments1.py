###############################################################################
#
# An example of writing cell comments to a worksheet using Python and
# XlsxWriter.
#
# For more advanced comment options see comments2.py.
#
# Copyright 2013-2020, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('comments1.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Hello')
worksheet.write_comment('A1', 'This is a comment')

workbook.close()
