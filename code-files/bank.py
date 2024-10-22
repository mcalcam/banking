from datetime import date
from dateutil.relativedelta import relativedelta

ACCOUNTS = []
LOANS = []
CUSTOMERS = []
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
    
    def calculate_interest(self):
        pass

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
        self.number = len(CUSTOMERS) + 1
        self.account = Account()
        self.loans = []
        CUSTOMERS.append(self)

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

def execute_option(option,customer):
    if option == 1:
        advance_date()
    elif option == 2:
        customer.account.current_balance()
    elif option == 3:
        amount = int(input('Deposit amount: '))
        customer.account.deposit(amount)
    elif option == 4:
        amount = int(input('Withdraw amount: '))
        customer.account.withdraw(amount)



def main():
    user_input = ''
    customer = Customer()
    while True:
        print_options()
        user_input = input('Select an option: ')
        if user_input == 'q':
            return
        else:
            print()
            execute_option(int(user_input),customer)

if __name__=="__main__":
    main()
