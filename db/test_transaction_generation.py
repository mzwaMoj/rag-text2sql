"""
Test script for transaction history data generation
"""

import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

def test_generate_transaction_data():
    """Test the transaction data generation function"""
    fake = Faker()
    
    # Mock customer IDs
    customer_ids = [10000001, 10000002, 10000003, 10000004, 10000005]
    
    # Transaction types and categories
    transaction_types = [
        "Deposit", "Withdrawal", "Transfer", "Payment", "Purchase", 
        "Refund", "Fee", "Interest", "Loan Payment", "Salary"
    ]
    
    transaction_categories = [
        "Groceries", "Gas", "Restaurant", "Shopping", "Utilities", 
        "Healthcare", "Entertainment", "Travel", "Education", "Insurance",
        "Banking", "Investment", "Salary", "Bonus", "Refund", "Other"
    ]
    
    transaction_channels = [
        "ATM", "Online Banking", "Mobile App", "Branch", "POS Terminal",
        "Wire Transfer", "ACH", "Check", "Direct Deposit"
    ]
    
    transaction_statuses = ["Completed", "Pending", "Failed", "Cancelled"]
    currencies = ["ZAR", "USD", "EUR", "GBP", "JPY"]
    
    # Generate 10 test transactions
    data = []
    for i in range(10):
        customer_id = random.choice(customer_ids)
        transaction_id = fake.unique.random_number(digits=12)
        transaction_type = random.choice(transaction_types)
        category = random.choice(transaction_categories)
        channel = random.choice(transaction_channels)
        status = random.choice(transaction_statuses)
        currency = random.choices(currencies, weights=[85, 5, 3, 3, 4])[0]
        
        # Generate amount based on type
        if transaction_type in ["Salary", "Bonus"]:
            amount = round(random.uniform(15000.0, 80000.0), 2)
        elif transaction_type in ["Deposit", "Transfer"]:
            amount = round(random.uniform(100.0, 25000.0), 2)
        elif transaction_type in ["Withdrawal", "Payment", "Purchase"]:
            amount = round(random.uniform(50.0, 5000.0), 2)
        elif transaction_type == "Fee":
            amount = round(random.uniform(5.0, 200.0), 2)
        elif transaction_type == "Interest":
            amount = round(random.uniform(10.0, 1000.0), 2)
        else:
            amount = round(random.uniform(10.0, 10000.0), 2)
        
        # Make withdrawals, payments, purchases, and fees negative
        if transaction_type in ["Withdrawal", "Payment", "Purchase", "Fee", "Loan Payment"]:
            amount = -abs(amount)
        
        transaction_date = fake.date_time_between(start_date="-2y", end_date="now")
        
        # Generate merchant info for purchases/payments
        if transaction_type in ["Purchase", "Payment"]:
            merchant_name = fake.company()
            merchant_category = category
        else:
            merchant_name = None
            merchant_category = None
        
        reference_number = fake.bothify(text='REF####??####')
        
        # Generate description
        if transaction_type == "Purchase":
            description = f"{category} purchase at {merchant_name if merchant_name else fake.company()}"
        elif transaction_type == "Transfer":
            description = f"Transfer to {fake.name()}"
        elif transaction_type == "Salary":
            description = f"Salary payment from {fake.company()}"
        elif transaction_type == "Withdrawal":
            description = f"Cash withdrawal - {channel}"
        elif transaction_type == "Deposit":
            description = f"Deposit - {channel}"
        else:
            description = f"{transaction_type} - {category}"
        
        account_from = fake.random_number(digits=10)
        account_to = fake.random_number(digits=10) if transaction_type == "Transfer" else None
        balance_after = round(random.uniform(500.0, 50000.0), 2)
        location = fake.city() + ", " + fake.country()
        
        transaction = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "transaction_date": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_type": transaction_type,
            "amount": amount,
            "currency": currency,
            "description": description,
            "category": category,
            "channel": channel,
            "status": status,
            "reference_number": reference_number,
            "merchant_name": merchant_name,
            "merchant_category": merchant_category,
            "account_from": str(account_from),
            "account_to": str(account_to) if account_to else None,
            "balance_after": balance_after,
            "location": location,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(transaction)
    
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} test transaction records")
    print("\nSample transactions:")
    print(df[['transaction_id', 'customer_id', 'transaction_type', 'amount', 'currency', 'description']].head())
    
    return df

if __name__ == "__main__":
    test_generate_transaction_data()
