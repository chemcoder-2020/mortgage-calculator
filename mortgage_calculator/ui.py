from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QDoubleSpinBox, QComboBox, QPushButton, QMessageBox
)
from .calculator import calculate_down_payment

class MortgageCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mortgage Down Payment Calculator")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._create_form()
        self._create_results()
        self._connect_signals()

    def _create_form(self):
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
        self.property_tax_input.setRange(0, 1_000_000)
        self.property_tax_input.setValue(6000)
        self.property_tax_input.setPrefix("$ ")
        self.property_tax_input.setGroupSeparatorShown(True)

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

        self.pmi_rate_input = QDoubleSpinBox()
        self.pmi_rate_input.setRange(0, 10)
        self.pmi_rate_input.setValue(0.5)
        self.pmi_rate_input.setSuffix(" %")

        form_layout.addRow("Home Price:", self.home_price_input)
        form_layout.addRow("Target Monthly Payment:", self.target_payment_input)
        form_layout.addRow("Interest Rate (Annual):", self.interest_rate_input)
        form_layout.addRow("Loan Term (Years):", self.loan_term_input)
        form_layout.addRow("Property Tax (Annual):", self.property_tax_input)
        form_layout.addRow("Home Insurance (Annual):", self.home_insurance_input)
        form_layout.addRow("HOA Fees (Monthly):", self.hoa_fees_input)
        form_layout.addRow("PMI Rate (Annual):", self.pmi_rate_input)

        self.layout.addLayout(form_layout)

    def _create_results(self):
        self.calculate_button = QPushButton("Calculate Down Payment")
        self.layout.addWidget(self.calculate_button)

        self.result_down_payment_label = QLabel("Required Down Payment: -")
        self.result_down_payment_percentage_label = QLabel("Required Down Payment %: -")

        self.layout.addWidget(self.result_down_payment_label)
        self.layout.addWidget(self.result_down_payment_percentage_label)

    def _connect_signals(self):
        self.calculate_button.clicked.connect(self.perform_calculation)

    def perform_calculation(self):
        try:
            down_payment, down_payment_percent = calculate_down_payment(
                home_price=self.home_price_input.value(),
                target_monthly_payment=self.target_payment_input.value(),
                interest_rate=self.interest_rate_input.value(),
                loan_term_years=int(self.loan_term_input.currentText()),
                property_tax=self.property_tax_input.value(),
                home_insurance=self.home_insurance_input.value(),
                hoa_fees=self.hoa_fees_input.value(),
                pmi_rate=self.pmi_rate_input.value(),
            )

            self.result_down_payment_label.setText(f"Required Down Payment: ${down_payment:,.2f}")
            self.result_down_payment_percentage_label.setText(f"Required Down Payment %: {down_payment_percent:.2f}%")

        except ValueError as e:
            QMessageBox.warning(self, "Calculation Error", str(e))
            self.result_down_payment_label.setText("Required Down Payment: -")
            self.result_down_payment_percentage_label.setText("Required Down Payment %: -")
