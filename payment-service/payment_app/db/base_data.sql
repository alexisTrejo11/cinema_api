INSERT INTO payment_app_paymentmethod 
(name, is_active, configuration, created_at, updated_at)
VALUES 
(
    'credit_card',
    true,
    '{
        "api_key": "pk_test_51ABCDEfghijk",
        "api_secret": "sk_test_98765432xyz",
        "gateway": "stripe",
        "supported_cards": ["visa", "mastercard", "amex"],
        "test_mode": true,
        "webhook_url": "https://api.mycinema.com/webhooks/stripe",
        "success_url": "https://mycinema.com/payment/success",
        "failure_url": "https://mycinema.com/payment/failure"
    }',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO payment_app_paymentmethod 
(name, is_active, configuration, created_at, updated_at)
VALUES 
(
    'paypal',
    true,
    '{
        "client_id": "AeXaMpLe123456_client_id",
        "client_secret": "EXaMpLe123456_secret",
        "mode": "sandbox",
        "api_base_url": "https://api.sandbox.paypal.com",
        "webhook_id": "WH-1234567890",
        "return_url": "https://mycinema.com/payment/paypal/return",
        "cancel_url": "https://mycinema.com/payment/paypal/cancel"
    }',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO payment_app_paymentmethod 
(name, is_active, configuration, created_at, updated_at)
VALUES 
(
    'cinema_wallet',
    true,
    '{
        "wallet_type": "internal",
        "daily_limit": 1000.00,
        "transaction_limit": 500.00,
        "require_pin": true,
        "allow_refunds": true,
        "expiry_days": 365,
        "notification_email": "wallet@mycinema.com"
    }',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO payment_app_paymentmethod 
(name, is_active, configuration, created_at, updated_at)
VALUES 
(
    'google_pay',
    true,
    '{
        "merchant_id": "merchant-id-1234567890",
        "merchant_name": "My Cinema",
        "environment": "TEST",
        "gateway": "stripe",
        "gateway_merchant_id": "pk_test_merchant_123",
        "allowed_payment_methods": ["CARD", "TOKENIZED_CARD"],
        "allowed_card_networks": ["VISA", "MASTERCARD"]
    }',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);