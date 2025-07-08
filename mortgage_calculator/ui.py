from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QDoubleSpinBox, QComboBox, QPushButton, QMessageBox, QFrame, QTabWidget, QSpinBox
)
from .calculator import calculate_down_payment, calculate_time_to_save, calculate_refinance_details

class MortgageCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mortgage & Refinance Calculator")
        self.setGeometry(100, 100, 450, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        down_payment_tab = self._create_down_payment_tab()
        refinance_tab = self._create_refinance_tab()

        self.tabs.addTab(down_payment_tab, "Down Payment Calculator")
        self.tabs.addTab(refinance_tab, "Refinance Calculator")

        self._connect_signals()

    def _create_down_payment_tab(self):
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        form_layout = QFormLayout()

        self.home_price_input = QDoubleSpinBox()
        self.home_price_input.setRange(0, 10_000_000)
        self.home_price_input.setValue(500_000)
        self.home_price_input.setPrefix("$ ")
        self.home_price_input.setGroupSeparatorShown(True)

        self.target_payment_input = QDoubleSpinBox()
        self.target_payment_input.setRange(0, 100_000)
        self.target_payment_input.setValue(3000)
        self.target_payment_input.setPrefix("$ ")
        self.target_payment_input.setGroupSeparatorShown(True)

        self.interest_rate_input = QDoubleSpinBox()
        self.interest_rate_input.setRange(0, 100)
        self.interest_rate_input.setValue(7.0)
        self.interest_rate_input.setSuffix(" %")

        self.loan_term_input = QComboBox()
        self.loan_term_input.addItems(["30", "20", "15", "10"])

        self.property_tax_input = QDoubleSpinBox()
        self.property_tax_input.setGroupSeparatorShown(True)
        self.property_tax_type_input = QComboBox()
        self.property_tax_type_input.addItems(["$", "%"])
        self._update_property_tax_input_style()


        self.home_insurance_input = QDoubleSpinBox()
        self.home_insurance_input.setRange(0, 1_000_000)
        self.home_insurance_input.setValue(1200)
        self.home_insurance_input.setPrefix("$ ")
        self.home_insurance_input.setGroupSeparatorShown(True)

        self.hoa_fees_input = QDoubleSpinBox()
        self.hoa_fees_input.setRange(0, 10_000)
        self.hoa_fees_input.setValue(50)
        self.hoa_fees_input.setPrefix("$ ")
        self.hoa_fees_input.setGroupSeparatorShown(True)

        self.closing_costs_input = QDoubleSpinBox()
        self.closing_costs_input.setRange(0, 1_000_000)
        self.closing_costs_input.setValue(10000)
        self.closing_costs_input.setPrefix("$ ")
        self.closing_costs_input.setGroupSeparatorShown(True)

        self.pmi_rate_input = QDoubleSpinBox()
        self.pmi_rate_input.setRange(0, 10)
        self.pmi_rate_input.setValue(0.5)
        self.pmi_rate_input.setSuffix(" %")

        form_layout.addRow("Home Price:", self.home_price_input)
        form_layout.addRow("Target Monthly Payment:", self.target_payment_input)
        form_layout.addRow("Interest Rate (Annual):", self.interest_rate_input)
        form_layout.addRow("Loan Term (Years):", self.loan_term_input)

        property_tax_layout = QHBoxLayout()
        property_tax_layout.addWidget(self.property_tax_input)
        property_tax_layout.addWidget(self.property_tax_type_input)
        form_layout.addRow("Property Tax (Annual):", property_tax_layout)

        form_layout.addRow("Home Insurance (Annual):", self.home_insurance_input)
        form_layout.addRow("HOA Fees (Monthly):", self.hoa_fees_input)
        form_layout.addRow("Closing Costs:", self.closing_costs_input)
        form_layout.addRow("PMI Rate (Annual):", self.pmi_rate_input)

        layout.addLayout(form_layout)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        savings_header = QLabel("Time to Save for Down Payment")
        savings_header.setStyleSheet("font-weight: bold; margin-top: 5px;")
        layout.addWidget(savings_header)

        savings_form_layout = QFormLayout()

        self.current_savings_input = QDoubleSpinBox()
        self.current_savings_input.setRange(0, 10_000_000)
        self.current_savings_input.setValue(20_000)
        self.current_savings_input.setPrefix("$ ")
        self.current_savings_input.setGroupSeparatorShown(True)

        self.checking_account_input = QDoubleSpinBox()
        self.checking_account_input.setRange(0, 10_000_000)
        self.checking_account_input.setValue(5_000)
        self.checking_account_input.setPrefix("$ ")
        self.checking_account_input.setGroupSeparatorShown(True)

        self.savings_rate_input = QDoubleSpinBox()
        self.savings_rate_input.setRange(0, 100)
        self.savings_rate_input.setValue(4.5)
        self.savings_rate_input.setSuffix(" %")

        self.monthly_paycheck_input = QDoubleSpinBox()
        self.monthly_paycheck_input.setRange(0, 1_000_000)
        self.monthly_paycheck_input.setValue(5000)
        self.monthly_paycheck_input.setPrefix("$ ")
        self.monthly_paycheck_input.setGroupSeparatorShown(True)

        self.monthly_dividend_input = QDoubleSpinBox()
        self.monthly_dividend_input.setRange(0, 1_000_000)
        self.monthly_dividend_input.setValue(100)
        self.monthly_dividend_input.setPrefix("$ ")
        self.monthly_dividend_input.setGroupSeparatorShown(True)

        self.other_income_input = QDoubleSpinBox()
        self.other_income_input.setRange(0, 1_000_000)
        self.other_income_input.setValue(0)
        self.other_income_input.setPrefix("$ ")
        self.other_income_input.setGroupSeparatorShown(True)

        self.monthly_expenses_input = QDoubleSpinBox()
        self.monthly_expenses_input.setRange(0, 1_000_000)
        self.monthly_expenses_input.setValue(3000)
        self.monthly_expenses_input.setPrefix("$ ")
        self.monthly_expenses_input.setGroupSeparatorShown(True)

        savings_form_layout.addRow("Current Savings:", self.current_savings_input)
        savings_form_layout.addRow("Current Checking Account:", self.checking_account_input)
        savings_form_layout.addRow("Savings APY:", self.savings_rate_input)
        savings_form_layout.addRow("Monthly Paycheck:", self.monthly_paycheck_input)
        savings_form_layout.addRow("Monthly Dividend Income:", self.monthly_dividend_input)
        savings_form_layout.addRow("Other Monthly Income:", self.other_income_input)
        savings_form_layout.addRow("Monthly Expenses:", self.monthly_expenses_input)

        layout.addLayout(savings_form_layout)

        self.calculate_button = QPushButton("Calculate Down Payment")
        layout.addWidget(self.calculate_button)

        self.result_down_payment_label = QLabel("Required Down Payment: -")
        self.result_down_payment_percentage_label = QLabel("Required Down Payment %: -")

        layout.addWidget(self.result_down_payment_label)
        layout.addWidget(self.result_down_payment_percentage_label)

        self.savings_status_label = QLabel("Savings Status: -")
        layout.addWidget(self.savings_status_label)

        self.result_time_to_save_label = QLabel("Time to save: -")
        layout.addWidget(self.result_time_to_save_label)

        return tab_widget

    def _create_refinance_tab(self):
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        form_layout = QFormLayout()

        # Inputs
        self.refi_orig_amount_input = QDoubleSpinBox()
        self.refi_orig_amount_input.setRange(0, 10_000_000)
        self.refi_orig_amount_input.setValue(300_000)
        self.refi_orig_amount_input.setPrefix("$ ")
        self.refi_orig_amount_input.setGroupSeparatorShown(True)

        self.refi_orig_rate_input = QDoubleSpinBox()
        self.refi_orig_rate_input.setRange(0, 100)
        self.refi_orig_rate_input.setValue(6.5)
        self.refi_orig_rate_input.setSuffix(" %")

        self.refi_orig_term_input = QComboBox()
        self.refi_orig_term_input.addItems(["30", "20", "15", "10"])

        self.refi_months_paid_input = QSpinBox()
        self.refi_months_paid_input.setRange(0, 30 * 12)
        self.refi_months_paid_input.setValue(24)

        self.refi_new_rate_input = QDoubleSpinBox()
        self.refi_new_rate_input.setRange(0, 100)
        self.refi_new_rate_input.setValue(5.5)
        self.refi_new_rate_input.setSuffix(" %")

        self.refi_new_term_input = QComboBox()
        self.refi_new_term_input.addItems(["30", "20", "15", "10"])

        self.refi_closing_costs_input = QDoubleSpinBox()
        self.refi_closing_costs_input.setRange(0, 100_000)
        self.refi_closing_costs_input.setValue(5000)
        self.refi_closing_costs_input.setPrefix("$ ")
        self.refi_closing_costs_input.setGroupSeparatorShown(True)

        form_layout.addRow("Original Loan Amount:", self.refi_orig_amount_input)
        form_layout.addRow("Original Interest Rate:", self.refi_orig_rate_input)
        form_layout.addRow("Original Loan Term (Years):", self.refi_orig_term_input)
        form_layout.addRow("Months Already Paid:", self.refi_months_paid_input)
        form_layout.addRow("New Interest Rate:", self.refi_new_rate_input)
        form_layout.addRow("New Loan Term (Years):", self.refi_new_term_input)
        form_layout.addRow("Refinance Closing Costs:", self.refi_closing_costs_input)
        layout.addLayout(form_layout)

        # Results
        self.refi_calculate_button = QPushButton("Calculate Refinance Savings")
        layout.addWidget(self.refi_calculate_button)

        self.refi_orig_payment_label = QLabel("Original Monthly Payment: -")
        self.refi_new_payment_label = QLabel("New Monthly Payment: -")
        self.refi_monthly_savings_label = QLabel("Monthly Savings: -")
        self.refi_breakeven_label = QLabel("Break-even Point: -")
        self.refi_lifetime_savings_label = QLabel("Lifetime Savings: -")

        layout.addWidget(self.refi_orig_payment_label)
        layout.addWidget(self.refi_new_payment_label)
        layout.addWidget(self.refi_monthly_savings_label)
        layout.addWidget(self.refi_breakeven_label)
        layout.addWidget(self.refi_lifetime_savings_label)

        return tab_widget

    def _connect_signals(self):
        self.calculate_button.clicked.connect(self.perform_calculation)
        self.property_tax_type_input.currentTextChanged.connect(self._update_property_tax_input_style)
        self.refi_calculate_button.clicked.connect(self.perform_refi_calculation)

    def _update_property_tax_input_style(self):
        if self.property_tax_type_input.currentText() == "$":
            self.property_tax_input.setPrefix("$ ")
            self.property_tax_input.setSuffix("")
            self.property_tax_input.setRange(0, 1_000_000)
            self.property_tax_input.setValue(6000)
        else: # "%"
            self.property_tax_input.setPrefix("")
            self.property_tax_input.setSuffix(" %")
            self.property_tax_input.setRange(0, 100)
            self.property_tax_input.setValue(1.2)

    def perform_calculation(self):
        try:
            property_tax_value = self.property_tax_input.value()
            if self.property_tax_type_input.currentText() == "%":
                property_tax_amount = (property_tax_value / 100) * self.home_price_input.value()
            else: # "$"
                property_tax_amount = property_tax_value

            down_payment, down_payment_percent = calculate_down_payment(
                home_price=self.home_price_input.value(),
                target_monthly_payment=self.target_payment_input.value(),
                interest_rate=self.interest_rate_input.value(),
                loan_term_years=int(self.loan_term_input.currentText()),
                property_tax=property_tax_amount,
                home_insurance=self.home_insurance_input.value(),
                hoa_fees=self.hoa_fees_input.value(),
                pmi_rate=self.pmi_rate_input.value(),
            )

            self.result_down_payment_label.setText(f"Required Down Payment: ${down_payment:,.2f}")
            self.result_down_payment_percentage_label.setText(f"Required Down Payment %: {down_payment_percent:.2f}%")

            # Calculate savings status and time to save
            closing_costs = self.closing_costs_input.value()
            total_needed = down_payment + closing_costs
            initial_savings = self.current_savings_input.value() + self.checking_account_input.value()
            savings_difference = total_needed - initial_savings

            if savings_difference > 0:
                percentage_left = (savings_difference / total_needed) * 100 if total_needed > 0 else 0
                self.savings_status_label.setText(
                    f"Savings Status: ${savings_difference:,.2f} left to save ({percentage_left:.2f}%)"
                )
            else:
                self.savings_status_label.setText(
                    f"Savings Status: ${abs(savings_difference):,.2f} over your goal!"
                )

            monthly_income = (
                self.monthly_paycheck_input.value() +
                self.monthly_dividend_input.value() +
                self.other_income_input.value()
            )
            monthly_contribution = monthly_income - self.monthly_expenses_input.value()

            if total_needed > 0:
                time_to_save_months = calculate_time_to_save(
                    target_savings=total_needed,
                    initial_savings=initial_savings,
                    monthly_contribution=monthly_contribution,
                    annual_interest_rate=self.savings_rate_input.value()
                )
                years = time_to_save_months // 12
                months = time_to_save_months % 12
                self.result_time_to_save_label.setText(f"Time to save: {years} years, {months} months")
            else:
                self.result_time_to_save_label.setText("Time to save: Not applicable (no savings needed)")


        except ValueError as e:
            QMessageBox.warning(self, "Calculation Error", str(e))
            self.result_down_payment_label.setText("Required Down Payment: -")
            self.result_down_payment_percentage_label.setText("Required Down Payment %: -")
            self.savings_status_label.setText("Savings Status: -")
            self.result_time_to_save_label.setText("Time to save: -")

    def perform_refi_calculation(self):
        try:
            results = calculate_refinance_details(
                original_loan_amount=self.refi_orig_amount_input.value(),
                original_interest_rate=self.refi_orig_rate_input.value(),
                original_loan_term_years=int(self.refi_orig_term_input.currentText()),
                months_paid=self.refi_months_paid_input.value(),
                new_interest_rate=self.refi_new_rate_input.value(),
                new_loan_term_years=int(self.refi_new_term_input.currentText()),
                refinance_closing_costs=self.refi_closing_costs_input.value(),
            )

            self.refi_orig_payment_label.setText(f"Original Monthly Payment: ${results['original_monthly_payment']:,.2f}")
            self.refi_new_payment_label.setText(f"New Monthly Payment: ${results['new_monthly_payment']:,.2f}")

            monthly_savings = results['monthly_savings']
            if monthly_savings >= 0:
                self.refi_monthly_savings_label.setText(f"Monthly Savings: ${monthly_savings:,.2f}")
            else:
                self.refi_monthly_savings_label.setText(f"Monthly Cost Increase: ${abs(monthly_savings):,.2f}")

            break_even = results['break_even_months']
            if break_even != float('inf'):
                years = int(break_even // 12)
                months = int(break_even % 12)
                self.refi_breakeven_label.setText(f"Break-even Point: {years} years, {months} months")
            else:
                self.refi_breakeven_label.setText("Break-even Point: Not achievable")

            lifetime_savings = results['lifetime_savings']
            if lifetime_savings >= 0:
                self.refi_lifetime_savings_label.setText(f"Lifetime Savings: ${lifetime_savings:,.2f}")
            else:
                self.refi_lifetime_savings_label.setText(f"Lifetime Loss: ${abs(lifetime_savings):,.2f}")

        except ValueError as e:
            QMessageBox.warning(self, "Calculation Error", str(e))
            self.refi_orig_payment_label.setText("Original Monthly Payment: -")
            self.refi_new_payment_label.setText("New Monthly Payment: -")
            self.refi_monthly_savings_label.setText("Monthly Savings: -")
            self.refi_breakeven_label.setText("Break-even Point: -")
            self.refi_lifetime_savings_label.setText("Lifetime Savings: -")
