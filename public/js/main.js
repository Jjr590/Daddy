// Initialize Stripe (mock for demo)
const stripe = window.Stripe ? window.Stripe('pk_test_demo_key') : null;

// Global variables
let services = {};
let selectedService = null;
let elements = null;
let paymentElement = null;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    loadServices();
    setupEventListeners();
    setupMobileMenu();
});

// Load services from API
async function loadServices() {
    try {
        const response = await fetch('/api/payment/pricing');
        services = await response.json();
        displayServices();
    } catch (error) {
        console.error('Error loading services:', error);
        // Fallback to hardcoded services
        services = {
            'basic-edit': {
                name: 'Basic Video Edit',
                description: 'Cut, trim, and basic color correction',
                price: 2500,
                duration: '1-2 business days'
            },
            'advanced-edit': {
                name: 'Advanced Video Edit',
                description: 'Professional editing with effects, transitions, and audio mixing',
                price: 7500,
                duration: '3-5 business days'
            },
            'premium-edit': {
                name: 'Premium Video Edit',
                description: 'Complete production with motion graphics, custom animations',
                price: 15000,
                duration: '1-2 weeks'
            },
            'motion-graphics': {
                name: 'Motion Graphics Package',
                description: 'Custom motion graphics and animations',
                price: 10000,
                duration: '1 week'
            },
            'consultation': {
                name: 'Video Strategy Consultation',
                description: '1-hour consultation for video production planning',
                price: 5000,
                duration: '1 hour session'
            }
        };
        displayServices();
    }
}

// Display services in the grid
function displayServices() {
    const servicesGrid = document.getElementById('services-grid');
    servicesGrid.innerHTML = '';

    Object.entries(services).forEach(([key, service]) => {
        const serviceCard = createServiceCard(key, service);
        servicesGrid.appendChild(serviceCard);
    });
}

// Create service card element
function createServiceCard(key, service) {
    const card = document.createElement('div');
    card.className = 'service-card';
    
    const price = (service.price / 100).toFixed(2);
    
    card.innerHTML = `
        <div class="service-header">
            <div>
                <h3>${service.name}</h3>
                <div class="service-duration">⏱️ ${service.duration}</div>
            </div>
            <div class="service-price">$${price}</div>
        </div>
        <p>${service.description}</p>
        <button class="btn-primary" onclick="selectService('${key}')">
            Select Service
        </button>
    `;
    
    return card;
}

// Setup event listeners
function setupEventListeners() {
    // Contact form
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', handleContactSubmit);

    // Modal close
    const modal = document.getElementById('payment-modal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Payment submission
    const submitButton = document.getElementById('submit-payment');
    submitButton.addEventListener('click', handlePaymentSubmit);
}

// Setup mobile menu
function setupMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close menu when clicking on links
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
}

// Select service and open payment modal
function selectService(serviceKey) {
    selectedService = serviceKey;
    const service = services[serviceKey];
    
    // Update modal content
    const paymentDetails = document.getElementById('payment-details');
    const price = (service.price / 100).toFixed(2);
    
    paymentDetails.innerHTML = `
        <div class="service-summary">
            <h4>${service.name}</h4>
            <p>${service.description}</p>
            <div class="price-summary">
                <strong>Total: $${price}</strong>
            </div>
        </div>
    `;

    // Show modal
    document.getElementById('payment-modal').style.display = 'block';
    
    // Initialize Stripe Elements (mock)
    initializePaymentForm();
}

// Handle contact form submission
function handleContactSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const serviceValue = formData.get('service') || formData.get('select');
    
    if (serviceValue && services[serviceValue]) {
        selectService(serviceValue);
    } else {
        alert('Please select a service to continue.');
    }
}

// Initialize payment form (mock implementation)
function initializePaymentForm() {
    const paymentForm = document.getElementById('payment-form');
    
    // Mock Stripe Elements UI
    paymentForm.innerHTML = `
        <div class="payment-element-mock">
            <div class="card-input-group">
                <label>Card Number</label>
                <input type="text" id="card-number" placeholder="1234 5678 9012 3456" maxlength="19">
            </div>
            <div class="card-input-row">
                <div class="card-input-group">
                    <label>Expiry</label>
                    <input type="text" id="card-expiry" placeholder="MM/YY" maxlength="5">
                </div>
                <div class="card-input-group">
                    <label>CVC</label>
                    <input type="text" id="card-cvc" placeholder="123" maxlength="4">
                </div>
            </div>
            <div class="card-input-group">
                <label>Cardholder Name</label>
                <input type="text" id="card-name" placeholder="John Doe">
            </div>
        </div>
        <style>
            .payment-element-mock {
                padding: 1rem;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                background: #f8fafc;
            }
            .card-input-group {
                margin-bottom: 1rem;
            }
            .card-input-group label {
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 500;
                color: #333;
            }
            .card-input-group input {
                width: 100%;
                padding: 12px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 1rem;
            }
            .card-input-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }
        </style>
    `;

    // Add card number formatting
    const cardNumberInput = document.getElementById('card-number');
    cardNumberInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
        e.target.value = formattedValue;
    });

    // Add expiry formatting
    const expiryInput = document.getElementById('card-expiry');
    expiryInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
            value = value.substring(0, 2) + '/' + value.substring(2, 4);
        }
        e.target.value = value;
    });
}

// Handle payment submission (mock)
async function handlePaymentSubmit() {
    const submitButton = document.getElementById('submit-payment');
    const statusDiv = document.getElementById('payment-status');
    
    // Validate form
    const cardNumber = document.getElementById('card-number').value;
    const cardExpiry = document.getElementById('card-expiry').value;
    const cardCvc = document.getElementById('card-cvc').value;
    const cardName = document.getElementById('card-name').value;

    if (!cardNumber || !cardExpiry || !cardCvc || !cardName) {
        showPaymentStatus('Please fill in all card details.', 'error');
        return;
    }

    // Show loading state
    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';
    statusDiv.innerHTML = '';

    try {
        // Mock payment processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Simulate successful payment
        const service = services[selectedService];
        const amount = service.price;
        
        // Mock API call for payment confirmation
        const mockPaymentResult = {
            success: true,
            payment: {
                id: `pi_mock_${Date.now()}`,
                amount: amount / 100,
                currency: 'usd',
                status: 'succeeded',
                service: selectedService
            },
            cryptoPayout: {
                success: true,
                transactionId: `crypto_${Date.now()}`,
                amount: amount / 100,
                currency: 'usd',
                cryptoAmount: (amount / 100 * 0.000025).toFixed(8),
                cryptoCurrency: 'BTC'
            }
        };

        // Show success message
        showPaymentStatus(`
            <div class="payment-success">
                <h4>✅ Payment Successful!</h4>
                <p><strong>Order ID:</strong> ${mockPaymentResult.payment.id}</p>
                <p><strong>Service:</strong> ${service.name}</p>
                <p><strong>Amount:</strong> $${mockPaymentResult.payment.amount}</p>
                <hr style="margin: 1rem 0;">
                <p><strong>Crypto Payout Processed:</strong></p>
                <p>${mockPaymentResult.cryptoPayout.cryptoAmount} ${mockPaymentResult.cryptoPayout.cryptoCurrency}</p>
                <p><strong>Transaction ID:</strong> ${mockPaymentResult.cryptoPayout.transactionId}</p>
                <br>
                <p>You will receive an email confirmation shortly. We'll get started on your project within 24 hours!</p>
            </div>
        `, 'success');

        // Reset button after delay
        setTimeout(() => {
            closeModal();
            resetPaymentForm();
        }, 5000);

    } catch (error) {
        console.error('Payment error:', error);
        showPaymentStatus('Payment failed. Please try again.', 'error');
        submitButton.disabled = false;
        submitButton.textContent = 'Pay Now';
    }
}

// Show payment status
function showPaymentStatus(message, type) {
    const statusDiv = document.getElementById('payment-status');
    statusDiv.innerHTML = message;
    statusDiv.className = type;
}

// Close modal
function closeModal() {
    document.getElementById('payment-modal').style.display = 'none';
    resetPaymentForm();
}

// Reset payment form
function resetPaymentForm() {
    const submitButton = document.getElementById('submit-payment');
    const statusDiv = document.getElementById('payment-status');
    
    submitButton.disabled = false;
    submitButton.textContent = 'Pay Now';
    statusDiv.innerHTML = '';
    
    // Clear form inputs
    document.querySelectorAll('#payment-form input').forEach(input => {
        input.value = '';
    });
}

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.backdropFilter = 'blur(20px)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.service-card, .portfolio-item, .skill-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
});