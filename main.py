import streamlit as st
from mortgage_calculator.calculator import (
    calculate_down_payment,
    calculate_time_to_save,
    calculate_refinance_details,
)

def down_payment_calculator_tab():
    """UI and logic for the down payment calculator tab."""
    with st.form(key="down_payment_form"):
        st.header("Mortgage Details")
        home_price = st.number_input("Home Price:", min_value=0.0, value=500_000.0, step=1000.0, format="$%.2f")
        target_monthly_payment = st.number_input("Target Monthly Payment:", min_value=0.0, value=3000.0, step=100.0, format="$%.2f")
        interest_rate = st.number_input("Interest Rate (Annual):", min_value=0.0, max_value=100.0, value=7.0, step=0.1, format="%.2f %%")
        loan_term_years = st.selectbox("Loan Term (Years):", options=[30, 20, 15, 10], index=0)

        col1, col2 = st.columns(2)
        with col1:
            property_tax_value = st.number_input("Property Tax (Annual):", min_value=0.0, value=1.2, step=0.1)
        with col2:
            property_tax_type = st.selectbox("Tax Type", options=["%", "$"], index=0, label_visibility="collapsed")

        home_insurance = st.number_input("Home Insurance (Annual):", min_value=0.0, value=1200.0, step=100.0, format="$%.2f")
        hoa_fees = st.number_input("HOA Fees (Monthly):", min_value=0.0, value=50.0, step=10.0, format="$%.2f")
        pmi_rate = st.number_input("PMI Rate (Annual):", min_value=0.0, max_value=10.0, value=0.5, step=0.01, format="%.2f %%")

        st.header("Savings Details")
        closing_costs = st.number_input("Closing Costs:", min_value=0.0, value=10000.0, step=500.0, format="$%.2f")
        current_savings = st.number_input("Current Savings:", min_value=0.0, value=20_000.0, step=1000.0, format="$%.2f")
        checking_account = st.number_input("Current Checking Account:", min_value=0.0, value=5_000.0, step=1000.0, format="$%.2f")
        savings_rate = st.number_input("Savings APY:", min_value=0.0, max_value=100.0, value=4.5, step=0.1, format="%.2f %%")
        monthly_paycheck = st.number_input("Monthly Paycheck:", min_value=0.0, value=5000.0, step=100.0, format="$%.2f")
        monthly_dividend = st.number_input("Monthly Dividend Income:", min_value=0.0, value=100.0, step=10.0, format="$%.2f")
        other_income = st.number_input("Other Monthly Income:", min_value=0.0, value=0.0, step=10.0, format="$%.2f")
        monthly_expenses = st.number_input("Monthly Expenses:", min_value=0.0, value=3000.0, step=100.0, format="$%.2f")

        submit_button = st.form_submit_button(label="Calculate Down Payment")

    if submit_button:
        try:
            if property_tax_type == "%":
                property_tax_amount = (property_tax_value / 100) * home_price
            else:  # "$"
                property_tax_amount = property_tax_value

            down_payment, down_payment_percent = calculate_down_payment(
                home_price=home_price,
                target_monthly_payment=target_monthly_payment,
                interest_rate=interest_rate,
                loan_term_years=loan_term_years,
                property_tax=property_tax_amount,
                home_insurance=home_insurance,
                hoa_fees=hoa_fees,
                pmi_rate=pmi_rate,
            )

            st.success(f"**Required Down Payment: ${down_payment:,.2f}** ({down_payment_percent:.2f}%)")

            total_needed = down_payment + closing_costs
            initial_savings = current_savings + checking_account
            savings_difference = total_needed - initial_savings

            if savings_difference > 0:
                percentage_left = (savings_difference / total_needed) * 100 if total_needed > 0 else 0
                st.info(f"**Savings Status:** You have **${initial_savings:,.2f}** saved. You need **${total_needed:,.2f}** for the down payment and closing costs. You have **${savings_difference:,.2f}** left to save ({percentage_left:.2f}%).")
            else:
                st.success(f"**Savings Status:** You have **${initial_savings:,.2f}** saved, which is **${abs(savings_difference):,.2f}** over your goal of **${total_needed:,.2f}**!")

            monthly_income = monthly_paycheck + monthly_dividend + other_income
            monthly_contribution = monthly_income - monthly_expenses

            if total_needed > initial_savings:
                if monthly_contribution <= 0:
                    st.warning("**Time to save:** Your monthly expenses are greater than or equal to your income. You are not able to save money.")
                else:
                    time_to_save_months = calculate_time_to_save(
                        target_savings=total_needed,
                        initial_savings=initial_savings,
                        monthly_contribution=monthly_contribution,
                        annual_interest_rate=savings_rate
                    )
                    years = time_to_save_months // 12
                    months = time_to_save_months % 12
                    st.info(f"**Time to save:** With a monthly contribution of **${monthly_contribution:,.2f}**, it will take you **{years} years and {months} months** to save for your down payment and closing costs.")
            else:
                st.success("**Time to save:** You already have enough saved for your down payment and closing costs!")

        except ValueError as e:
            st.error(f"Calculation Error: {e}")

def refinance_calculator_tab():
    """UI and logic for the refinance calculator tab."""
    with st.form(key="refinance_form"):
        st.header("Refinance Details")
        
        st.subheader("Original Loan")
        refi_orig_amount = st.number_input("Original Loan Amount:", min_value=0.0, value=300_000.0, step=1000.0, format="$%.2f")
        refi_orig_rate = st.number_input("Original Interest Rate:", min_value=0.0, max_value=100.0, value=6.5, step=0.1, format="%.2f %%")
        refi_orig_term = st.selectbox("Original Loan Term (Years):", options=[30, 20, 15, 10], index=0, key="refi_orig_term")
        refi_months_paid = st.number_input("Months Already Paid:", min_value=0, value=24, step=1)

        st.subheader("New Loan")
        refi_new_rate = st.number_input("New Interest Rate:", min_value=0.0, max_value=100.0, value=5.5, step=0.1, format="%.2f %%")
        refi_new_term = st.selectbox("New Loan Term (Years):", options=[30, 20, 15, 10], index=0, key="refi_new_term")
        refi_closing_costs = st.number_input("Refinance Closing Costs:", min_value=0.0, value=5000.0, step=100.0, format="$%.2f")

        submit_button = st.form_submit_button(label="Calculate Refinance Savings")

    if submit_button:
        try:
            results = calculate_refinance_details(
                original_loan_amount=refi_orig_amount,
                original_interest_rate=refi_orig_rate,
                original_loan_term_years=refi_orig_term,
                months_paid=refi_months_paid,
                new_interest_rate=refi_new_rate,
                new_loan_term_years=refi_new_term,
                refinance_closing_costs=refi_closing_costs,
            )

            st.metric(label="Original Monthly Payment", value=f"${results['original_monthly_payment']:,.2f}")
            st.metric(label="New Monthly Payment", value=f"${results['new_monthly_payment']:,.2f}", delta=f"${-results['monthly_savings']:,.2f}")

            monthly_savings = results['monthly_savings']
            if monthly_savings < 0:
                st.warning(f"Your monthly payment will increase by ${abs(monthly_savings):,.2f}.")

            break_even = results['break_even_months']
            if break_even != float('inf'):
                years = int(break_even // 12)
                months = int(break_even % 12)
                st.info(f"**Break-even Point:** {years} years, {months} months")
            else:
                st.warning("**Break-even Point:** Not achievable with these terms.")

            lifetime_savings = results['lifetime_savings']
            if lifetime_savings >= 0:
                st.success(f"**Lifetime Savings:** ${lifetime_savings:,.2f}")
            else:
                st.error(f"**Lifetime Loss:** ${abs(lifetime_savings):,.2f}")

        except ValueError as e:
            st.error(f"Calculation Error: {e}")

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="Mortgage & Refinance Calculator", layout="centered")
    st.title("Mortgage & Refinance Calculator")

    tab1, tab2 = st.tabs(["Down Payment Calculator", "Refinance Calculator"])

    with tab1:
        down_payment_calculator_tab()

    with tab2:
        refinance_calculator_tab()

if __name__ == "__main__":
    main()
