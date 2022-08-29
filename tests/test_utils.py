from dis import dis
from fixincome import utils as ut


def almost_equal(result, expect, precision: float = 1e-4) -> bool:
    return abs(result-expect) <= precision


def test_geometric_series_sum():
    assert almost_equal(ut.geometric_series_sum(
        10, 2.3, 20), 132011979.33342900)


def test_future_value_factor():
    assert almost_equal(ut.future_value_factor(0.013, 12.5), 13.47823117)


def test_present_value_factor():
    assert almost_equal(ut.present_value_factor(0.012, 20.7), 18.23315997)


def test_present_value():
    assert almost_equal(ut.present_value(100, 0.13, 10, 1000), 837.21269572)


def test_net_present_value():
    assert almost_equal(ut.net_present_value(
        0.1, [100, 200, 300, 400, 500]), 1065.258831)
    assert almost_equal(ut.net_present_value(0.12, [1.6, 2.4, 2.8], 5), 0.3348)


def test_internal_rate():
    assert almost_equal(ut.internal_rate(
        [100, 200, 300, 400, 500], 1000), 0.12005762)
    assert almost_equal(ut.internal_rate([1.6, 2.4, 2.8], 5), 0.1552)


def test_future_value():
    assert almost_equal(ut.future_value(0.01, 12, 1000), 12682.50301320)
    assert almost_equal(ut.future_value(0.07, 15, 150), 3769.3533)


def test_effective_annual_rate():
    assert almost_equal(ut.effective_annual_rate(0.03, 4), 0.1255)
    assert almost_equal(ut.effective_annual_rate(0.005, 12), 0.06168)


def test_discount_rate():
    assert almost_equal(ut.discount_rate(700, 100, 10), 0.07073)


def test_holding_period_yield():
    assert almost_equal(ut.holding_period_yield(100000, 98500), 0.015228)
