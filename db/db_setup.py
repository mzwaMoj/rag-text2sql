import sqlite3
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import json

def calculate_loan_interest_rate(credit_score, loan_tenure, loan_amount):
    """
    Calculate loan interest rate based on credit score, loan tenure (months), and loan amount.
    Lower credit score, longer tenure, and higher amount increase the rate.
    """
    # Base rate decreases with higher credit score
    base_rate = 15 - (credit_score - 300) * 0.012  # 15% for 300, ~6.6% for 850

    # Tenure adjustment: longer tenure increases rate
    tenure_adj = (loan_tenure / 60) * 2  # up to +2% for 60 months

    # Amount adjustment: higher amounts slightly increase rate
    amount_adj = (loan_amount / 100000) * 1.5  # up to +1.5% for 100k

    # Clamp to reasonable range
    rate = base_rate + tenure_adj + amount_adj
    return round(max(3.5, min(rate, 20.0)), 2)

def get_product_names():
    """
    Extract product names from the product offerings file.
    Returns a dictionary with product categories and their respective products.
    """
    product_file_path = os.path.join(os.path.dirname(__file__), 'product_offerings.txt')
    
    # Define default products in case file doesn't exist
    default_products = {
        "Deposit": ["Savings Account", "Checking Account", "Certificates of Deposit (CDs)"],
        "Credit": ["Personal Loans", "Auto Loans", "Home Mortgages", "Credit Cards", "Overdraft Protection"],
        "Investment": ["Brokerage Accounts", "Retirement Accounts (IRA, 401k)", "Investment Advisory Services"],
        "Services": ["Mobile & Online Banking", "Foreign Currency Exchange", "Safe Deposit Boxes", "Insurance Products"]
    }
    
    # Print debug info
    print(f"Looking for product offerings file at: {product_file_path}")
    print(f"File exists: {os.path.exists(product_file_path)}")
    
    # Return default products if file doesn't exist
    if not os.path.exists(product_file_path):
        print("Product offerings file not found, using default products")
        return default_products
    
    try:
        # Extract products from product offerings file
        with open(product_file_path, 'r') as file:
            content = file.read()
        
        # Extract product names from the format "### N. Product Name"
        import re
        product_matches = re.findall(r'### \d+\. ([^\n]+)', content)
        
        # Also capture credit card types
        credit_card_matches = re.findall(r'##### [a-z]\) ([^\n]+)', content)
        
        # Extract main categories "## Category Name"
        category_matches = re.findall(r'## ([^\n]+)', content)
        
        # Create the products dictionary
        products = {}
        
        # Add main categories
        for category in category_matches:
            products[category] = []
            
        # For simplicity, just put all products in a single "All Products" category
        all_products = product_matches + credit_card_matches
        products["All Products"] = all_products
        
        # Add products to their respective categories based on the categories in the file
        products["Retail Banking"] = product_matches[:7]  # First 7 products
        products["Business Banking"] = product_matches[7:11]  # Next 4 products
        products["Wealth Management & Investment"] = product_matches[11:14]  # Next 3 products
        products["Digital & Specialized Services"] = product_matches[14:]  # Remaining products
        
        print(f"Found {len(all_products)} products in the file")
        for category, prods in products.items():
            print(f"Category '{category}' has {len(prods)} products")
        
        # Return extracted products or default if extraction failed
        if all_products:
            return products
        else:
            print("No products found in file, using default products")
            return default_products
    except Exception as e:
        print(f"Error reading product offerings file: {e}")
        print("Using default products")
        return default_products

def generate_product_holdings(income, age, credit_score, income_category):
    """
    Generate a list of product holdings based on customer profile.
    Higher income, age, and credit score increase the chance of having more products.
    """
    products_by_category = get_product_names()
    
    # Use the "All Products" category if it exists, otherwise flatten the products manually
    if "All Products" in products_by_category:
        all_products = products_by_category["All Products"]
    else:
        all_products = []
        for category, products in products_by_category.items():
            all_products.extend(products)
    
    # Remove duplicates and ensure we have valid products
    all_products = list(set(all_products))
    
    # Handle case of no products
    if not all_products:
        print("Warning: No products found! Using default products")
        all_products = ["Savings Account", "Checking Account", "Credit Card"]
        
    # Print number of products available for selection
    print(f"Total unique products available for selection: {len(all_products)}")
    
    # Calculate probability factors
    income_factor = min(income / 100000, 1.0)  # Higher income, more products
    age_factor = min(age / 70, 1.0)  # Older customers have more products
    credit_factor = min((credit_score - 300) / 550, 1.0)  # Better credit, more products
    
    # Get total number of available products
    total_available = len(all_products)
    
    # Determine base number of products, but cap at available products
    if income_category == "High":
        max_base = min(7, total_available)
        base_products_count = random.randint(min(3, max_base), max_base) if max_base >= 3 else max_base
    elif income_category == "Medium":
        max_base = min(5, total_available)
        base_products_count = random.randint(min(2, max_base), max_base) if max_base >= 2 else max_base
    else:
        max_base = min(3, total_available)
        base_products_count = random.randint(min(1, max_base), max_base) if max_base >= 1 else max_base
    
    # Adjust based on factors, but ensure it's not greater than available products
    products_count = min(
        round(base_products_count * (1 + income_factor * 0.5 + age_factor * 0.3 + credit_factor * 0.2)),
        total_available
    )
    
    # Ensure at least 1 product, but no more than available
    products_count = max(1, min(products_count, total_available))
    
    # Select random products
    selected_products = random.sample(all_products, products_count)
    
    return selected_products

def setup_database(db_path="./db/local_customers.db"):
    """Create and populate the SQLite database with synthetic customer data in a single table."""
    fake = Faker()
    
    def generate_customers(n=70):
        data = []
        
        # Define income sources and categories
        income_sources = ["Employment", "Self-employment", "Business", "Investments", "Pension", "Rental", "Freelance"]
        
        for _ in range(n):
            customer_id = fake.random_int(min=10000000, max=99999999)
            gender = random.choice(["Male", "Female"])
            age = random.randint(18, 75)
            occupation = fake.job()
            
            # Add income based on age and random factors
            base_income = random.randint(20000, 40000)
            age_factor = min(2.5, max(1.0, age / 30))
            income = round(base_income * age_factor * random.uniform(0.8, 1.5), 2)
            
            # Assign income source and category
            income_source = random.choice(income_sources)
            
            # Determine income category based on income amount
            if income < 30000:
                income_category = "Low"
            elif income < 70000:
                income_category = "Medium"
            else:
                income_category = "High"
            
            # Add previous loans count
            previous_loans_count = random.randint(0, 5)
            
            credit_score = random.randint(300, 850)
            is_loan_eligible = credit_score >= 580

            eligible_loan_amount = 0.0
            if is_loan_eligible:
                if credit_score >= 750:
                    eligible_loan_amount = round(random.uniform(25000.0, 100000.0), 2)
                elif credit_score >= 670:
                    eligible_loan_amount = round(random.uniform(10000.0, 50000.0), 2)
                else:
                    eligible_loan_amount = round(random.uniform(1000.0, 25000.0), 2)
            
            loan_amount = 0.0
            loan_status = None
            loan_tenure = None
            loan_interest_rate = None
            loan_purpose = None
            loan_application_date = None
            
            if is_loan_eligible and random.random() > 0.4:
                loan_amount = min(round(random.uniform(1000.0, 50000.0), 2), eligible_loan_amount)
                loan_status = random.choice(["Pending", "Approved", "Active", "Closed"])
                loan_tenure = random.randint(6, 60)
                loan_interest_rate = calculate_loan_interest_rate(credit_score, loan_tenure, loan_amount)
                loan_purpose = random.choice(["Home", "Education", "Vehicle", "Personal", "Business"])
                loan_application_date = fake.date_time_between(start_date="-2y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate product holdings
            products = generate_product_holdings(income, age, credit_score, income_category)
            no_product_holding = len(products)
            
            # Calculate entrenchment score (percentage of products held vs potential products)
            # We'll assume total potential products is 23 based on the product_offerings.txt
            total_potential_products = 23
            entrenchment_score = round((no_product_holding / total_potential_products) * 100, 2)
            
            customer = {
                "id": customer_id,
                "full_name": fake.name(),
                "email": fake.email(),
                "phone_number": fake.phone_number(),
                "address": fake.address().replace("\n", ", "),
                "account_number": fake.unique.random_number(digits=10),
                "account_type": random.choice(["Savings", "Cheque", "Business"]),
                "balance": round(random.uniform(100.0, 50000.0), 2),
                "gender": gender,
                "age": age,
                "occupation": occupation,
                "income": income,
                "income_source": income_source,
                "income_category": income_category,
                "previous_loans_count": previous_loans_count,
                "credit_score": credit_score,
                "loan_eligible": is_loan_eligible,
                "eligible_loan_amount": eligible_loan_amount if is_loan_eligible else 0.0,
                "loan_amount_applied_for": loan_amount,
                "loan_status": loan_status if loan_amount > 0 else None,  # Ensure status is None when no loan applied
                "loan_tenure": loan_tenure,
                "loan_interest_rate": loan_interest_rate,
                "loan_purpose": loan_purpose,
                "loan_application_date": loan_application_date,
                "last_login": fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
                "product_holding": json.dumps(products),  # Store as JSON string
                "no_product_holding": no_product_holding,
                "entrenchment_score": entrenchment_score,
            }
            data.append(customer)
        
        return pd.DataFrame(data)

    conn = sqlite3.connect(db_path)
    customers_df = generate_customers()
    customers_df.to_sql("customer_information", conn, index=False, if_exists="replace")
    conn.commit()
    conn.close()
    print("Database setup complete with single customer_information table!")
    
    return customers_df  # Return the DataFrame for potential export to SQL Server

def export_to_sql_server(customers_df=None):
    """Export customer data to SQL Server using azure-data-studio.py script"""
    try:
        # Import needed modules
        import subprocess
        import sys
        
        # If no DataFrame provided, read from SQLite
        if customers_df is None:
            db_path = os.path.join(os.path.dirname(__file__), "local_customers.db")
            conn = sqlite3.connect(db_path)
            customers_df = pd.read_sql_query("SELECT * FROM customer_information", conn)
            conn.close()
        
        # Execute the azure-data-studio-copy.py script as a module (using the fixed version)
        script_path = os.path.join(os.path.dirname(__file__), "azure-data-studio-copy.py")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Data successfully exported to SQL Server!")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("Error exporting data to SQL Server:")
            if result.stderr:
                print("Error:", result.stderr)
            
    except Exception as e:
        print(f"Error exporting to SQL Server: {e}")

if __name__ == "__main__":
    customers_df = setup_database()
    
    # Ask if user wants to export to SQL Server
    export_choice = input("Do you want to export data to SQL Server? (y/n): ").strip().lower()
    if export_choice == 'y' or export_choice == 'Y':
        export_to_sql_server(customers_df)