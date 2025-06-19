# Payment Gateway API

A Flask-based payment gateway API that integrates with PayPal for handling subscription-based payments. This project provides endpoints for creating and managing subscriptions with different plan types.

## Features

- PayPal integration for subscription management
- JWT-based authentication
- Support for multiple subscription plans (Basic and Premium)
- Webhook handling for subscription status updates
- SQLite database for storing subscription information

## Prerequisites

- Python 3.7 or higher
- PayPal Business Account
- PayPal API credentials (Client ID and Secret)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd payment_gateway
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following required variables:
```
# Database Configuration
DATABASE_URL=sqlite:///payment_gateway.db  # SQLite database URL (change for production)

# Security
JWT_SECRET_KEY=your_jwt_secret_key  # Secret key for JWT token generation and verification

# PayPal Configuration
PAYPAL_MODE=sandbox  # Use 'sandbox' for testing, 'live' for production
PAYPAL_CLIENT_ID=your_paypal_client_id  # Your PayPal API client ID
PAYPAL_CLIENT_SECRET=your_paypal_client_secret  # Your PayPal API client secret
PAYPAL_PLAN_ID=your_paypal_plan_id  # ID of your PayPal subscription plan

# Server Configuration
PORT=5000  # Port number for the application to run on
```

Note: Make sure to keep these environment variables secure and never commit them to version control.

## Project Structure

- `payment_api.py`: Main application file containing API endpoints
- `models.py`: Database models for subscriptions
- `config.py`: Application configuration
- `utils.py`: Utility functions including JWT verification
- `requirements.txt`: Project dependencies

## API Endpoints

### Create Subscription
- **URL**: `/api/subscribe`
- **Method**: `POST`
- **Headers**: 
  - `Authorization`: JWT token
- **Body**:
  ```json
  {
    "plan_type": "premium"  // or "basic"
  }
  ```
- **Response**: Returns PayPal approval URL for subscription

### PayPal Webhook
- **URL**: `/api/webhook`
- **Method**: `POST`
- **Body**: PayPal webhook event data
- **Response**: Success status

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:
```bash
python payment_api.py
```

The server will start on `http://localhost:5000` (or the port specified in your .env file)

## Security Considerations

- Always use HTTPS in production
- Keep your PayPal API credentials secure
- Use strong JWT secrets
- Implement rate limiting for production use
- Validate all incoming webhook data

## Development

### Testing
- Use PayPal sandbox environment for testing
- Test webhook handling using PayPal's webhook simulator
- Verify subscription status updates

### Production Deployment
- Set `PAYPAL_MODE` to 'live' in production
- Use proper SSL certificates
- Implement proper error handling and logging
- Set up monitoring for webhook events

