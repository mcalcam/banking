from datetime import datetime, timedelta
import re

# Constants
MIN_LOAN_AMOUNT = 500
MAX_LOAN_AMOUNT = 50000
MIN_INTEREST_RATE = 0.06
MAX_INTEREST_RATE = 0.18
LATE_FEE = 50
MIN_PAYMENT = 10

# Global Variables
CURRENT_DATE = datetime.now()
ACCOUNTS = []
LOANS = []
CUSTOMERS = []

class Loan:
    def __init__(self, principal, interest_rate):
        self.principal = principal
        self.interest_rate = interest_rate
        self.balance = principal
        self.accrued_interest = 0
        self.last_payment_date = CURRENT_DATE
        LOANS.append(self)
    
    def calculate_interest(self):
        monthly_rate = self.interest_rate / 12
        self.accrued_interest += self.balance * monthly_rate

    def apply_interest(self):
        self.balance += self.accrued_interest
        self.accrued_interest = 0

    def make_payment(self, amount):
        if amount < self.minimum_payment():
            # Only add the late fee; do not deduct the insufficient payment amount
            self.balance += LATE_FEE
        else:
            # Deduct the payment amount if it meets or exceeds the minimum payment
            self.balance -= amount
            if self.balance <= 0:
                LOANS.remove(self)

    def minimum_payment(self):
        interest_due = self.accrued_interest
        principal_payment = max(self.principal * 0.01, MIN_PAYMENT)
        return interest_due + principal_payment

class Account:
    def __init__(self):
        self.number = len(ACCOUNTS) + 1
        self.balance = 0.00
        self.open_date = CURRENT_DATE
        self.interest_rate = 0
        ACCOUNTS.append(self)

    def current_balance(self):
        print(f'Current Balance: ${self.balance:.2f}')
        print()

    def deposit(self, amount):
        if amount < 0:
            print("Invalid deposit amount")
            return
        self.balance += amount
        self.current_balance()

    def withdraw(self, amount):
        if amount < 0:
            print("Invalid withdrawal amount")
            return
        if amount > self.balance:
            print("Insufficient Funds")
        else:
            self.balance -= amount
        self.current_balance()

    def calculate_interest(self):
        monthly_rate = self.interest_rate / 12
        interest = self.balance * monthly_rate
        self.balance += interest

class Customer: 
    def __init__(self):
        self.account = Account()
        self.loans = []

    def initiate_loan(self, principal, interest_rate): 
        if len(self.loans) == 3:
            print("Max number of outstanding loans reached")
        elif principal < MIN_LOAN_AMOUNT or principal > MAX_LOAN_AMOUNT:
            print("Loan amount must be between $500 and $50,000")
        elif interest_rate < MIN_INTEREST_RATE or interest_rate > MAX_INTEREST_RATE:
            print("Interest rate must be between 6% and 18%")
        else:
            loan = Loan(principal, interest_rate)
            self.loans.append(loan)

    def payment_on_loan(self, loan, amount):
        if loan in self.loans:
            loan.make_payment(amount)
            if loan.balance == 0: # Remove loan if fully paid.
                self.loans.remove(loan)

    def generate_statement(self):
        print(f"Statement for Account {self.account.number}")
        print(f"Beginning Balance: ${self.account.balance:.2f}")
        for loan in self.loans:
            print(f"Loan Balance: ${loan.balance:.2f}")
        print(f"Ending Balance: ${self.account.balance:.2f}")
        print()

    def current_balance(self):
        self.account.current_balance()
        for i, loan in enumerate(self.loans, start=1):
            print(f'Loan {i} Balance: ${loan.balance:.2f}')
        print()

def advance_date():
    global CURRENT_DATE
    CURRENT_DATE += timedelta(days=30)
    for account in ACCOUNTS:
        account.calculate_interest()
    for loan in LOANS:
        loan.calculate_interest()
        loan.apply_interest()
    for customer in CUSTOMERS:
        customer.generate_statement()

def print_options():
    print(f'Today: {CURRENT_DATE.strftime("%A %d. %B %Y")}')
    print('1: Advance to the next month')
    print('2: Check balance')
    print('3: Deposit to savings')
    print('4: Withdraw from savings')
    print('5: Initiate a loan')
    print('6: Make a payment on a loan')
    print()

# Returns true if the value is a positive int
def is_valid_int(amount) -> bool:
    return amount.isdigit() and int(amount) >= 0

# Returns true if the value is a positive decimal
def is_valid_dec(amount) -> bool:
    try:
        return float(amount) >= 0
    except ValueError:
        return False

def execute_option(option, CUSTOMER):
    if option == 1:
        advance_date()
    elif option == 2:
        CUSTOMER.current_balance()
    elif option == 3:
        user_input = input('Deposit amount: ')
        if is_valid_int(user_input):
            amount = int(user_input)
            CUSTOMER.account.deposit(amount)
        else:
            print('\nInvalid deposit amount\n')
    elif option == 4:
        user_input = input('Withdraw amount: ')
        if is_valid_int(user_input):
            amount = int(user_input)
            CUSTOMER.account.withdraw(amount)
        else:
            print('\nInvalid deposit amount\n')
    elif option == 5:
        principal = input('Loan principal amount: ')
        if is_valid_int(principal):
            principal = int(principal)
        else:
            print('\nInvalid principal value\n')
            return
                        
        interest_rate = input('Loan interest rate (as a decimal): ')
        if is_valid_dec(interest_rate):
            interest_rate = float(interest_rate)
        else:
            print('\nInvalid loan interest rate value\n')
            return
        
        CUSTOMER.initiate_loan(principal, interest_rate)
    elif option == 6:
        loan_number = input('Loan number: ')
        if is_valid_int(loan_number):
            loan_number = int(loan_number)
        else:
            print('\nInvalid loan number')
            return
        
        amount = input('Payment amount: ')
        if is_valid_int(amount):
            amount = int(amount)
        else:
            print('\nInvalid payment amount')
            return
        if 0 < loan_number <= len(CUSTOMER.loans):
            CUSTOMER.payment_on_loan(CUSTOMER.loans[loan_number - 1], amount)
        else:
            print('Invalid loan number')
    else:
        print('Invalid Input\n')

def main():
    user_input = ''
    CUSTOMER = Customer()
    CUSTOMERS.append(CUSTOMER)
    while True:
        print_options()
        user_input = input('Select an option: ')
        if user_input == 'q':
            return
        elif re.search(r'\D', user_input):
            print('\nInvalid Input\n')
        else:
            print()
            execute_option(int(user_input), CUSTOMER)

if __name__ == "__main__":
    main()