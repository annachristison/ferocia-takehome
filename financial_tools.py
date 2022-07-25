from decimal import Decimal


def effective_interest_rate(
    interest_rate_per_period: Decimal, term: int, compounding_frequency: int
) -> Decimal:
    """
    Based on the calculator here: https://www.calculatorsoup.com/calculators/financial/effective-interest-rate-calculator.php
    :param interest_rate_per_period: Given as a decimal in an annual, or annual adjusted to monthly rate.
    :param term: The total length of time, given in months or years.
    :param compounding_frequency: The intervals (months/years) during the term at which we compound interest.
    :return: A rate which can multiplied by an investment to get the compound interest earned over the term given.
    """
    return Decimal(
        (
            (1 + (interest_rate_per_period / compounding_frequency))
            ** (compounding_frequency * term)
        )
        - 1
    )


def monthly_interest_rate(nominal_interest_rate: float) -> Decimal:
    return Decimal((nominal_interest_rate / 100) / 12)


def annual_interest_rate(nominal_interest_rate: float) -> Decimal:
    return Decimal(nominal_interest_rate / 100)


def interest_earned_on_n_years(
    annual_rate: Decimal, balance: Decimal, number_of_years: int
) -> Decimal:
    return Decimal(annual_rate * balance * number_of_years)


def interest_earned_on_n_months(
    monthly_rate: Decimal, balance: Decimal, number_of_months: int
) -> Decimal:
    return Decimal(monthly_rate * balance * number_of_months)


def compound_interest_after_n_years(
    annual_rate: Decimal,
    balance: Decimal,
    number_of_years: int,
    compounding_frequency: int = 1,
) -> Decimal:
    if number_of_years == 0:
        return 0
    if number_of_years < 0:
        raise ValueError("The number of years needs to be a positive integer.")

    rate = effective_interest_rate(annual_rate, number_of_years, compounding_frequency)
    return balance * rate


def compound_interest_after_n_months(
    monthly_rate: Decimal,
    balance: Decimal,
    number_of_months: int,
    compounding_frequency: int = 1,
) -> Decimal:
    if number_of_months == 0:
        return 0
    if number_of_months < 0:
        raise ValueError("The number of months needs to be a positive integer.")

    rate = effective_interest_rate(
        monthly_rate, number_of_months, compounding_frequency
    )
    return balance * rate
