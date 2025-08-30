#!/usr/bin/env python3
"""
Daddy Bank CLI - Banking application with T-mobile integration
"""
import argparse
import sys
from daddy_bank.core import BankAccount, CreditCard
from daddy_bank.tmobile import TMobilePaymentGateway


class DaddyBankCLI:
    """Command line interface for Daddy Bank"""
    
    def __init__(self):
        self.accounts = {}
        self.credit_cards = {}
        self.tmobile_gateway = TMobilePaymentGateway()
    
    def create_account(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        """Create a new bank account"""
        if account_number in self.accounts:
            print(f"Account {account_number} already exists")
            return False
        
        account = BankAccount(account_number, account_holder, initial_balance)
        self.accounts[account_number] = account
        print(f"Account {account_number} created for {account_holder} with balance ${initial_balance:.2f}")
        return True
    
    def create_credit_card(self, card_number: str, cardholder: str, credit_limit: float = 1000.0):
        """Create a new credit card"""
        if card_number in self.credit_cards:
            print(f"Credit card {card_number} already exists")
            return False
        
        card = CreditCard(card_number, cardholder, credit_limit)
        self.credit_cards[card_number] = card
        print(f"Credit card {card_number} created for {cardholder} with limit ${credit_limit:.2f}")
        return True
    
    def pay_with_tmobile(self, phone_number: str, amount: float, description: str = "Purchase"):
        """Process payment using T-mobile carrier billing"""
        print(f"Processing T-mobile carrier billing payment...")
        print(f"Phone: {phone_number}")
        print(f"Amount: ${amount:.2f}")
        print(f"Description: {description}")
        print("-" * 50)
        
        result = self.tmobile_gateway.process_payment(phone_number, amount, description)
        
        if result.get("success"):
            print("✅ Payment successful!")
            print(f"Transaction ID: {result.get('transaction_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Message: {result.get('message')}")
        else:
            print("❌ Payment failed!")
            print(f"Error: {result.get('error')}")
        
        return result
    
    def check_tmobile_limits(self, phone_number: str):
        """Check T-mobile carrier billing limits"""
        print(f"Checking T-mobile carrier billing limits for {phone_number}...")
        
        limits = self.tmobile_gateway.carrier_billing.get_customer_billing_limit(phone_number)
        
        if limits.get("success"):
            print("📱 T-mobile Carrier Billing Limits:")
            print(f"Daily Limit: ${limits.get('daily_limit'):.2f}")
            print(f"Monthly Limit: ${limits.get('monthly_limit'):.2f}")
            print(f"Available Today: ${limits.get('available_today'):.2f}")
            print(f"Available Monthly: ${limits.get('available_monthly'):.2f}")
        else:
            print(f"❌ Error: {limits.get('error')}")
        
        return limits
    
    def demo_tmobile_features(self):
        """Demonstrate T-mobile integration features"""
        print("🏦 Daddy Bank - T-mobile Integration Demo")
        print("=" * 50)
        
        # Demo T-mobile phone number
        tmobile_number = "505-123-4567"
        
        # Check limits
        print("\n1. Checking T-mobile carrier billing limits:")
        self.check_tmobile_limits(tmobile_number)
        
        # Process small payment
        print("\n2. Processing $15.99 payment via T-mobile:")
        self.pay_with_tmobile(tmobile_number, 15.99, "Coffee Shop Purchase")
        
        # Process larger payment
        print("\n3. Processing $45.00 payment via T-mobile:")
        self.pay_with_tmobile(tmobile_number, 45.00, "Online Store Purchase")
        
        # Try with invalid number
        print("\n4. Testing with non-T-mobile number:")
        self.pay_with_tmobile("555-123-4567", 10.00, "Test Purchase")
        
        # Try with amount over limit
        print("\n5. Testing with amount over limit:")
        self.pay_with_tmobile(tmobile_number, 75.00, "Large Purchase")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Daddy Bank - Banking with T-mobile Integration")
    parser.add_argument("--demo", action="store_true", help="Run T-mobile integration demo")
    parser.add_argument("--tmobile-pay", nargs=3, metavar=("PHONE", "AMOUNT", "DESCRIPTION"),
                       help="Pay using T-mobile carrier billing")
    parser.add_argument("--tmobile-limits", metavar="PHONE", help="Check T-mobile billing limits")
    
    args = parser.parse_args()
    
    cli = DaddyBankCLI()
    
    if args.demo:
        cli.demo_tmobile_features()
    elif args.tmobile_pay:
        phone, amount_str, description = args.tmobile_pay
        try:
            amount = float(amount_str)
            cli.pay_with_tmobile(phone, amount, description)
        except ValueError:
            print("Error: Amount must be a valid number")
            sys.exit(1)
    elif args.tmobile_limits:
        cli.check_tmobile_limits(args.tmobile_limits)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()