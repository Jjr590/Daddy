"""
Tests for T-mobile integration functionality
"""
import unittest
from unittest.mock import patch, MagicMock
from daddy_bank.tmobile import TMobileCarrierBilling, TMobilePaymentGateway


class TestTMobileCarrierBilling(unittest.TestCase):
    """Test T-mobile carrier billing functionality"""
    
    def setUp(self):
        self.billing = TMobileCarrierBilling()
    
    def test_verify_tmobile_number_valid(self):
        """Test valid T-mobile phone number verification"""
        valid_numbers = [
            "505-123-4567",
            "5051234567",
            "(505) 123-4567",
            "878-555-0123"
        ]
        
        for number in valid_numbers:
            with self.subTest(number=number):
                self.assertTrue(self.billing.verify_tmobile_number(number))
    
    def test_verify_tmobile_number_invalid(self):
        """Test invalid phone number verification"""
        invalid_numbers = [
            "555-123-4567",  # Not T-mobile prefix
            "12345",         # Too short
            "123-456-78901", # Too long
            "abc-def-ghij"   # Not numeric
        ]
        
        for number in invalid_numbers:
            with self.subTest(number=number):
                self.assertFalse(self.billing.verify_tmobile_number(number))
    
    def test_initiate_carrier_billing_valid(self):
        """Test successful carrier billing initiation"""
        with patch('random.random', return_value=0.5):  # Ensure success
            result = self.billing.initiate_carrier_billing("505-123-4567", 25.00, "Test purchase")
            
            self.assertTrue(result["success"])
            self.assertIsNotNone(result["transaction_id"])
            self.assertEqual(result["status"], "pending")
    
    def test_initiate_carrier_billing_invalid_number(self):
        """Test carrier billing with invalid phone number"""
        result = self.billing.initiate_carrier_billing("555-123-4567", 25.00, "Test purchase")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Invalid T-mobile phone number")
    
    def test_initiate_carrier_billing_invalid_amount(self):
        """Test carrier billing with invalid amounts"""
        # Test negative amount
        result = self.billing.initiate_carrier_billing("505-123-4567", -10.00, "Test purchase")
        self.assertFalse(result["success"])
        
        # Test zero amount
        result = self.billing.initiate_carrier_billing("505-123-4567", 0.00, "Test purchase")
        self.assertFalse(result["success"])
        
        # Test amount over limit
        result = self.billing.initiate_carrier_billing("505-123-4567", 100.00, "Test purchase")
        self.assertFalse(result["success"])
    
    def test_get_customer_billing_limit(self):
        """Test getting customer billing limits"""
        result = self.billing.get_customer_billing_limit("505-123-4567")
        
        self.assertTrue(result["success"])
        self.assertIn("daily_limit", result)
        self.assertIn("monthly_limit", result)
        self.assertGreater(result["daily_limit"], 0)


class TestTMobilePaymentGateway(unittest.TestCase):
    """Test T-mobile payment gateway functionality"""
    
    def setUp(self):
        self.gateway = TMobilePaymentGateway()
    
    @patch('daddy_bank.tmobile.TMobileCarrierBilling.get_customer_billing_limit')
    @patch('daddy_bank.tmobile.TMobileCarrierBilling.initiate_carrier_billing')
    def test_process_payment_success(self, mock_billing, mock_limits):
        """Test successful payment processing"""
        # Mock billing limits
        mock_limits.return_value = {
            "success": True,
            "daily_limit": 50.0,
            "available_today": 50.0
        }
        
        # Mock billing initiation
        mock_billing.return_value = {
            "success": True,
            "transaction_id": "test-123",
            "status": "pending"
        }
        
        result = self.gateway.process_payment("505-123-4567", 25.00, "Test purchase")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["payment_method"], "T-mobile Carrier Billing")
        self.assertEqual(result["amount"], 25.00)
    
    @patch('daddy_bank.tmobile.TMobileCarrierBilling.get_customer_billing_limit')
    def test_process_payment_over_limit(self, mock_limits):
        """Test payment processing when amount exceeds limit"""
        # Mock billing limits
        mock_limits.return_value = {
            "success": True,
            "daily_limit": 25.0,
            "available_today": 25.0
        }
        
        result = self.gateway.process_payment("505-123-4567", 50.00, "Test purchase")
        
        self.assertFalse(result["success"])
        self.assertIn("exceeds daily carrier billing limit", result["error"])


if __name__ == "__main__":
    unittest.main()