# Auction Marketplace (Django)

A full-stack auction marketplace built with Django that allows users to list products, place bids, manage favorites, complete purchases using Stripe Checkout, and rate purchased items.

This project demonstrates authentication workflows, relational data modeling, payment integration, and business-logic enforcement using Django class-based views.

Repository:
https://github.com/songyuchen2584/cs412/tree/main/project

---

## Features

### User Accounts
- User registration and login/logout
- Profile creation and editing
- Personal dashboard views
  - My Products
  - My Favorites
  - My Bids
  - My Orders

### Product Marketplace
- Create, update, and delete product listings
- Upload multiple product images
- Product search and category filtering
- Seller-only product editing restrictions

### Bidding System
- Place bids on available products
- Sellers can accept exactly one bid
- Automatic rejection of competing bids
- Prevent bidding on sold products

### Favorites
- Add and remove favorite products
- Dashboard view for saved items

### Checkout and Orders
- Checkout accepted bids
- Order creation with product state updates
- Stripe Checkout integration
- Stripe webhook for payment confirmation
- Atomic transaction handling for order finalization

### Ratings
- Buyers can rate products after purchase
- Rating stored with product data

---

## Tech Stack

- Python
- Django
- SQLite
- Stripe API
- Django ORM
- HTML Templates

---

## Database Models

The application uses normalized relational models:

- Account
- Product
- ProductImage
- Bid
- Favorite
- Order

Relationships include:

- Account → Product (one-to-many)
- Product → Bid (one-to-many)
- Order ↔ Product (many-to-many)

---

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/songyuchen2584/cs412.git
cd cs412/project
Create a virtual environment:

python -m venv venv
Activate it:

Windows:

venv\Scripts\activate
Mac/Linux:

source venv/bin/activate
Install dependencies:

pip install django stripe pillow
Run migrations:

python manage.py migrate
Create admin user:

python manage.py createsuperuser
Run the server:

python manage.py runserver
Open in browser:

http://127.0.0.1:8000/project/

```

## Stripe Configuration
Stripe API keys must be defined inside:

    cs412/settings.py

Add:

```python
STRIPE_SECRET_KEY = "your_secret_key"
STRIPE_PUBLISHABLE_KEY = "your_publishable_secret"
STRIPE_WEBHOOK_SECRET = "yout_webhook_secret"
```

## Stripe Test Payment Information

This project uses **Stripe test mode**, so no real payment is required.

Use the following test card during checkout:

Card number:
4242 4242 4242 4242

Expiration date:
Any future date (e.g., 12/34)

CVC:
123

ZIP:
Any value (e.g., 02115)


These credentials are provided by Stripe for testing checkout flows.

Stripe documentation:
https://stripe.com/docs/testing


## Business Logic Highlights
- Only sellers can accept bids

- Only one bid can be accepted per product

- Sold products cannot be edited or deleted

- Users can only rate purchased products

- Stripe webhook finalizes orders atomically

- Checkout prevents duplicate order creation