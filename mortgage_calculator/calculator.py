import math

def calculate_down_payment(
    home_price: float,
    interest_rate: float,
    loan_term_years: int,
    property_tax: float,
    home_insurance: float,
    hoa_fees: float,
    pmi_rate: float,
    target_monthly_payment: float,
) -> tuple[float, float]:
    """
    Calculates the required down payment to achieve a target monthly payment.

    Args:
        home_price: The total price of the home.
        interest_rate: The annual interest rate (as a percentage, e.g., 7.0).
        loan_term_years: The loan term in years.
        property_tax: The annual property tax amount.
        home_insurance: The annual home insurance amount.
        hoa_fees: The monthly HOA fees.
        pmi_rate: The annual PMI rate as a percentage of the loan amount.
        target_monthly_payment: The desired total monthly payment.

    Returns:
        A tuple containing:
        - The required down payment in dollars.
        - The required down payment as a percentage of the home price.

    Raises:
        ValueError: If the calculation is not possible with the given inputs.
    """
    monthly_property_tax = property_tax / 12
    monthly_home_insurance = home_insurance / 12
    other_monthly_costs = monthly_property_tax + monthly_home_insurance + hoa_fees

    if target_monthly_payment <= other_monthly_costs:
        raise ValueError(
            "Target monthly payment is too low to even cover taxes, insurance, and HOA."
        )

    target_mortgage_payment = target_monthly_payment - other_monthly_costs

    monthly_interest_rate = interest_rate / 100 / 12
    num_payments = loan_term_years * 12

    if monthly_interest_rate == 0:
        if num_payments == 0:
            raise ValueError("Loan term cannot be zero years.")
        mortgage_factor = 1 / num_payments
    else:
        mortgage_factor = (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / \
                          ((1 + monthly_interest_rate) ** num_payments - 1)

    # Scenario 1: Assume no PMI is needed.
    loan_amount_no_pmi = target_mortgage_payment / mortgage_factor
    down_payment_no_pmi = home_price - loan_amount_no_pmi

    if down_payment_no_pmi < 0:
        return 0.0, 0.0

    down_payment_percentage = (down_payment_no_pmi / home_price) * 100

    if down_payment_percentage >= 20:
        return down_payment_no_pmi, down_payment_percentage

    # Scenario 2: PMI is needed.
    if pmi_rate <= 0:
        raise ValueError(
            "A down payment of less than 20% is required, but PMI rate is zero or negative."
        )

    monthly_pmi_factor = pmi_rate / 100 / 12
    total_factor_with_pmi = mortgage_factor + monthly_pmi_factor

    loan_amount_with_pmi = target_mortgage_payment / total_factor_with_pmi
    down_payment_with_pmi = home_price - loan_amount_with_pmi

    if down_payment_with_pmi < 0:
        return 0.0, 0.0

    down_payment_percentage_with_pmi = (down_payment_with_pmi / home_price) * 100

    # If the calculation including PMI results in a down payment of 20% or more,
    # it means the target payment can be met or beaten with exactly a 20% down payment,
    # thus avoiding PMI.
    if down_payment_percentage_with_pmi >= 20:
        down_payment_at_20_percent = home_price * 0.20
        return down_payment_at_20_percent, 20.0

    return down_payment_with_pmi, down_payment_percentage_with_pmi


def calculate_time_to_save(
    target_savings: float,
    initial_savings: float,
    monthly_contribution: float,
    annual_interest_rate: float,
) -> int:
    """
    Calculates the time in months to save for a target amount.

    Args:
        target_savings: The target savings amount (e.g., down payment).
        initial_savings: The current amount of savings.
        monthly_contribution: The amount saved each month.
        annual_interest_rate: The annual interest rate of the savings account (as a percentage).

    Returns:
        The time in months to reach the target savings.

    Raises:
        ValueError: If the savings goal is not achievable.
    """
    if initial_savings >= target_savings:
        return 0

    # Handle case with no interest
    if annual_interest_rate == 0:
        if monthly_contribution <= 0:
            raise ValueError("With no interest and no monthly savings, goal is unreachable.")
        months = (target_savings - initial_savings) / monthly_contribution
        return math.ceil(months)

    monthly_rate = annual_interest_rate / 100 / 12

    # If monthly contributions are not enough to grow the principal
    if monthly_contribution + initial_savings * monthly_rate <= 0:
        raise ValueError("Savings will not grow with the current monthly contribution.")

    try:
        # Using formula: n = log((PMT + FV*i) / (PMT + PV*i)) / log(1+i)
        numerator = monthly_contribution + target_savings * monthly_rate
        denominator = monthly_contribution + initial_savings * monthly_rate

        if denominator <= 0:
            raise ValueError("Savings will deplete over time.")

        if (numerator / denominator) <= 1:
            raise ValueError("Savings goal is not achievable with current parameters.")

        months = math.log(numerator / denominator) / math.log(1 + monthly_rate)
    except (ValueError, ZeroDivisionError):
        raise ValueError("Calculation failed. Please check savings parameters.")

    return math.ceil(months)
