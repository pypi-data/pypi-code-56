"""
parse_internal_continuous.py
====================================
Module to parse input files containing internally calibrated continuous spectra.
"""

from .parse_generic import *

# Columns that contain arrays (as strings)
array_columns = [
    'bp_coefficients',
    'bp_coefficient_errors',
    'rp_coefficients',
    'rp_coefficient_errors']
# Pairs of the form (matrix_size (N), values_to_put_in_matrix) for columns
# that contain matrices as strings
to_matrix_columns = [('bp_num_of_parameters', 'bp_coefficient_correlations'),
                     ('rp_num_of_parameters', 'rp_coefficient_correlations')]


class InternalContinuousParser(GenericParser):
    """
    Parser for internally calibrated continuous spectra.
    """

    def _parse_csv(self, csv_file):
        """
        Parse the input CSV file and store the result in a pandas DataFrame if it
        contains internally calibrated continuous spectra.

        Args:
            csv_file (str): Path to a CSV file.

        Returns:
            DataFrame: Pandas DataFrame representing the CSV file.
        """
        return super()._parse_csv(
            csv_file,
            array_columns=array_columns,
            matrix_columns=to_matrix_columns)
