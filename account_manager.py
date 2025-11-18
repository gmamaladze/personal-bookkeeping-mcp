"""
Account Manager - CRUD interface for GnuCash-style account hierarchy
"""
import pandas as pd
import random
import string
from typing import Optional, List, Dict, Any
from enum import Enum


class AccountType(Enum):
    """
    Account types for double-entry bookkeeping.
    
    Based on GnuCash account hierarchy:
    - ASSET: Resources owned (Aktiva)
    - LIABILITY: Debts and obligations (Fremdkapital)
    - EQUITY: Owner's equity (Eigenkapital)
    - INCOME: Revenue and earnings (Erträge)
    - EXPENSE: Costs and expenditures (Aufwendungen)
    - CASH: Physical cash accounts (Bargeld)
    - BANK: Bank accounts (Girokonto, Sparkonto)
    - CREDIT: Credit card accounts (Kreditkarte)
    """
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    CASH = "CASH"
    BANK = "BANK"
    CREDIT = "CREDIT"
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a string is a valid account type."""
        return value in cls._value2member_map_
    
    @classmethod
    def get_all_values(cls) -> List[str]:
        """Get list of all account type values."""
        return [member.value for member in cls]


class AccountManager:
    """
    Manages account hierarchy using pandas DataFrame.
    Provides CRUD operations for double-entry bookkeeping accounts.
    """
    
    # Required column names
    REQUIRED_COLUMNS = [
        'account_key',       # Unique immutable 5-letter ID
        'parent_key',        # Parent account key (empty for root accounts)
        'type',              # Account type (Typ)
        'name',              # Account name (Kontobezeichnung)
        'full_name',         # Full hierarchical name (Volle Kontobezeichnung)
        'account_number',    # Account number (Kontonummer)
        'currency',          # Currency symbol (Symbol/Währung)
        'hidden'             # Hidden flag (Versteckt)
    ]
    
    # Optional columns
    OPTIONAL_COLUMNS = [
        'description',       # Description (Beschreibung)
        'color',             # Account color (Kontofarbe)
        'notes',             # Notes (Bemerkungen)
        'namespace',         # Namespace (Namensraum)
        'tax_relevant',      # Tax relevant (Steuerrelevante Information)
        'placeholder'        # Placeholder account (Platzhalter)
    ]
    
    def __init__(self):
        self._df = pd.DataFrame(columns=self.REQUIRED_COLUMNS + self.OPTIONAL_COLUMNS)
    
    def _generate_account_key(self) -> str:
        """Generate a unique 5-letter account key."""
        while True:
            key = ''.join(random.choices(string.ascii_uppercase, k=5))
            if 'account_key' not in self._df.columns or key not in self._df['account_key'].values:
                return key
    
    def create_account(self, 
                      account_type: str,
                      name: str,
                      full_name: str,
                      parent_key: str = "",
                      account_number: str = "",
                      currency: str = "EUR",
                      hidden: bool = False,
                      **optional_fields) -> str:
        """
        Create a new account.
        
        Args:
            account_type: Account type (ASSET, LIABILITY, EQUITY, INCOME, EXPENSE, etc.)
            name: Account name
            full_name: Full hierarchical name (e.g., "Assets:Cash:Checking")
            parent_key: Parent account key (empty for root accounts)
            account_number: Account number (optional)
            currency: Currency symbol (default: EUR)
            hidden: Whether account is hidden (default: False)
            **optional_fields: Additional optional fields (description, color, etc.)
        
        Returns:
            The newly created account's unique key
        """
        # Validate account type
        if not AccountType.is_valid(account_type):
            valid_types = ', '.join(AccountType.get_all_values())
            raise ValueError(f"Invalid account type: {account_type}. Valid types: {valid_types}")
        
        # Validate parent_key if provided
        if parent_key and 'account_key' in self._df.columns:
            if parent_key not in self._df['account_key'].values:
                raise ValueError(f"Parent account key '{parent_key}' does not exist")
        
        # Generate unique account key
        account_key = self._generate_account_key()
        
        # Create new account data
        new_account = {
            'account_key': account_key,
            'parent_key': parent_key,
            'type': account_type,
            'name': name,
            'full_name': full_name,
            'account_number': account_number,
            'currency': currency,
            'hidden': hidden
        }
        
        # Add optional fields
        for field in self.OPTIONAL_COLUMNS:
            if field in optional_fields:
                new_account[field] = optional_fields[field]
        
        # Append to dataframe
        new_df = pd.DataFrame([new_account])
        self._df = pd.concat([self._df, new_df], ignore_index=True)
        
        return account_key
        
    def get_account_by_key(self, account_key: str) -> Optional[pd.Series]:
        """
        Get account by its unique key.
        
        Args:
            account_key: The account's unique key
        
        Returns:
            Account as Series or None if not found
        """
        if 'account_key' not in self._df.columns:
            return None
        
        result = self._df[self._df['account_key'] == account_key]
        if len(result) > 0:
            return result.iloc[0]
        return None
    
    def get_children(self, parent_key: str) -> pd.DataFrame:
        """
        Get all direct children of an account.
        
        Args:
            parent_key: The parent account's key
        
        Returns:
            DataFrame with child accounts
        """
        if 'parent_key' not in self._df.columns:
            return pd.DataFrame()
        
        return self._df[self._df['parent_key'] == parent_key].copy()
    
    def get_root_accounts(self) -> pd.DataFrame:
        """
        Get all root-level accounts (accounts with no parent).
        
        Returns:
            DataFrame with root accounts
        """
        if 'parent_key' not in self._df.columns:
            return pd.DataFrame()
        
        return self._df[self._df['parent_key'] == ''].copy()
    
    def get_account_path(self, account_key: str) -> List[str]:
        """
        Get the full path from root to this account as list of account keys.
        
        Args:
            account_key: The account's unique key
        
        Returns:
            List of account keys from root to the specified account
        """
        path = []
        current_key = account_key
        
        # Prevent infinite loops
        max_depth = 100
        depth = 0
        
        while current_key and depth < max_depth:
            account = self.get_account_by_key(current_key)
            if account is None:
                break
            
            path.insert(0, current_key)
            current_key = account.get('parent_key', '')
            depth += 1
        
        return path
    
    def get_all_accounts(self) -> pd.DataFrame:
        """
        Get all accounts.
        
        Returns:
            DataFrame with all accounts
        """
        return self._df.copy()
    
