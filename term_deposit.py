import sys
from decimal import ROUND_HALF_DOWN, Decimal

from errors import (
    InvalidPaymentFrequencyError,
    MinimumDepositError,
    InvalidInterestRateError,
)

from financial_tools import (
    interest_earned_on_n_months,
    interest_earned_on_n_years,
    compound_interest_after_n_years,
    compound_interest_after_n_months,
    annual_interest_rate,
    monthly_interest_rate,
)
from logger import logger


class TermDeposit:
    def __init__(
        self,
        initial_deposit: float,
        interest_rate: float,
        term_years: int,
        term_months: int,
        payment_frequency: str,
    ):
        self.initial_deposit = self._validate_and_format_deposit(initial_deposit)
        self.nominal_interest_rate = self._validate_nominal_interest_rate(interest_rate)
        self.term_years = term_years
        self.term_months = term_months
        self.payment_frequency = self._validate_frequency(payment_frequency)

    def _validate_and_format_deposit(self, initial_deposit: float) -> float:
        if initial_deposit < 1000:
            raise MinimumDepositError(
                "A Term Deposit account requires a minimum initial deposit of AUD $1000.00"
            )
        return Decimal(initial_deposit)

    def _validate_nominal_interest_rate(self, interest_rate: float) -> float:
        if not (interest_rate > 0 and interest_rate <= 5):
            raise InvalidInterestRateError(
                f"The nominal interest rate '{interest_rate}' needs to be greater than 0 and as much as 5."
            )
        return interest_rate

    def _validate_frequency(self, frequency: str) -> str:
        try:
            validated_frequency = next(
                filter(
                    lambda f: f == frequency.upper(),
                    ["MONTHLY", "QUARTERLY", "ANNUALLY", "AT_MATURITY"],
                )
            )
        except StopIteration:
            raise InvalidPaymentFrequencyError(
                f"The payment frequency '{frequency}' was misspelled or is not a valid frequency."
            )
        return validated_frequency

    def get_balance_at_maturity(self) -> Decimal:
        running_balance = Decimal(self.initial_deposit)
        monthly_rate = monthly_interest_rate(self.nominal_interest_rate)
        annual_rate = annual_interest_rate(self.nominal_interest_rate)
        class_summary_logging = (
            f"Calculating the balance at maturity for a term deposit account with the following inputs: "
            f"Amount: ${self.initial_deposit} "
            f"Interest Rate: {self.nominal_interest_rate}% "
            f"Years: {self.term_years} "
            f"Months: {self.term_months} "
        )
        if self.payment_frequency == "MONTHLY":
            logger.info(
                class_summary_logging + f" Frequency: {self.payment_frequency}"
            )
            # All inputs need to be in relative terms for the effective interest rate.
            term_as_months = self.term_years * 12 + self.term_months
            monthly_compound_interest_earned = compound_interest_after_n_months(
                monthly_rate, running_balance, term_as_months
            )
            final_balance = self.initial_deposit + monthly_compound_interest_earned

        elif self.payment_frequency == "QUARTERLY":
            logger.info(
                class_summary_logging + f" Frequency: {self.payment_frequency}."
            )
            term_as_months = self.term_years * 12 + self.term_months
            extra_months = term_as_months % 4
            months_within_quarters = term_as_months - extra_months

            quarterly_compound_interest_earned = compound_interest_after_n_months(
                monthly_rate,
                running_balance,
                months_within_quarters,
                compounding_frequency=4,
            )
            running_balance += quarterly_compound_interest_earned
            monthly_interest_earned = interest_earned_on_n_months(
                monthly_rate, running_balance, extra_months
            )

            final_balance = (
                self.initial_deposit
                + quarterly_compound_interest_earned
                + monthly_interest_earned
            )

        elif self.payment_frequency == "ANNUALLY":
            logger.info(
                class_summary_logging + f" Frequency: {self.payment_frequency}."
            )
            annual_compound_interest_earned = compound_interest_after_n_years(
                annual_rate, running_balance, self.term_years
            )
            running_balance += annual_compound_interest_earned
            monthly_interest_earned = interest_earned_on_n_months(
                monthly_rate, running_balance, self.term_months
            )
            final_balance = (
                self.initial_deposit
                + annual_compound_interest_earned
                + monthly_interest_earned
            )

        elif self.payment_frequency == "AT_MATURITY":
            logger.info(
                class_summary_logging + f" Frequency: {self.payment_frequency}."
            )
            annual_interest_earned = interest_earned_on_n_years(
                annual_rate, running_balance, self.term_years
            )
            monthly_interest_earned = interest_earned_on_n_months(
                monthly_rate, running_balance, self.term_months
            )
            final_balance = (
                self.initial_deposit + annual_interest_earned + monthly_interest_earned
            )

        return final_balance.quantize(Decimal("1."), rounding=ROUND_HALF_DOWN)


if __name__ == "__main__":
    filename, *user_inputs = sys.argv
    (
        initial_deposit,
        interest_rate,
        term_years,
        term_months,
        payment_frequency,
    ) = user_inputs
    account = TermDeposit(
        float(initial_deposit),
        float(interest_rate),
        int(term_years),
        int(term_months),
        payment_frequency,
    )
    result = account.get_balance_at_maturity()
    print(f"Final balance: {result}")
