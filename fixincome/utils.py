"""This module is a collection of helper functions.
"""

from datetime import datetime
from typing import List

import numpy as np
from scipy.optimize import fsolve


def geometric_series_sum(a1: float, q: float, n: float) -> float:
    """Calculate the sum of a geometric sequence

    Args:
        a1 (float): first item
        q (float): common ratio
        n (float): number of items

    Returns:
        float: sum of geometric numbers
    """
    return a1*(1-q**n)/(1-q)


def future_value_factor(rate: float, nper: float, time: int = 0) -> float:
    """Calculate the annuity future value factor

    Args:
        rate (float): rate of return
        nper (float): Total annuity investment period
        time(int,optional): Whether the payment time point is at the beginning or the end of the period,
                if 0 means the end of the period, 1 means the beginning of the period, the default is 0

    Returns:
        float: annuity future value factor
    """
    res = geometric_series_sum(1, 1+rate, nper)
    return res if time == 0 else res*(1+rate)


def present_value_factor(rate: float, nper: float, time: int = 0) -> float:
    """Calculate the annuity present value factor

    Args:
        rate (float): rate of return
        nper (float): Total annuity investment period
        time(int,optional): Whether the payment time point is at the beginning or the end of the period,
                if 0 means the end of the period, 1 means the beginning of the period, the default is 0

    Returns:
        float: annuity present value factor
    """
    res = geometric_series_sum(1/(1+rate), 1/(1+rate), nper)
    return res if time == 0 else res*(1+rate)


def present_value(pmt: float, rate: float, term: int, fv: float = 0, time: int = 0) -> float:
    """Calculate the present value of a series of cash flows

    Args:
        pmt (float): Cash flow per period, which remains the same throughout the investment period
        rate (float): Discount rate, which remains the same throughout the investment period
        term (int): Total period of cash flow   
        fv (float,optional): future value of cash flow
        time(int,optional): Whether the payment time point is at the beginning or the end of the period,
                 if 0 means the end of the period, 1 means the beginning of the period, the default is 0

    Returns:
        float: present value of cash flow
    """
    pv = pmt*present_value_factor(rate, term, time) + fv/pow(1+rate, term)
    return pv


def net_present_value(rate: float, cashflows: List[float], investment: float = 0) -> float:
    """Calculates the net present value of a series of cash flows, 
        with the initial investment expressed as a negative number

    Args:
        rate (float): Discount rate
        cashflow (List[float]):  Cash flow per period

    Returns:
        float: net present value
    """
    return sum(c/pow(1+rate, t+1) for t, c in enumerate(cashflows)) - investment


def internal_rate(cashflows: List[float], initial_investment: float, guess: float = 0.1) -> float:
    """Calculate the internal rate of return on cash flow

    Args:
        cashflows (List[float]): a series of cash flows
        initial_investment (float): initial investment

    Returns:
        float: Internal Rate of Return
    """
    def func(r): return sum(c/pow(1+r, 1+t)
                            for t, c in enumerate(cashflows)) - initial_investment
    return fsolve(func, guess)[0]


def future_value(rate: float, term: int, pmt: float, pv: float = 0.0, time: int = 0) -> float:
    """Calculate the future value of a series of investments

    Args:
        rate (float): return on investment
        term (int): investment period
        pmt (float): Amount of investment in each period
        pv (float, optional): Initial investment amount. Defaults to 0.0.
        time(int,optional): Whether the payment time point is at the beginning or 
                            the end of the period, if 0 means the end of the period, 
                            1 means the beginning of the period, the default is 0

    Returns:
        float: future value of investment
    """
    fv = pmt*future_value_factor(rate, term, time) + pv*pow(1+rate, term)
    return fv


def effective_annual_rate(rate: float, t: float = 1, time_unit: str = "d") -> float:
    """Convert holding period yield to effective annual rate

    Args:
        rate (float): Yield during holding period
        t (float): holding period
        time_unit(str): time unit, can be days("d"), months("m") and quarters("q"), the default is days

    Returns:
        float: effective annual rate
    """
    tu = {"d": 365, "m": 12, "q": 4}
    return pow(1+rate, tu[time_unit]/t) - 1


def discount_rate(pv: float, pmt: float, nper: int, fv: float = 0, guess: float = 0.1) -> float:
    """Calculate the discount rate for an annuity

    Args:
        pv (float): present value of the annuity
        pmt (float): Annuity Payments Each Period
        nper (int): Number of annuity payments
        guess (float, optional): the given interest rate guess. Defaults to 0.1.

    Returns:
        float: discount rate
    """
    def func(r): return present_value(pmt, r, nper, fv) - pv
    return fsolve(func, guess)[0]


def holding_period_yield(p1: float, p0: float, d: float = 0) -> float:
    """Calculate the holding period return

    Args:
        p1 (float): price received for instrument at maturity
        p0 (float): initial price of instrument
        d (float): interest payment

    Returns:
        float: holding period yield(HPY)
    """
    return (p1 + d - p0) / p0


def hpy_to_ear(p1: float, p0: float, t: float, d: float = 0, time_unit: str = "d") -> float:
    """Convert holding period yield to effective annual rate

    Args:
        p1 (float): price received for instrument at maturity
        p0 (float): initial price of instrument
        t (int): holding period
        d (float): interest payment
        time_unit(str): time unit, can be days("d"), months("m") and quarters("q"), the default is days

    Returns:
        float: effective annual rate of return
    """
    hpy = (p1 + d - p0) / p0
    return effective_annual_rate(hpy, t, time_unit)


def xnpv(rate: float, dates: List[str], cashflows: List[float]) -> float:
    """Returns the net present value for the cash flow plan

    Args:
        rate(float): annual discount rate
        dates (List[str]): The payment date of each cash flow, input as a string in the form of "20060101"
        cashflows (List[float]): Cash flow for each payment date

    Returns:
        float: net present value
    """
    dates = [datetime.strptime(d, "%Y%m%d") for d in dates]
    delta = [(d - dates[0]).days for d in dates[1:]]
    r = pow(1+rate, 1/365) - 1
    npv = sum(c/pow(1+r, d)
              for c, d in zip(cashflows[1:], delta)) + cashflows[0]
    return npv


def xirr(dates: List[str], cashflows: List[float]) -> float:
    """Returns the internal rate of return for the cash flow plan

    Args:
        dates (List[str]): The payment date of each cash flow, input as a string in the form of "20060101"
        cashflows (List[float]): Cash flow for each payment date

    Returns:
        float: internal rate of return
    """
    return fsolve(lambda r: xnpv(r, dates, cashflows), 0)[0]


def macaulay_duration(price: float, ytm: float, par_value: float, par_rate: float, term: int) -> float:
    """Calculate Macaulay Duration

       Macaulay duration is the weighted average of the time to receive the cash flows from a bond. 
       It is measured in units of years. Macaulay duration tells the weighted average time that a bond 
       needs to be held so that the total present value of the cash flows received is equal to the current
       market price paid for the bond. It is often used in bond immunization strategies.

    Args:
        price (float): the current price of the bond
        ytm (float): bond yield to maturity
        par_value (float): face value of bond
        par_rate (float): bond coupon
        term (int): the maturity of the bond

    Returns:
        float: Macaulay duration
    """
    pmts = [par_value*par_rate] * (term - 1) + [par_value*par_rate + par_value]
    return sum((t+1) * pmt/pow(1+ytm, t+1) for t, pmt in enumerate(pmts))/price


def modified_duration(price: float, ytm: float, par_value: float, par_rate: float, term: int) -> float:
    """Modified duration is calculated as Macaulay duration divided by one plus the bond's yield to
       maturity.Modified duration provides an approximate percentage in a bond's price for a 1% change
       in yield to maturity.


    Args:
        price (float): the current price of the bond
        ytm (float): bond yield to maturity
        par_value (float): face value of bond
        par_rate (float): bond coupon
        term (int): the maturity of the bond

    Returns:
        float: modified duration
    """
    return macaulay_duration(price, ytm, par_value, par_rate, term)/(1+ytm)


def pvbp(price: float, coupon: float, term: int) -> float:
    """calculate the price value of basis point(pvbp)
       price value of a basis point is the money change in the full price(In hundred dollars) of 
       a bond when its YTM change by one basis point, or 0.01% 

    Args:
        price (float): the current price of the bond
        coupon (float): Coupon, in hundred dollars
        term (int): the maturity of the bond

    Returns:
        float: price value of basis point(pvbp)
    """
    ytm = discount_rate(price, coupon, term, 100)
    v_plus = present_value(coupon, ytm-0.0001, term, 100)
    v_minus = present_value(coupon, ytm+0.0001, term, 100)
    return (v_plus-v_minus)/2


def convexity(price: float, coupon: float, term: int, face_value: float, delta: float = 0.0001) -> float:
    """Calculate the convexity of a bond

    Args:
        price (float): he current price of the bond
        coupon (float): bond coupons
        term (int): the maturity of the bond
        face_value (float): face value of the bond
        delta (float, optional): change in yield to maturity. Defaults to 0.0001.

    Returns:
        float: he convexity of a bond
    """
    ytm = discount_rate(price, coupon, term, face_value)
    v_plus = present_value(coupon, ytm-delta, term, face_value)
    v_minus = present_value(coupon, ytm+delta, term, face_value)
    return (v_minus+v_plus-2*price)/(delta*delta*price)
