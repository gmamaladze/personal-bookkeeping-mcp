"""
Example usage of AccountManager class
"""
from account_manager import AccountManager, AccountType


def main():
    # Example 1: Load from existing CSV file
    print("=" * 60)
    print("Example 1: Loading from CSV")
    print("=" * 60)
    
    # Load the German CSV file
    manager = AccountManager(r"c:\Users\gmama\OneDrive\Desktop\Konten")
    
    print(f"Total accounts loaded: {manager.count_accounts(include_hidden=True)}")
    print(f"Visible accounts: {manager.count_accounts(include_hidden=False)}")
    
    # Example 2: Get all ASSET accounts
    print("\n" + "=" * 60)
    print("Example 2: Get all ASSET accounts")
    print("=" * 60)
    
    assets = manager.get_accounts_by_type(AccountType.ASSET.value)
    print(f"\nFound {len(assets)} asset accounts:")
    for _, account in assets.head(5).iterrows():
        print(f"  - {account['name']} ({account['currency']})")
    
    # Example 3: Search for specific account
    print("\n" + "=" * 60)
    print("Example 3: Search for 'Girokonto'")
    print("=" * 60)
    
    account = manager.get_account_by_name("Girokonto")
    if account is not None:
        print(f"Found account: {account['name']}")
        print(f"  Type: {account['type']}")
        print(f"  Currency: {account['currency']}")
        print(f"  Full name: {account.get('full_name', 'N/A')}")
    
    # Example 4: Create a new account
    print("\n" + "=" * 60)
    print("Example 4: Create new account")
    print("=" * 60)
    
    new_manager = AccountManager()
    
    index = new_manager.create_account(
        account_type=AccountType.BANK.value,
        name="Checking Account",
        account_number="12345678",
        currency="EUR",
        hidden=False,
        full_name="Assets:Cash:Checking Account",
        description="Main checking account",
        placeholder=False
    )
    
    print(f"Created new account at index {index}")
    print(f"Total accounts: {new_manager.count_accounts()}")
    
    # Example 5: Update account
    print("\n" + "=" * 60)
    print("Example 5: Update account")
    print("=" * 60)
    
    success = new_manager.update_account(
        "Checking Account",
        description="Updated main checking account",
        account_number="87654321"
    )
    
    print(f"Update successful: {success}")
    
    updated_account = new_manager.get_account_by_name("Checking Account")
    print(f"Updated description: {updated_account['description']}")
    print(f"Updated account number: {updated_account['account_number']}")
    
    # Example 6: Get account hierarchy
    print("\n" + "=" * 60)
    print("Example 6: Account hierarchy (first level)")
    print("=" * 60)
    
    hierarchy = manager.get_account_hierarchy()
    print(f"Root level accounts: {len(hierarchy)}")
    for account in hierarchy[:3]:  # Show first 3
        print(f"  - {account.get('full_name', account['name'])}")
        print(f"    Children: {len(account['children'])}")
    
    # Example 7: Search accounts
    print("\n" + "=" * 60)
    print("Example 7: Search for 'Gehalt'")
    print("=" * 60)
    
    results = manager.search_accounts("Gehalt")
    print(f"Found {len(results)} accounts:")
    for _, account in results.iterrows():
        print(f"  - {account['name']} ({account['type']})")
    
    # Example 8: Get accounts by type
    print("\n" + "=" * 60)
    print("Example 8: All INCOME accounts")
    print("=" * 60)
    
    income_accounts = manager.get_accounts_by_type(AccountType.INCOME.value)
    print(f"Found {len(income_accounts)} income accounts:")
    for _, account in income_accounts.head(5).iterrows():
        print(f"  - {account.get('full_name', account['name'])}")
    
    # Example 9: Delete account
    print("\n" + "=" * 60)
    print("Example 9: Delete account")
    print("=" * 60)
    
    success = new_manager.delete_account("Checking Account")
    print(f"Delete successful: {success}")
    print(f"Total accounts remaining: {new_manager.count_accounts()}")
    
    # Example 10: Save to CSV
    print("\n" + "=" * 60)
    print("Example 10: Save accounts to CSV")
    print("=" * 60)
    
    # Create a few accounts
    test_manager = AccountManager()
    test_manager.create_account(
        account_type=AccountType.ASSET.value,
        name="Cash",
        currency="EUR",
        hidden=False,
        full_name="Assets:Cash",
        description="Cash on hand"
    )
    test_manager.create_account(
        account_type=AccountType.EXPENSE.value,
        name="Groceries",
        currency="EUR",
        hidden=False,
        full_name="Expenses:Groceries",
        description="Grocery expenses"
    )
    
    # Save in English format
    test_manager.save_to_csv("test_accounts_en.csv", german_format=False)
    print("Saved to test_accounts_en.csv (English format)")
    
    # Save in German format
    test_manager.save_to_csv("test_accounts_de.csv", german_format=True)
    print("Saved to test_accounts_de.csv (German format)")


if __name__ == "__main__":
    main()
