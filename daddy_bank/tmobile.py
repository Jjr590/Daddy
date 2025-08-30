"""
T-mobile carrier billing integration for Daddy Bank
Enables T-mobile customers to charge purchases to their mobile phone bill
"""
import requests
from typing import Dict, Optional
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class TMobileCarrierBilling:
    """T-mobile carrier billing payment processor"""
    
    def __init__(self):
        self.api_base_url = os.getenv("TMOBILE_API_BASE_URL", "https://api.t-mobile.com/billing/v1")
        self.api_key = os.getenv("TMOBILE_API_KEY", "demo_key")
        self.merchant_id = os.getenv("TMOBILE_MERCHANT_ID", "daddy_bank_001")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "DaddyBank/1.0"
        })
    
    def verify_tmobile_number(self, phone_number: str) -> bool:
        """Verify if phone number is a valid T-mobile number"""
        # Remove any formatting from phone number
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Basic validation - T-mobile US numbers
        if len(clean_number) != 10:
            return False
        
        # T-mobile prefixes (this is a simplified check)
        tmobile_prefixes = [
            "505", "506", "508", "509", "878", "879", 
            "280", "281", "282", "283", "284"
        ]
        
        area_code = clean_number[:3]
        return area_code in tmobile_prefixes
    
    def initiate_carrier_billing(self, phone_number: str, amount: float, description: str) -> Dict:
        """Initiate a carrier billing transaction"""
        if not self.verify_tmobile_number(phone_number):
            return {
                "success": False,
                "error": "Invalid T-mobile phone number",
                "transaction_id": None
            }
        
        if amount <= 0 or amount > 50.0:  # T-mobile typically limits carrier billing amounts
            return {
                "success": False,
                "error": "Amount must be between $0.01 and $50.00 for carrier billing",
                "transaction_id": None
            }
        
        transaction_id = str(uuid.uuid4())
        
        # In a real implementation, this would make an API call to T-mobile
        # For demo purposes, we'll simulate the API response
        billing_request = {
            "merchant_id": self.merchant_id,
            "phone_number": phone_number,
            "amount": amount,
            "currency": "USD",
            "description": description,
            "transaction_id": transaction_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate API call success/failure (90% success rate for demo)
        import random
        if random.random() < 0.9:
            return {
                "success": True,
                "transaction_id": transaction_id,
                "status": "pending",
                "billing_request": billing_request,
                "message": "Carrier billing initiated. Customer will receive SMS confirmation."
            }
        else:
            return {
                "success": False,
                "error": "T-mobile carrier billing service temporarily unavailable",
                "transaction_id": transaction_id
            }
    
    def check_transaction_status(self, transaction_id: str) -> Dict:
        """Check the status of a carrier billing transaction"""
        # In a real implementation, this would query T-mobile's API
        # For demo purposes, simulate different statuses
        import random
        statuses = ["pending", "confirmed", "failed", "cancelled"]
        status = random.choice(statuses)
        
        return {
            "transaction_id": transaction_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_customer_billing_limit(self, phone_number: str) -> Dict:
        """Get the carrier billing limit for a T-mobile customer"""
        if not self.verify_tmobile_number(phone_number):
            return {
                "success": False,
                "error": "Invalid T-mobile phone number"
            }
        
        # Simulate different billing limits based on customer account
        import random
        limits = [10.0, 25.0, 50.0]
        current_limit = random.choice(limits)
        
        return {
            "success": True,
            "phone_number": phone_number,
            "daily_limit": current_limit,
            "monthly_limit": current_limit * 10,
            "available_today": current_limit,
            "available_monthly": current_limit * 8
        }


class TMobilePaymentGateway:
    """T-mobile payment gateway integration"""
    
    def __init__(self):
        self.carrier_billing = TMobileCarrierBilling()
    
    def process_payment(self, phone_number: str, amount: float, description: str) -> Dict:
        """Process a payment using T-mobile carrier billing"""
        # Check customer's billing limit first
        limit_check = self.carrier_billing.get_customer_billing_limit(phone_number)
        if not limit_check.get("success"):
            return limit_check
        
        if amount > limit_check.get("available_today", 0):
            return {
                "success": False,
                "error": f"Amount exceeds daily carrier billing limit of ${limit_check.get('daily_limit', 0)}"
            }
        
        # Initiate the carrier billing
        result = self.carrier_billing.initiate_carrier_billing(phone_number, amount, description)
        
        if result.get("success"):
            return {
                "success": True,
                "transaction_id": result.get("transaction_id"),
                "payment_method": "T-mobile Carrier Billing",
                "amount": amount,
                "status": "pending",
                "message": "Payment initiated via T-mobile carrier billing"
            }
        else:
            return result
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify a payment transaction"""
        return self.carrier_billing.check_transaction_status(transaction_id)