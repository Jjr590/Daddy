#!/usr/bin/env python3
"""
Quick demo script showing T-mobile integration capabilities
"""
from daddy_bank.core import BankAccount, CreditCard
from daddy_bank.tmobile import TMobilePaymentGateway


def main():
    print("🏦 Daddy Bank - T-mobile Integration Demo")
    print("=" * 50)
    
    # Create a sample bank account
    account = BankAccount("12345", "John Doe", 100.0)
    print(f"Created account {account.account_number} for {account.account_holder}")
    print(f"Initial balance: ${account.get_balance():.2f}")
    
    # Create a sample credit card
    credit_card = CreditCard("4567", "John Doe", 500.0)
    print(f"Created credit card {credit_card.card_number} with limit ${credit_card.credit_limit:.2f}")
    
    # Initialize T-mobile payment gateway
    tmobile = TMobilePaymentGateway()
    
    print("\n📱 T-mobile Carrier Billing Demo")
    print("-" * 30)
    
    # Demo phone number (T-mobile)
    phone = "505-123-4567"
    
    # Check customer limits
    print(f"Checking limits for {phone}...")
    limits = tmobile.carrier_billing.get_customer_billing_limit(phone)
    if limits["success"]:
        print(f"✅ Daily limit: ${limits['daily_limit']:.2f}")
        print(f"✅ Available today: ${limits['available_today']:.2f}")
    
    # Process a payment
    print(f"\nProcessing $15.99 payment via T-mobile...")
    result = tmobile.process_payment(phone, 15.99, "Coffee Shop Purchase")
    
    if result["success"]:
        print(f"✅ Payment successful!")
        print(f"   Transaction ID: {result['transaction_id']}")
        print(f"   Method: {result['payment_method']}")
        print(f"   Status: {result['status']}")
        
        # Add to bank account as a deposit (simulating payment received)
        account.deposit(15.99, f"T-mobile payment {result['transaction_id']}")
        print(f"   Account balance updated: ${account.get_balance():.2f}")
    else:
        print(f"❌ Payment failed: {result['error']}")
    
    # Try with a non-T-mobile number
    print(f"\nTesting with non-T-mobile number (555-123-4567)...")
    result2 = tmobile.process_payment("555-123-4567", 10.00, "Test Purchase")
    if not result2["success"]:
        print(f"❌ Expected failure: {result2['error']}")
    
    # Show transaction history
    print(f"\n📊 Account Transaction History:")
    for txn in account.get_transaction_history():
        print(f"   {txn['type']}: ${txn['amount']:+.2f} - {txn['description']}")
    
    print(f"\nFinal account balance: ${account.get_balance():.2f}")
    print("\n🎉 Demo completed successfully!")


if __name__ == "__main__":
    main()