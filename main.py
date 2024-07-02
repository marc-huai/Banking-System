def main():
    """Main function to run the banking system from the command line."""
    bank = BankSystem()
    
    while True:
        print("\nWelcome to the Bank System")
        print("1. Add Customer")
        print("2. Create Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            address = input("Enter address: ")
            bank.add_customer(first_name, last_name, address)
            print("Customer added successfully!")

        elif choice == '2':
            # Assuming customers are listed for simplicity
            print("Select customer by index:")
            for idx, customer in enumerate(bank.customers):
                print(f"{idx}: {customer.first_name} {customer.last_name}")
            customer_idx = int(input("Enter customer index: "))
            account_type = input("Enter account type (checking/savings): ")
            initial_balance = float(input("Enter initial balance: "))
            bank.create_account(bank.customers[customer_idx], account_type, initial_balance)
            print("Account created successfully!")

        elif choice == '3':
            # Similar to account creation, handling deposit
            pass

        elif choice == '4':
            # Similar to account creation, handling withdraw
            pass

        elif choice == '5':
            # Similar to account creation, handling balance check
            pass

        elif choice == '6':
            break

if __name__ == "__main__":
    main()
