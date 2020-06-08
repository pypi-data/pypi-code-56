import numpy as np
import numpy.testing as npt


def test_Pk():
    from ..generator import Pk

    assert Pk(1, alpha=2, fknee=1) == 1
    assert np.all(Pk(np.arange(10), alpha=0, fknee=1) == np.ones(10))


def gen_pkfield():
    from ..generator import gen_pkfield

    np.random.seed(42)
    pkfield = gen_pkfield(npix=256, alpha=0, fknee=1, res=1)

    assert pkfield.shape == (256, 256)
    npt.assert_almost_equal(np.mean(pkfield), 0)
    npt.assert_almost_equal(np.std(pkfield), 1, decimal=3)
