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


def _calculate_monthly_pi(principal, annual_rate_percent, term_years):
    """Helper to calculate principal and interest payment."""
    if principal <= 0:
        return 0
    monthly_rate = annual_rate_percent / 100 / 12
    num_payments = term_years * 12

    if num_payments == 0:
        raise ValueError("Loan term cannot be zero years.")

    if monthly_rate == 0:
        return principal / num_payments

    payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return payment


def calculate_amortization_schedule(
    loan_amount: float,
    annual_interest_rate: float,
    loan_term_years: int,
    additional_principal_payment: float = 0.0,
) -> list[dict]:
    """
    Calculates the amortization schedule for a loan.

    Args:
        loan_amount: The total amount of the loan.
        annual_interest_rate: The annual interest rate (as a percentage).
        loan_term_years: The term of the loan in years.
        additional_principal_payment: Extra amount paid towards principal each month.

    Returns:
        A list of dictionaries, where each dictionary represents a month's payment details.
    """
    monthly_interest_rate = annual_interest_rate / 100 / 12
    num_payments = loan_term_years * 12

    if loan_amount <= 0:
        return []

    monthly_payment = _calculate_monthly_pi(
        loan_amount, annual_interest_rate, loan_term_years
    )

    remaining_balance = loan_amount
    schedule = []
    month = 0

    while remaining_balance > 0:
        month += 1
        # Safety break to prevent infinite loops
        if month > num_payments * 2:
            break

        interest_payment = remaining_balance * monthly_interest_rate

        principal_paid = (monthly_payment - interest_payment) + additional_principal_payment
        total_payment = monthly_payment + additional_principal_payment

        if remaining_balance <= principal_paid:
            # This is the final payment
            total_payment = remaining_balance + interest_payment
            principal_paid = remaining_balance
            remaining_balance = 0
        else:
            remaining_balance -= principal_paid

        schedule.append(
            {
                "Month": month,
                "Monthly Payment": total_payment,
                "Principal": principal_paid,
                "Interest": interest_payment,
                "Remaining Balance": remaining_balance,
            }
        )

    return schedule


def calculate_refinance_details(
    original_loan_amount: float,
    original_interest_rate: float,
    original_loan_term_years: int,
    months_paid: int,
    new_interest_rate: float,
    new_loan_term_years: int,
    refinance_closing_costs: float,
    additional_principal_payment: float = 0.0,
) -> dict:
    """
    Calculates the details of a mortgage refinance.

    Returns:
        A dictionary with refinance details.
    """
    # 1. Original loan details
    original_monthly_rate = original_interest_rate / 100 / 12
    original_num_payments = original_loan_term_years * 12
    original_monthly_payment = _calculate_monthly_pi(
        original_loan_amount, original_interest_rate, original_loan_term_years
    )

    # 2. Remaining balance
    remaining_payments = original_num_payments - months_paid
    if remaining_payments <= 0:
        remaining_balance = 0.0
    else:
        if original_monthly_rate > 0:
            # Formula for remaining balance
            remaining_balance = original_loan_amount * (
                ((1 + original_monthly_rate) ** original_num_payments) -
                ((1 + original_monthly_rate) ** months_paid)
            ) / (((1 + original_monthly_rate) ** original_num_payments) - 1)
        else:  # 0 interest
            remaining_balance = original_loan_amount * (remaining_payments / original_num_payments)

    # 3. New loan details
    new_loan_amount = remaining_balance + refinance_closing_costs
    new_monthly_payment = _calculate_monthly_pi(
        new_loan_amount, new_interest_rate, new_loan_term_years
    )

    # 4. Savings and break-even
    monthly_savings = original_monthly_payment - new_monthly_payment
    break_even_months = refinance_closing_costs / monthly_savings if monthly_savings > 0 else float('inf')

    # 5. Lifetime savings
    total_to_pay_original = original_monthly_payment * remaining_payments

    new_loan_amortization = calculate_amortization_schedule(
        loan_amount=new_loan_amount,
        annual_interest_rate=new_interest_rate,
        loan_term_years=new_loan_term_years,
        additional_principal_payment=additional_principal_payment,
    )

    total_to_pay_refinanced = sum(p["Monthly Payment"] for p in new_loan_amortization) if new_loan_amortization else 0
    lifetime_savings = total_to_pay_original - total_to_pay_refinanced

    return {
        "original_monthly_payment": original_monthly_payment,
        "new_monthly_payment": new_monthly_payment,
        "monthly_savings": monthly_savings,
        "break_even_months": break_even_months,
        "lifetime_savings": lifetime_savings,
        "amortization_schedule": new_loan_amortization,
    }
