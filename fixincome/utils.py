"""This module is a collection of helper functions.
"""

from typing import List

import numpy as np
from scipy.optimize import fsolve


def geometric_series_sum(a1: float, q: float, n: float) -> float:
    """Calculate the sum of a geometric sequence

    Args:
        a1 (float): first item
        q (float): common ratio
        n (int): number of items

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
