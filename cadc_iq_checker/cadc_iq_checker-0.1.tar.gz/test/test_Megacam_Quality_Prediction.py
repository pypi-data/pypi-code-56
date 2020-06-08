from unittest import TestCase

import numpy
import sompy
from astropy.io import fits

from Megacam_Prediction.Megacam_Quality_Prediction import LDAC, ImageQualityModel


class TestLDAC(TestCase):
    def setUp(self) -> None:
        self.ldac = LDAC('SC_CORR-0216650-008.ldac')

    def test_header(self):
        self.assertIsInstance(self.ldac.header, fits.Header)
        self.assertEquals(self.ldac.header['FITSEXT'], 1)

    def test_data(self):
        self.assertAlmostEqual(self.ldac.data['ELLIPTICITY'][100], 0.0967232, 5)


class TestImageQualityModel(TestCase):
    def setUp(self) -> None:
        self.iqm = ImageQualityModel('SC_CORR-0216650-008.ldac')
        self.map_1d = numpy.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 4., 7.,
                                   10., 35., 40., 32., 0., 0., 0., 0., 0., 1., 0.,
                                   0., 0., 3., 7., 9., 15., 84., 5., 0., 0., 0.,
                                   0., 0., 0., 0., 4., 4., 9., 16., 13., 66., 120.,
                                   55., 0., 0., 0., 0., 3., 0., 0., 0., 2., 5.,
                                   8., 4., 63., 165., 163., 0., 0., 0., 0., 5., 2.,
                                   2., 4., 3., 8., 15., 57., 121., 131., 47., 0., 0.,
                                   0., 0., 0., 9., 8., 3., 14., 14., 30., 59., 72.,
                                   88., 84., 0., 0., 0., 0., 0., 15., 18., 26., 24.,
                                   36., 34., 47., 36., 53., 38., 0., 0., 0., 0., 0.,
                                   0., 0., 4., 13., 17., 21., 34., 28., 21., 47., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 9., 12., 7.,
                                   9., 15., 11., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 16., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                   0., 0., 0., 0., 0.])

    def test_map(self):
        self.assertEqual(numpy.all(self.iqm.map == self.map_1d), True)

    def test_model_input_data(self):
        data = self.iqm.model_input_data
        self.assertEqual(len(self.iqm.model_input_data[0]),
                         self.iqm.som_model.codebook.mapsize[0] * self.iqm.som_model.codebook.mapsize[1])
        self.assertEqual(len(self.iqm.model_input_data[1]),
                         (self.iqm.cutout_dimensions[0]*self.iqm.cutout_dimensions[1]))
        self.assertAlmostEqual(self.iqm.model_input_data[5].sum(), 0.0, 2)
