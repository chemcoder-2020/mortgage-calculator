import sys
from PyQt6.QtWidgets import QApplication
from mortgage_calculator.ui import MortgageCalculatorApp

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = MortgageCalculatorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
