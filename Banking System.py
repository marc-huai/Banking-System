import json
import uuid

class Customer:
    """Represents a customer in the banking system.

    Attributes:
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        address (str): The address of the customer.
        accounts (list): A list of accounts associated with the customer.
    """

    def __init__(self, first_name, last_name, address):
        """
        Initializes a new Customer instance.

        Args:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            address (str): The address of the customer.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.accounts = []

    @log_function_call
    def add_account(self, account):
        """
        Adds an account to the customer's list of accounts.

        Args:
            account (Account): The account to add.
        """
        self.accounts.append(account)


class Account:
    """Represents a bank account.

    Attributes:
        account_type (str): The type of the account (checking/savings).
        balance (float): The balance of the account.
        account_number (str): The unique account number.
    """

    def __init__(self, account_type, initial_balance=0):
        """
        Initializes a new Account instance.

        Args:
            account_type (str): The type of the account (checking/savings).
            initial_balance (float, optional): The initial balance of the account. Defaults to 0.
        """
        self.account_type = account_type
        self.balance = initial_balance
        self.account_number = str(uuid.uuid4())

    @log_function_call
    @handle_transaction
    def deposit(self, amount):
        """
        Deposits an amount into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if the deposit was successful, False otherwise.
        """
        if amount > 0:
            self.balance += amount
            return True
        return False

    @log_function_call
    @handle_transaction
    def withdraw(self, amount):
        """
        Withdraws an amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if the withdrawal was successful, False otherwise.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    @log_function_call
    def get_balance(self):
        """
        Gets the balance of the account.

        Returns:
            float: The current balance of the account.
        """
        return self.balance


class Employee:
    """Represents an employee of the bank.

    Attributes:
        first_name (str): The first name of the employee.
        last_name (str): The last name of the employee.
        employee_id (str): The unique ID of the employee.
        position (str): The position of the employee.
    """

    def __init__(self, first_name, last_name, employee_id, position):
        """
        Initializes a new Employee instance.

        Args:
            first_name (str): The first name of the employee.
            last_name (str): The last name of the employee.
            employee_id (str): The unique ID of the employee.
            position (str): The position of the employee.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.employee_id = employee_id
        self.position = position

    @log_function_call
    @authorize_employee
    def approve_loan(self, customer, loan_amount, interest_rate):
        """
        Approves a loan for a customer.

        Args:
            customer (Customer): The customer requesting the loan.
            loan_amount (float): The amount of the loan.
            interest_rate (float): The interest rate of the loan.

        Returns:
            Loan: The approved loan.
        """
        loan = Loan(customer, loan_amount, interest_rate)
        return loan

    @log_function_call
    @authorize_employee
    def issue_credit_card(self, customer, credit_limit):
        """
        Issues a credit card to a customer.

        Args:
            customer (Customer): The customer requesting the credit card.
            credit_limit (float): The credit limit of the credit card.

        Returns:
            CreditCard: The issued credit card.
        """
        credit_card = CreditCard(customer, credit_limit)
        return credit_card


class Service:
    """Represents a service provided by the bank.

    Attributes:
        service_type (str): The type of the service.
        customer (Customer): The customer associated with the service.
    """

    def __init__(self, service_type, customer):
        """
        Initializes a new Service instance.

        Args:
            service_type (str): The type of the service.
            customer (Customer): The customer associated with the service.
        """
        self.service_type = service_type
        self.customer = customer


class Loan(Service):
    """Represents a loan service provided by the bank.

    Attributes:
        loan_amount (float): The amount of the loan.
        interest_rate (float): The interest rate of the loan.
    """

    def __init__(self, customer, loan_amount, interest_rate):
        """
        Initializes a new Loan instance.

        Args:
            customer (Customer): The customer taking the loan.
            loan_amount (float): The amount of the loan.
            interest_rate (float): The interest rate of the loan.
        """
        super().__init__('Loan', customer)
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate


class CreditCard(Service):
    """Represents a credit card service provided by the bank.

    Attributes:
        credit_limit (float): The credit limit of the credit card.
    """

    def __init__(self, customer, credit_limit):
        """
        Initializes a new CreditCard instance.

        Args:
            customer (Customer): The customer receiving the credit card.
            credit_limit (float): The credit limit of the credit card.
        """
        super().__init__('Credit Card', customer)
        self.credit_limit = credit_limit


class BankSystem:
    """Represents the banking system.

    Attributes:
        customers (list): A list of customers in the bank.
        employees (list): A list of employees in the bank.
        data_file (str): The file path for data storage.
    """

    def __init__(self, data_file='bank_data.json'):
        """
        Initializes a new BankSystem instance and loads data from the specified file.

        Args:
            data_file (str, optional): The file path for data storage. Defaults to 'bank_data.json'.
        """
        self.customers = []
        self.employees = []
        self.load_data(data_file)
        self.data_file = data_file

    @log_function_call
    def load_data(self, data_file):
        """
        Loads data from a JSON file.

        Args:
            data_file (str): The file path for data storage.
        """
        try:
            with open(data_file, 'r') as file:
                data = json.load(file)
                self.customers = [Customer(**cust) for cust in data['customers']]
                self.employees = [Employee(**emp) for emp in data['employees']]
        except FileNotFoundError:
            self.customers = []
            self.employees = []

    @log_function_call
    def save_data(self):
        """
        Saves the current data to a JSON file.
        """
        data = {
            'customers': [cust.__dict__ for cust in self.customers],
            'employees': [emp.__dict__ for emp in self.employees]
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    @log_function_call
    def add_customer(self, first_name, last_name, address):
        """
        Adds a new customer to the bank.

        Args:
            first_name (str): The first name of the customer.
