#!/usr/bin/env python

"""
Conduct joint recurrence quantification analysis.

Input data representation: Column store
Recurrence matrix materialisation: Yes
Similarity value representation: Bit
Intermediate results recycling: No
"""

import numpy as np

from pyrqa.utils import SettableSettings
from pyrqa.operators.create_matrix.radius.column_materialisation_bit import create_matrix
from pyrqa.operators.join_matrices.materialisation_bit import join_matrices
from pyrqa.operators.detect_diagonal_lines.materialisation_bit import detect_diagonal_lines
from pyrqa.operators.detect_vertical_lines.materialisation_bit_no_recycling import detect_vertical_lines
from pyrqa.runtimes import FlavourRuntimesMultipleOperators

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class ColumnMaterialisationBitNoRecycling(SettableSettings):
    """
    See module description regarding computational properties.

    :ivar opencl: OpenCL environment.
    :ivar device: OpenCL device.
    :ivar data_type: Data type to represent the similarity values.
    :ivar optimisations_enabled: Are the default OpenCL compiler optimisations enabled?
    :ivar loop_unroll: Loop unrolling factor.
    :ivar program: OpenCL program.
    :ivar program_created: Has the OpenCL program already been created?
    :ivar kernels: OpenCL kernels.
    :ivar kernels_created: Have the OpenCL kernels already been created?
    """
    def __init__(self,
                 settings,
                 opencl,
                 device,
                 **kwargs):
        """
        :param settings: Settings.
        :param opencl: OpenCL environment.
        :param device: OpenCL device.
        :param kwargs: Keyword arguments.
        """
        SettableSettings.__init__(self,
                                  settings)

        self.opencl = opencl
        self.device = device

        self.data_type = kwargs['data_type'] if 'data_type' in list(kwargs.keys()) else np.uint32
        self.optimisations_enabled = kwargs['optimisations_enabled'] if 'optimisations_enabled' in list(kwargs.keys()) else False
        self.loop_unroll = kwargs['loop_unroll'] if 'loop_unroll' in list(kwargs.keys()) else 1

        self.program = None
        self.program_created = False

        self.kernels = {}
        self.kernels_created = False

        self.clear_buffer_kernel_name = self.settings.clear_buffer_kernel_name(self.data_type)
        self.create_matrix_kernel_name_1 = self.settings.settings_1.create_matrix_kernel_name
        self.create_matrix_kernel_name_2 = self.settings.settings_2.create_matrix_kernel_name
        self.join_matrices_kernel_name = self.settings.join_matrices_operator_name
        self.detect_vertical_lines_kernel_name = self.settings.detect_vertical_lines_operator_name
        self.detect_diagonal_lines_kernel_name = self.settings.detect_diagonal_lines_operator_name

        self.__initialize()

    def __initialize(self):
        """
        Initialization of the variant.
        """
        if not self.program_created:
            self.program = self.opencl.create_program(self.device,
                                                      (create_matrix,
                                                       join_matrices,
                                                       detect_vertical_lines,
                                                       detect_diagonal_lines),
                                                      self.settings.kernels_sub_dir,
                                                      self.settings.dtype,
                                                      optimisations_enabled=self.optimisations_enabled,
                                                      loop_unroll=self.loop_unroll)

            self.program_created = True

        if not self.kernels_created:
            self.kernels = self.opencl.create_kernels(self.program,
                                                      (self.clear_buffer_kernel_name,
                                                       self.create_matrix_kernel_name_1,
                                                       self.create_matrix_kernel_name_2,
                                                       self.join_matrices_kernel_name,
                                                       self.detect_vertical_lines_kernel_name,
                                                       self.detect_diagonal_lines_kernel_name))

            self.kernels_created = True

    def process_sub_matrix(self,
                           sub_matrix):
        """
        Processing of a single sub matrix.

        :param sub_matrix: Sub matrix.
        :return: Runtimes for processing the sub matrix.
        """
        # Create variant runtimes
        variant_runtimes = FlavourRuntimesMultipleOperators()

        # Create first matrix
        sub_matrix_1_buffer, \
            create_matrix_1_runtimes = create_matrix(self.settings.settings_1,
                                                     self.data_type,
                                                     sub_matrix,
                                                     self.device,
                                                     self.opencl.contexts[self.device],
                                                     self.opencl.command_queues[self.device],
                                                     (self.kernels[self.clear_buffer_kernel_name],
                                                      self.kernels[self.create_matrix_kernel_name_1],),
                                                     return_sub_matrix_data=False)

        variant_runtimes.create_matrix_runtimes = create_matrix_1_runtimes

        # Create second matrix
        sub_matrix_2_buffer, \
            create_matrix_2_runtimes = create_matrix(self.settings.settings_2,
                                                     self.data_type,
                                                     sub_matrix,
                                                     self.device,
                                                     self.opencl.contexts[self.device],
                                                     self.opencl.command_queues[self.device],
                                                     (self.kernels[self.clear_buffer_kernel_name],
                                                      self.kernels[self.create_matrix_kernel_name_2],),
                                                     return_sub_matrix_data=False)

        variant_runtimes.create_matrix_runtimes += create_matrix_2_runtimes

        # Join first and second matrix
        joined_sub_matrix_buffer, \
            join_matrices_runtimes = join_matrices(self.data_type,
                                                   sub_matrix,
                                                   sub_matrix_1_buffer,
                                                   sub_matrix_2_buffer,
                                                   self.device,
                                                   self.opencl.contexts[self.device],
                                                   self.opencl.command_queues[self.device],
                                                   (self.kernels[self.clear_buffer_kernel_name],
                                                    self.kernels[self.join_matrices_kernel_name],),
                                                   return_sub_matrix_data=False)

        variant_runtimes.create_matrix_runtimes += join_matrices_runtimes

        # Detect vertical lines
        detect_vertical_lines_runtimes = detect_vertical_lines(self.data_type,
                                                               sub_matrix,
                                                               joined_sub_matrix_buffer,
                                                               self.device,
                                                               self.opencl.contexts[self.device],
                                                               self.opencl.command_queues[self.device],
                                                               (self.kernels[self.detect_vertical_lines_kernel_name],))

        variant_runtimes.detect_vertical_lines_runtimes = detect_vertical_lines_runtimes

        # Detect diagonal lines
        detect_diagonal_lines_runtimes = detect_diagonal_lines(self.settings.is_matrix_symmetric,
                                                               self.settings.theiler_corrector,
                                                               self.data_type,
                                                               sub_matrix,
                                                               joined_sub_matrix_buffer,
                                                               self.device,
                                                               self.opencl.contexts[self.device],
                                                               self.opencl.command_queues[self.device],
                                                               (self.kernels[self.detect_diagonal_lines_kernel_name],))

        variant_runtimes.detect_diagonal_lines_runtimes = detect_diagonal_lines_runtimes

        return variant_runtimes
