import pytest
import bandparams
import pathlib

testdata = pathlib.Path(__file__).parent.resolve().joinpath('testdata')

def test():
    r = bandparams.bandparams(bandparams.read_spc(testdata / 'spc1.dat'))
    assert r['barycenter'] == pytest.approx(2.0518, 1e-4)
    assert r['max_pos'] == pytest.approx(2.0305, 1e-4)
    assert r['fwhm'] == pytest.approx(0.2695, 1e-4)
    assert r['max_val'] == pytest.approx(1.4663e+04, 1)
