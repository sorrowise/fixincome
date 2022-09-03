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
    assert almost_equal(ut.effective_annual_rate(0.03, 1, "q"), 0.1255)
    assert almost_equal(ut.effective_annual_rate(0.005, 1, "m"), 0.06168)
    assert almost_equal(ut.effective_annual_rate(0.06/365, 1), 0.06183)


def test_discount_rate():
    assert almost_equal(ut.discount_rate(700, 100, 10), 0.07073)


def test_holding_period_yield():
    assert almost_equal(ut.holding_period_yield(100000, 98500), 0.015228)


def test_hpy_to_ear():
    assert almost_equal(ut.hpy_to_ear(100000, 98500, 120), 0.047042)


def test_npv():
    ds = ['20060101', '20070303', '20070704', '20081012', '20091225']
    cf = [-1000, 100, 195, 350, 800]
    assert almost_equal(ut.xnpv(0.12, ds, cf), 16.80083062214726)


def test_xirr():
    dates = ['20060101', '20060303', '20060704', '20061012', '20061225']
    cashflows = [-1000, 150, 100, 50, 1000]
    assert almost_equal(ut.xirr(dates, cashflows), 0.37188269789)


def test_macaulay_duration():
    assert almost_equal(ut.macaulay_duration(
        1000, 0.05, 1000, 0.05, 4), 3.7232480293704775)


def test_modified_duration():
    assert almost_equal(ut.modified_duration(
        1000, 0.05, 1000, 0.05, 4), 3.7232480293/1.05)


def test_pvbp():
    assert almost_equal(ut.pvbp(101.39, 6, 20), 0.1169594)


def test_convexity():
    assert almost_equal(ut.convexity(1000, 50, 4, 1000), 16.473834)
