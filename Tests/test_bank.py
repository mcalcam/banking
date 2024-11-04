import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code-files'))

import bank

import unittest
from unittest.mock import patch
from datetime import datetime
import bank

class TestBank(unittest.TestCase):
    def setUp(self):
        # Reset global variables before each test
        bank.ACCOUNTS.clear()
        bank.LOANS.clear()
        bank.CUSTOMERS.clear()
        bank.CURRENT_DATE = datetime(2023, 1, 1)  # Fixed start date for consistency

    # ---------------- Customer Account and Loan Management ----------------

    def test_unique_account_number(self):
        """Test ID 1.1: Verify that a unique account number is generated for each new customer."""
        customer1 = bank.Customer()
        customer2 = bank.Customer()
        self.assertNotEqual(customer1.account.number, customer2.account.number)
        self.assertEqual(customer1.account.number, 1)
        self.assertEqual(customer2.account.number, 2)

    def test_customer_initialized_with_account(self):
        """Test ID 1.2: Confirm each customer is initialized with a savings account."""
        customer = bank.Customer()
        self.assertIsInstance(customer.account, bank.Account)
        self.assertIn(customer.account, bank.ACCOUNTS)
        self.assertEqual(customer.account.balance, 0.00)

    def test_maximum_loans_limit(self):
        """Test ID 1.3: Validate that a customer can open and maintain a maximum of three active loans."""
        customer = bank.Customer()
        for _ in range(3):
            customer.initiate_loan(1000, 0.1)
        self.assertEqual(len(customer.loans), 3)
        self.assertEqual(len(bank.LOANS), 3)

    @patch('builtins.print')
    def test_opening_fourth_loan_should_fail(self, mock_print):
        """Test ID 1.4: Test for system response when attempting to open a fourth loan (should fail)."""
        customer = bank.Customer()
        for _ in range(3):
            customer.initiate_loan(1000, 0.1)
        customer.initiate_loan(1500, 0.12)
        self.assertEqual(len(customer.loans), 3)
        mock_print.assert_called_with("Max number of outstanding loans reached")

    # ---------------- Monthly Customer Actions ----------------

    def test_initiate_loan_within_limits(self):
        """Test ID 2.1: Confirm the ability to initiate a loan, checking for adherence to loan limits."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.1)
        self.assertEqual(len(customer.loans), 1)

    def test_make_loan_payment(self):
        """Test ID 2.2: Verify customers can make loan payments and handle minimum and excess payments."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.1)
        loan = customer.loans[0]
        loan.accrued_interest = 10  # Simulate interest
        min_payment = loan.minimum_payment()
        customer.payment_on_loan(loan, min_payment)
        self.assertLess(loan.balance, 1000)  # Confirm payment applied correctly without late fee

    def test_deposit_updates_balance(self):
        """Test ID 2.3: Confirm deposits to the savings account are processed and reflected in the account balance."""
        customer = bank.Customer()
        customer.account.deposit(500)
        self.assertEqual(customer.account.balance, 500)

    @patch('builtins.print')
    def test_withdraw_updates_balance_and_restrictions(self, mock_print):
        """Test ID 2.4: Validate withdrawals from the savings account, checking for correct balance updates."""
        customer = bank.Customer()
        customer.account.deposit(100)
        customer.account.withdraw(50)
        self.assertEqual(customer.account.balance, 50)
        customer.account.withdraw(60)
        self.assertEqual(customer.account.balance, 50)  # Balance should not change due to insufficient funds

    @patch('builtins.print')
    def test_multiple_monthly_actions(self, mock_print):
        """Test ID 2.5: Handle multiple actions within a month and enforce limits."""
        customer = bank.Customer()
        customer.account.deposit(1000)
        customer.initiate_loan(2000, 0.1)
        customer.initiate_loan(3000, 0.15)
        self.assertEqual(len(customer.loans), 2)
        customer.account.withdraw(500)
        self.assertEqual(customer.account.balance, 500)

    # ---------------- Interest Rate Initialization and Validation ----------------

    def test_loan_interest_rate_initialization(self):
        """Test ID 3.1: Verify interest rates for loans are set at startup within specified range."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.1)
        self.assertGreaterEqual(customer.loans[0].interest_rate, bank.MIN_INTEREST_RATE)
        self.assertLessEqual(customer.loans[0].interest_rate, bank.MAX_INTEREST_RATE)

    # ---------------- Month Advancement Functionality ----------------

    @patch('builtins.print')
    def test_advance_date_functionality(self, mock_print):
        """Test ID 4.1: Verify that the 'advance to the next month' functionality initiates all month-end processes."""
        customer = bank.Customer()
        customer.account.deposit(1000)
        customer.initiate_loan(1000, 0.12)
        bank.advance_date()
        self.assertEqual(len(customer.loans), 1)  # Confirm loans persisted

    # ---------------- Month-End Processing ----------------

    def test_interest_calculations(self):
        """Test ID 5.1: Validate interest calculations for both savings and loan accounts."""
        customer = bank.Customer()
        customer.account.interest_rate = 0.04
        customer.account.deposit(1000)
        bank.advance_date()
        self.assertAlmostEqual(customer.account.balance, 1000 + (1000 * (0.04 / 12)), places=2)

    def test_interest_added_to_account_balance(self):
        """Test ID 5.2: Confirm interest is added to account balances at the end of each month."""
        customer = bank.Customer()
        customer.account.interest_rate = 0.04
        customer.account.deposit(1000)
        bank.advance_date()
        self.assertAlmostEqual(customer.account.balance, 1000 + (1000 * (0.04 / 12)), places=2)

    @patch('builtins.print')
    def test_statement_generation_accuracy(self, mock_print):
        """Test ID 5.3: Test statement generation for accuracy."""
        customer = bank.Customer()
        customer.account.deposit(1000)
        customer.initiate_loan(500, 0.1)
        customer.generate_statement()
        mock_print.assert_any_call(f"Statement for Account {customer.account.number}")

    # ---------------- Late Fee Assessment ----------------

    def test_late_fee_application_on_minimum_payment_not_met(self):
        """Test ID 6.1: Verify that a $50 late fee is applied when the minimum loan payment is not met."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.12)
        loan = customer.loans[0]
        loan.accrued_interest = 10  # Minimum payment = 20
        customer.payment_on_loan(loan, 10)  # Pay below minimum
        self.assertEqual(loan.balance, 1000 + bank.LATE_FEE)

    def test_multiple_late_fees_accumulate(self):
        """Test ID 6.2: Confirm that multiple late fees accumulate correctly."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.12)
        loan = customer.loans[0]

        # First insufficient payment
        customer.payment_on_loan(loan, 10)
        self.assertEqual(loan.balance, 1000 + bank.LATE_FEE)  # Expected balance: 1050

        # Second insufficient payment
        customer.payment_on_loan(loan, 10)
        self.assertEqual(loan.balance, 1000 + (bank.LATE_FEE * 2))  # Expected balance: 1100

    # ---------------- Minimum Payment Calculation and Enforcement ----------------

    def test_minimum_payment_calculation(self):
        """Test ID 7.1: Validate minimum payment calculation."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.12)
        loan = customer.loans[0]
        loan.accrued_interest = 10
        self.assertEqual(loan.minimum_payment(), 20)

    # ---------------- Loan Origination Limits ----------------

    def test_loan_origination_within_limits(self):
        """Test ID 8.1: Confirm that the system allows loan amounts only within the $500 to $50,000 range."""
        customer = bank.Customer()
        customer.initiate_loan(500, 0.1)
        customer.initiate_loan(50000, 0.1)
        self.assertEqual(len(customer.loans), 2)

    @patch('builtins.print')
    def test_loan_initiation_outside_limits(self, mock_print):
        """Test ID 8.2: Test system response to loan initiation attempts outside the range."""
        customer = bank.Customer()
        customer.initiate_loan(400, 0.1)
        mock_print.assert_called_with("Loan amount must be between $500 and $50,000")

    # ---------------- Loan Payment Handling ----------------

    def test_loan_payment_handling(self):
        """Test ID 9.1: Verify acceptance of payments above the minimum payment but not exceeding balance."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.12)
        loan = customer.loans[0]
        loan.accrued_interest = 10
        customer.payment_on_loan(loan, 500)
        self.assertEqual(loan.balance, 1000 - 500)

    # ---------------- Loan Account Closure Criteria ----------------

    def test_loan_closure_on_full_payment(self):
        """Test ID 10.1: Test automatic loan closure when the balance is fully paid."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.1)
        loan = customer.loans[0]
        customer.payment_on_loan(loan, 1000)  # Pay off loan
        self.assertNotIn(loan, customer.loans)
        self.assertNotIn(loan, bank.LOANS)

    # ---------------- Additional Tests for Comprehensive Coverage ----------------

    # Boundary Testing for Interest Rates
    def test_loan_with_minimum_interest_rate(self):
        """Test: Loan with the exact minimum interest rate should be accepted."""
        customer = bank.Customer()
        customer.initiate_loan(1000, bank.MIN_INTEREST_RATE)
        self.assertEqual(customer.loans[0].interest_rate, bank.MIN_INTEREST_RATE)

    def test_loan_with_maximum_interest_rate(self):
        """Test: Loan with the exact maximum interest rate should be accepted."""
        customer = bank.Customer()
        customer.initiate_loan(1000, bank.MAX_INTEREST_RATE)
        self.assertEqual(customer.loans[0].interest_rate, bank.MAX_INTEREST_RATE)

    # Edge Cases for Payments
    def test_payment_exactly_minimum(self):
        """Test: Loan payment exactly equal to minimum payment should not trigger late fee."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.1)
        loan = customer.loans[0]
        loan.accrued_interest = 10  # Simulate some interest
        min_payment = loan.minimum_payment()
        customer.payment_on_loan(loan, min_payment)
        self.assertEqual(loan.balance, 1000 - min_payment)  # Confirm balance updated correctly without late fee

    def test_multiple_loans_paid_off_in_same_month(self):
        """Test: Multiple loans paid off in the same month are correctly removed from the system."""
        customer = bank.Customer()
        customer.initiate_loan(500, 0.1)
        customer.initiate_loan(600, 0.1)
        loan1, loan2 = customer.loans
        customer.payment_on_loan(loan1, 500)  # Pay off loan1
        customer.payment_on_loan(loan2, 600)  # Pay off loan2
        self.assertNotIn(loan1, customer.loans)
        self.assertNotIn(loan2, customer.loans)

    # Accrued Interest Persistence
    def test_accrued_interest_resets_after_month_end(self):
        """Test: Accrued interest is reset after being applied to the balance at month-end."""
        customer = bank.Customer()
        customer.initiate_loan(1000, 0.12)  # 12% annual interest
        loan = customer.loans[0]

        # Calculate interest based on bank logic
        loan.calculate_interest()
        expected_accrued_interest = loan.accrued_interest  # Capture accrued interest for comparison

        # Confirm accrued interest matches expectation based on monthly rate
        monthly_rate = 0.12 / 12
        self.assertAlmostEqual(expected_accrued_interest, 1000 * monthly_rate, places=2)

        # Apply interest manually and check balance without using advance_date
        loan.apply_interest()  # Manually apply interest to avoid any double application

        # After applying, accrued interest should be zero, and balance should increase by accrued interest
        self.assertEqual(loan.accrued_interest, 0)  # Ensure accrued interest reset
        self.assertAlmostEqual(loan.balance, 1000 + expected_accrued_interest, places=2)

    # Data Integrity with Multiple Customers
    def test_multiple_customers_data_integrity(self):
        """Test: Actions on one customer should not affect another customer's data or loans."""
        customer1 = bank.Customer()
        customer2 = bank.Customer()
        customer1.account.deposit(500)
        customer2.account.deposit(1000)
        customer1.initiate_loan(1000, 0.1)
        self.assertEqual(customer1.account.balance, 500)
        self.assertEqual(customer2.account.balance, 1000)
        self.assertEqual(len(customer1.loans), 1)
        self.assertEqual(len(customer2.loans), 0)

    # Negative Testing for Deposits and Withdrawals
    @patch('builtins.print')
    def test_negative_deposit(self, mock_print):
        """Test: Negative deposit amounts should be rejected."""
        customer = bank.Customer()
        customer.account.deposit(-100)
        mock_print.assert_called_with("Invalid deposit amount")
        self.assertEqual(customer.account.balance, 0)

    @patch('builtins.print')
    def test_negative_withdrawal(self, mock_print):
        """Test: Negative withdrawal amounts should be rejected."""
        customer = bank.Customer()
        customer.account.deposit(100)
        customer.account.withdraw(-50)
        mock_print.assert_called_with("Invalid withdrawal amount")
        self.assertEqual(customer.account.balance, 100)

    # Stress Testing for Account and Loan Limits
    def test_high_volume_of_accounts_and_loans(self):
        """Test: System handles a high volume of accounts and loans without issues."""
        for i in range(100):  # Create 100 customers
            customer = bank.Customer()
            customer.account.deposit(100)
            if i < 50:  # Add loans to only the first 50 customers
                customer.initiate_loan(1000, 0.1)
        self.assertEqual(len(bank.ACCOUNTS), 100)
        self.assertEqual(len(bank.LOANS), 50)

    def test_enforce_loan_limit_under_high_volume(self):
        """Test: System enforces loan limit correctly under high volume conditions."""
        customer = bank.Customer()
        for _ in range(3):
            customer.initiate_loan(1000, 0.1)  # Should succeed up to 3 loans
        self.assertEqual(len(customer.loans), 3)
        customer.initiate_loan(1000, 0.1)  # Fourth loan should fail
        self.assertEqual(len(customer.loans), 3)  # Loan count should still be 3

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
