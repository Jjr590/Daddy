# Daddy Bank
Bank & CC application with T-mobile integration

## Features

- **Banking Services**: Create and manage bank accounts with deposits and withdrawals
- **Credit Card Services**: Issue and manage credit cards with spending limits
- **T-mobile Integration**: Carrier billing support for T-mobile customers

### T-mobile Carrier Billing

This application integrates with T-mobile's carrier billing service, allowing T-mobile customers to charge purchases directly to their mobile phone bill.

#### Features:
- Verify T-mobile phone numbers
- Process payments via carrier billing (up to $50 per transaction)
- Check customer billing limits
- Transaction status tracking

## Installation

```bash
pip install -e .
```

## Usage

### Command Line Interface

Run the T-mobile integration demo:
```bash
python -m daddy_bank.cli --demo
```

Process a payment via T-mobile carrier billing:
```bash
python -m daddy_bank.cli --tmobile-pay "505-123-4567" "25.99" "Coffee Shop"
```

Check T-mobile billing limits:
```bash
python -m daddy_bank.cli --tmobile-limits "505-123-4567"
```

### Python API

```python
from daddy_bank.tmobile import TMobilePaymentGateway

gateway = TMobilePaymentGateway()

# Process a payment
result = gateway.process_payment("505-123-4567", 25.99, "Coffee Shop Purchase")
if result["success"]:
    print(f"Payment processed: {result['transaction_id']}")
else:
    print(f"Payment failed: {result['error']}")
```

## Configuration

Copy `.env.example` to `.env` and configure your T-mobile API credentials:

```
TMOBILE_API_KEY=your_api_key_here
TMOBILE_MERCHANT_ID=your_merchant_id_here
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## T-mobile Integration Details

### Supported Phone Number Prefixes
- 505, 506, 508, 509 (New Mexico)
- 878, 879 (Pennsylvania/National)
- 280, 281, 282, 283, 284 (National)

### Transaction Limits
- Single transaction: $0.01 - $50.00
- Daily limit: Varies by customer (typically $10-$50)
- Monthly limit: Typically 10x daily limit

### Payment Flow
1. Customer initiates payment with T-mobile phone number
2. System verifies number is T-mobile and checks limits
3. Carrier billing request sent to T-mobile
4. Customer receives SMS confirmation
5. Payment is processed and charged to phone bill
