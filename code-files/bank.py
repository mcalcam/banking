from datetime import date
from dateutil.relativedelta import relativedelta

# Constants
MIN_LOAN_AMOUNT = 500
MAX_LOAN_AMOUNT = 50000
MIN_INTEREST_RATE = 0.06
MAX_INTEREST_RATE = 0.18
LATE_FEE = 50
MIN_PAYMENT = 10

ACCOUNTS = []
LOANS = []
CUSTOMER = None
CURRENT_DATE = date.today()

class Loan:
    def __init__(self, principal):
        self.number = len(LOANS) + 1
        self.principal = principal
        self.open_date = CURRENT_DATE
        # self.rate
        # self.accrued_interest
        # self.balance

        LOANS.append(self)

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

    def make_payment(self, amount):
        if amount < self.minimum_payment():
            self.balance += LATE_FEE
        else:
            self.balance -= amount
            if self.balance <= 0:
                LOANS.remove(self)

    def minimum_payment(self):
        interest_due = self.accrued_interestpoint
        principal_payment = max(self.principal * 0.01, MIN_PAYMENT)
        return interest_due + principal_payment

class Account:
    def __init__(self):
        self.number = len(ACCOUNTS) + 1
        self.balance = 0.00
        self.open_date = CURRENT_DATE
        ACCOUNTS.append(self)

    def current_balance(self):
        print(f'Current Balance: ${self.balance:.2f}')
        print()

    def deposit(self, amount):
        self.balance += amount
        self.current_balance()
        print()

    def withdraw(self, amount):
        if amount > self.balance:
            print('Insufficient Funds')
            self.current_balance()
            print()
        else:
            self.balance -= amount
            self.current_balance()
            print()

class Customer: 
    def __init__(self):
        self.account = Account()
        self.loans = []

    def initiate_loan(self): 
        if len(self.loans) == 3:
            print("Max number of outstanding loans reached")
        else:
            self.loans.append(Loan)

    def payment_on_loan(self):
        pass

def advance_date():
    global CURRENT_DATE
    CURRENT_DATE = CURRENT_DATE + relativedelta(months=1)
    print()
    print('Date advanced')

def print_options():
    print(f'Today: {CURRENT_DATE.strftime("%A %d. %B %Y")}')
    print('1: Advance to the next month')
    print('2: Check balance')
    print('3: Deposit to savings')
    print('4: Withdraw from savings')
    print()

def execute_option(option,CUSTOMER):
    if option == 1:
        advance_date()
    elif option == 2:
        CUSTOMER.account.current_balance()
    elif option == 3:
        amount = int(input('Deposit amount: '))
        CUSTOMER.account.deposit(amount)
    elif option == 4:
        amount = int(input('Withdraw amount: '))
        CUSTOMER.account.withdraw(amount)

def main():
    
    user_input = ''
    CUSTOMER = Customer()
    while True:
        print_options()
        user_input = input('Select an option: ')
        if user_input == 'q':
            return
        else:
            print()
            execute_option(int(user_input),CUSTOMER)

if __name__=="__main__":
    main()
