import datetime

ACCOUNTS = []
LOANS = []
CUSTOMERS = []
CURREN_DATE = datetime.date.today()

class Loan:
    def __init__(self, principal):
        self.number = len(LOANS) + 1
        self.principal = principal
        # self.rate
        # self.accrued_interest
        # self.balance

        LOANS.append(self)

class Account:
    def __init__(self):
        self.number = len(ACCOUNTS) + 1
        self.balance = 0.00
        ACCOUNTS.append(self)

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

    def deposit(self):
        pass

    def withdraw(self):
        pass

def main():
    user_input = ''
    while user_input != 'q':
        
        user_input = input('Select an option: ')

if __name__=="__main__":
    main()
