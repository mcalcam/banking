# Testing Plan for Cha-Ching Credit Union

## Overview

This testing plan outlines the strategy and scope of testing activities to ensure the bank loan management system meets its requirements and quality standards. This plan will guide the testing to be completed in future milestones, using both white box and black box testing methods.

## Scope

The scope of this testing plan includes verification of the following:

- Customer account management, including account creation, savings, and loan account handling.
- Monthly customer actions such as loan initiation, loan payment, deposits, and withdrawals.
- Interest rate management for loans and savings.
- End-of-month processing, including interest calculations, statements, and late fees.
- Loan payment enforcement, including minimum payment requirements and loan closure.

## Strategy

### Testing Types

1. **White Box Testing**: Analyze internal logic and structure of the code, focusing on control flow, data flow, and boundary conditions for complex operations like interest calculations and loan limit enforcement.
2. **Black Box Testing**: Validate the external behavior of the system based on specifications, without knowledge of the code. This will involve functional testing of requirements such as account creation, loan management, and monthly actions.
3. **Boundary Testing**: Test edge cases, such as maximum loan limits, interest rate boundaries, and minimum payments.
4. **Negative Testing**: Validate system responses to invalid inputs or actions, like exceeding loan limits.

### Test Data

- Generate customer data with varied loan and savings balances.
- Configure loan interest rates at minimum, maximum, and incremental levels.
- Set up delinquent accounts to test late fee application and minimum payment adjustments.

### Resources

- **Personnel**: Test engineers familiar with financial software testing.
- **Tools**:
  - Test automation tools for functional tests and regression tests, if needed.
  - Reporting tools for documentation and tracking of test progress.

## Risks

1. **Complex Interest Calculations**: Interest calculations on loans and savings may lead to errors if not thoroughly tested, especially at varying interest rates.
2. **Late Fees and Minimum Payment Accuracy**: Incorrect minimum payment or late fee calculations can lead to customer dissatisfaction and financial inconsistencies.
3. **Data Integrity**: Handling multiple accounts and transactions requires careful validation to ensure data integrity and accuracy.
4. **Automation Limitations**: Limited automation might reduce coverage in repetitive tests, risking overlooked errors in month-end processes.

---

## Test Cases

### 1. Customer Account and Loan Management

- **Test ID 1.1**: Verify that a unique account number is generated for each new customer.
- **Test ID 1.2**: Confirm each customer is initialized with a savings account.
- **Test ID 1.3**: Validate that a customer can open and maintain a maximum of three active loans.
- **Test ID 1.4**: Test for system response when attempting to open a fourth loan (should fail).

### 2. Monthly Customer Actions

- **Test ID 2.1**: Confirm the ability to initiate a loan, checking for adherence to loan limits.
- **Test ID 2.2**: Verify customers can make loan payments, and test the system’s handling of both minimum and excess payments.
- **Test ID 2.3**: Confirm deposits to the savings account are processed and reflected in the account balance.
- **Test ID 2.4**: Validate withdrawals from the savings account, checking for correct balance updates and any necessary restrictions.
- **Test ID 2.5**: Test the handling of multiple actions (a-d) within a month and the enforcement of any limits on these actions.

### 3. Interest Rate Initialization and Validation

- **Test ID 3.1**: Verify interest rates for loans are set at startup, ensuring they fall within the 6% to 18% range and are in increments of 0.25%.
- **Test ID 3.2**: Confirm the savings account interest rate is automatically calculated as one-fourth of the loan rate.

### 4. Month Advancement Functionality

- **Test ID 4.1**: Verify that the "advance to the next month" functionality initiates all month-end processes correctly.

### 5. Month-End Processing

- **Test ID 5.1**: Validate interest calculations for both savings and loan accounts, ensuring correct interest application based on rates and account balances.
- **Test ID 5.2**: Confirm interest is added to account balances at the end of each month.
- **Test ID 5.3**: Test statement generation for accuracy, ensuring it reflects beginning balances, account activities, applied interest, and ending balances.

### 6. Late Fee Assessment

- **Test ID 6.1**: Verify that a $50 late fee is applied when the minimum loan payment is not met.
- **Test ID 6.2**: Confirm that multiple late fees accumulate correctly in the loan balance for consecutive missed payments.

### 7. Minimum Payment Calculation and Enforcement

- **Test ID 7.1**: Validate minimum payment calculation as the greater of (interest due + 1% principal) or $10.
- **Test ID 7.2**: Verify that the minimum payment increases by $50 if the loan is delinquent from the previous month.

### 8. Loan Origination Limits

- **Test ID 8.1**: Confirm that the system allows loan amounts only within the $500 to $50,000 range.
- **Test ID 8.2**: Test system response to loan initiation attempts outside this range.

### 9. Loan Payment Handling

- **Test ID 9.1**: Verify acceptance of payments above the minimum payment but not exceeding the loan balance.

### 10. Loan Account Closure Criteria

- **Test ID 10.1**: Test automatic loan closure when the balance is fully paid and decide if it should be immediate or processed at month-end.
