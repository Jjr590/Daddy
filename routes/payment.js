const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const router = express.Router();

// Mock crypto payout function
async function processCryptoPayout(amount, currency) {
  console.log(`Processing crypto payout: ${amount} ${currency}`);
  console.log(`Sending to wallet: ${process.env.CRYPTO_WALLET_ADDRESS}`);
  
  // In a real implementation, this would:
  // 1. Convert fiat to crypto
  // 2. Send to wallet address
  // 3. Return transaction ID
  
  return {
    success: true,
    transactionId: `crypto_${Date.now()}`,
    amount: amount,
    currency: currency,
    cryptoAmount: (amount * 0.000025).toFixed(8), // Mock BTC conversion
    cryptoCurrency: 'BTC'
  };
}

// Create payment intent
router.post('/create-intent', async (req, res) => {
  try {
    const { amount, currency = 'usd', service, customerEmail } = req.body;

    if (!amount || amount < 50) {
      return res.status(400).json({ error: 'Minimum amount is $0.50' });
    }

    const paymentIntent = await stripe.paymentIntents.create({
      amount: amount, // Amount in cents
      currency: currency,
      metadata: {
        service: service || 'video-editing',
        customerEmail: customerEmail || 'unknown'
      }
    });

    res.json({
      clientSecret: paymentIntent.client_secret,
      amount: amount,
      currency: currency,
      service: service
    });

  } catch (error) {
    console.error('Payment intent creation error:', error);
    res.status(500).json({ error: 'Failed to create payment intent' });
  }
});

// Confirm payment and process crypto payout
router.post('/confirm', async (req, res) => {
  try {
    const { paymentIntentId } = req.body;
    
    if (!paymentIntentId) {
      return res.status(400).json({ error: 'Payment intent ID required' });
    }

    // Retrieve payment intent from Stripe
    const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);
    
    if (paymentIntent.status === 'succeeded') {
      // Process crypto payout to owner
      const cryptoPayout = await processCryptoPayout(
        paymentIntent.amount / 100, // Convert cents to dollars
        paymentIntent.currency
      );

      res.json({
        success: true,
        payment: {
          id: paymentIntent.id,
          amount: paymentIntent.amount / 100,
          currency: paymentIntent.currency,
          status: paymentIntent.status,
          service: paymentIntent.metadata.service
        },
        cryptoPayout: cryptoPayout
      });
    } else {
      res.status(400).json({ 
        error: 'Payment not successful',
        status: paymentIntent.status 
      });
    }

  } catch (error) {
    console.error('Payment confirmation error:', error);
    res.status(500).json({ error: 'Failed to confirm payment' });
  }
});

// Get service pricing
router.get('/pricing', (req, res) => {
  const services = {
    'basic-edit': {
      name: 'Basic Video Edit',
      description: 'Cut, trim, and basic color correction',
      price: 2500, // $25.00
      duration: '1-2 business days'
    },
    'advanced-edit': {
      name: 'Advanced Video Edit',
      description: 'Professional editing with effects, transitions, and audio mixing',
      price: 7500, // $75.00
      duration: '3-5 business days'
    },
    'premium-edit': {
      name: 'Premium Video Edit',
      description: 'Complete production with motion graphics, custom animations',
      price: 15000, // $150.00
      duration: '1-2 weeks'
    },
    'motion-graphics': {
      name: 'Motion Graphics Package',
      description: 'Custom motion graphics and animations',
      price: 10000, // $100.00
      duration: '1 week'
    },
    'consultation': {
      name: 'Video Strategy Consultation',
      description: '1-hour consultation for video production planning',
      price: 5000, // $50.00
      duration: '1 hour session'
    }
  };

  res.json(services);
});

module.exports = router;