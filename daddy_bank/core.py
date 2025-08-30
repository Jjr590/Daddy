"""
Core banking functionality for Daddy Bank
"""
from datetime import datetime
from typing import Dict, List, Optional
import uuid


class BankAccount:
    """Represents a bank account"""
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions: List[Dict] = []
        self.created_at = datetime.now()
    
    def deposit(self, amount: float, description: str = "Deposit") -> bool:
        """Deposit money into account"""
        if amount <= 0:
            return False
        
        self.balance += amount
        self._add_transaction("DEPOSIT", amount, description)
        return True
    
    def withdraw(self, amount: float, description: str = "Withdrawal") -> bool:
        """Withdraw money from account"""
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        self._add_transaction("WITHDRAWAL", -amount, description)
        return True
    
    def _add_transaction(self, transaction_type: str, amount: float, description: str):
        """Add transaction to history"""
        transaction = {
            "id": str(uuid.uuid4()),
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now(),
            "balance_after": self.balance
        }
        self.transactions.append(transaction)
    
    def get_balance(self) -> float:
        """Get current balance"""
        return self.balance
    
    def get_transaction_history(self) -> List[Dict]:
        """Get transaction history"""
        return self.transactions.copy()


class CreditCard:
    """Represents a credit card"""
    
    def __init__(self, card_number: str, cardholder: str, credit_limit: float = 1000.0):
        self.card_number = card_number
        self.cardholder = cardholder
        self.credit_limit = credit_limit
        self.current_balance = 0.0
        self.transactions: List[Dict] = []
        self.created_at = datetime.now()
    
    def charge(self, amount: float, merchant: str = "Unknown Merchant") -> bool:
        """Charge amount to credit card"""
        if amount <= 0:
            return False
        
        if self.current_balance + amount > self.credit_limit:
            return False  # Over credit limit
        
        self.current_balance += amount
        self._add_transaction("CHARGE", amount, f"Purchase at {merchant}")
        return True
    
    def payment(self, amount: float, payment_method: str = "Bank Transfer") -> bool:
        """Make payment towards credit card"""
        if amount <= 0 or amount > self.current_balance:
            return False
        
        self.current_balance -= amount
        self._add_transaction("PAYMENT", -amount, f"Payment via {payment_method}")
        return True
    
    def _add_transaction(self, transaction_type: str, amount: float, description: str):
        """Add transaction to history"""
        transaction = {
            "id": str(uuid.uuid4()),
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now(),
            "balance_after": self.current_balance
        }
        self.transactions.append(transaction)
    
    def get_available_credit(self) -> float:
        """Get available credit"""
        return self.credit_limit - self.current_balance
    
    def get_current_balance(self) -> float:
        """Get current balance owed"""
        return self.current_balance
    
    def get_transaction_history(self) -> List[Dict]:
        """Get transaction history"""
        return self.transactions.copy()