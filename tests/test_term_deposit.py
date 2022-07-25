from decimal import Decimal

import pytest

from financial_tools import (
    effective_interest_rate,
    monthly_interest_rate,
    annual_interest_rate,
    compound_interest_after_n_years,
    compound_interest_after_n_months,
)
from term_deposit import TermDeposit


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((10000, 1.10, 5, 0, "MONTHLY"), 10565),
        ((10000, 1.10, 4, 6, "MONTHLY"), 10507),
        ((10000, 1.10, 3, 2, "MONTHLY"), 10354),
        ((10000, 1.10, 2, 11, "MONTHLY"), 10326),
        ((10000, 1.10, 0, 4, "MONTHLY"), 10037),
    ],
)
def test_correctly_calculates_balance_at_maturity_for_monthly(test_input, expected):
    account = TermDeposit(*test_input)
    result = account.get_balance_at_maturity()

    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((10000, 1.10, 5, 0, "QUARTERLY"), 10565),
        ((10000, 1.10, 4, 6, "QUARTERLY"), 10507),
        ((10000, 1.10, 3, 2, "QUARTERLY"), 10354),
        ((10000, 1.10, 2, 11, "QUARTERLY"), 10326),
        ((10000, 1.10, 0, 4, "QUARTERLY"), 10037),
    ],
)
def test_correctly_calculates_balance_at_maturity_for_quarterly(test_input, expected):
    account = TermDeposit(*test_input)
    result = account.get_balance_at_maturity()

    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((10000, 1.10, 5, 0, "ANNUALLY"), 10562),
        ((10000, 1.10, 4, 6, "ANNUALLY"), 10505),
        ((10000, 1.10, 3, 2, "ANNUALLY"), 10353),
        ((10000, 1.10, 2, 11, "ANNUALLY"), 10324),
        ((10000, 1.10, 0, 4, "ANNUALLY"), 10037),
    ],
)
def test_correctly_calculates_balance_at_maturity_for_annually(test_input, expected):
    account = TermDeposit(*test_input)
    result = account.get_balance_at_maturity()

    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((10000, 1.10, 5, 0, "AT_MATURITY"), 10550),
        ((10000, 1.10, 4, 6, "AT_MATURITY"), 10495),
        ((10000, 1.10, 3, 2, "AT_MATURITY"), 10348),
        ((10000, 1.10, 2, 11, "AT_MATURITY"), 10321),
        ((10000, 1.10, 0, 4, "AT_MATURITY"), 10037),
    ],
)
def test_correctly_calculates_balance_at_maturity_for_at_maturity(test_input, expected):
    account = TermDeposit(*test_input)
    result = account.get_balance_at_maturity()

    assert result == expected


def test_effective_interest_rate():
    interest_rate_per_period = 0.0325
    term = 5
    compounding_frequency = 12
    rate = effective_interest_rate(
        interest_rate_per_period, term, compounding_frequency
    ).quantize(Decimal("1.00000"))
    assert rate == Decimal(".17619")


def test_monthly_interest_rate():
    rate = monthly_interest_rate(2.9).quantize(Decimal("1.00000"))
    assert rate == Decimal("0.00242")


def test_annual_interest_rate():
    rate = annual_interest_rate(2.9).quantize(Decimal("1.00000"))
    assert rate == Decimal("0.02900")


def test_compound_interest_after_n_years_correctly_calculates_interest_earned():
    annual_rate = Decimal("0.02900")
    balance = Decimal("1000")
    number_of_years = 5
    rate = compound_interest_after_n_years(
        annual_rate, balance, number_of_years
    ).quantize(Decimal("1."))

    assert rate == Decimal("154")


def test_compound_interest_after_n_months_correctly_calculates_interest_earned():
    monthly_rate = Decimal("0.00242")
    balance = Decimal("1000")
    number_of_months = 60
    rate = compound_interest_after_n_months(
        monthly_rate, balance, number_of_months
    ).quantize(Decimal("1."))
    assert rate == Decimal("156")
