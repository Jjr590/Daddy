# BigFX - Professional Video Editing Services

A complete e-commerce website for BigFX, offering professional video editing tools and services. Features modern design, payment processing, and crypto payout integration.

## Features

### Frontend
- **Modern Design**: Professional gradient design with responsive layout
- **Service Showcase**: Multiple video editing service tiers with clear pricing
- **Portfolio Gallery**: Visual showcase of work examples with hover effects
- **About Section**: Skills demonstration and business statistics
- **Contact Form**: Integrated service selection and project inquiry form

### Backend
- **Express.js Server**: Robust Node.js backend with REST API
- **Payment Processing**: Credit/debit card payment integration (Stripe-ready)
- **Crypto Payouts**: Automated cryptocurrency conversion and payout system
- **Service Management**: Dynamic pricing and service configuration

### Services Offered
- **Basic Video Edit** - $25.00 (Cut, trim, color correction)
- **Advanced Video Edit** - $75.00 (Effects, transitions, audio mixing)
- **Premium Video Edit** - $150.00 (Full production with motion graphics)
- **Motion Graphics Package** - $100.00 (Custom animations)
- **Video Strategy Consultation** - $50.00 (1-hour planning session)

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Node.js, Express.js
- **Payment**: Stripe API integration
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Unicode emoji icons for fast loading

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your Stripe keys and crypto wallet address
   ```

3. **Start the Server**
   ```bash
   npm start
   ```

4. **Visit the Website**
   ```
   http://localhost:3000
   ```

## API Endpoints

- `GET /api/payment/pricing` - Get service pricing
- `POST /api/payment/create-intent` - Create payment intent
- `POST /api/payment/confirm` - Confirm payment and process crypto payout

## Payment Flow

1. Customer selects a service
2. Payment form opens with service details
3. Customer enters credit/debit card information
4. Payment is processed through Stripe
5. Automated crypto conversion and payout to owner's wallet
6. Order confirmation and project initiation

## Business Model

- **Customer Payments**: Credit/debit cards for accessibility
- **Owner Payouts**: Cryptocurrency for modern financial flexibility
- **Service Tiers**: Multiple price points for different needs
- **Professional Branding**: BigFX brand identity throughout

## License

This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**BigFX** - Transform your raw footage into compelling visual narratives.
