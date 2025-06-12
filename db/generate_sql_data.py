import pandas as pd
import numpy as np
import os
import sys
import json
import pyodbc
import random
from faker import Faker
from datetime import datetime, timedelta
import re

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def connect_to_sql_server():
    """Connect to SQL Server using pyodbc"""
    server = os.environ.get("server_data_studio")  # Default to localhost if not set
    database = os.environ.get("database")  # You might want to change this to a specific database
    username = os.environ.get("administrator") 
    administrator = os.environ.get("administrator") 
    password = os.environ.get("password_server_data_studio")
    
    if not password:
        password = os.environ.get("password")  # Try lowercase version
        if not password:
            print("Error: SQL Server password not found in environment variables.")
            print("Please set the PASSWORD environment variable.")
            sys.exit(1)
    
    try:
        # Build connection string
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print(f"Successfully connected to SQL Server database: {database}")
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")
        sys.exit(1)

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

def generate_customer_data(n=70):
    """Generate synthetic customer data"""
    fake = Faker()
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
            "loan_status": loan_status if loan_amount > 0 else None,
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

def create_sql_server_table(cursor, table_name="customer_information"):
    """Create table in SQL Server if it doesn't exist"""
    try:
        # Drop table if exists to recreate it
        cursor.execute(f"""
        IF OBJECT_ID(N'dbo.{table_name}', N'U') IS NOT NULL
            DROP TABLE [dbo].[{table_name}]
        """)
        
        # Create table
        sql_create_table = f"""
        CREATE TABLE [dbo].[{table_name}] (
            [id] [int] NOT NULL,
            [full_name] [nvarchar](255) NOT NULL,
            [email] [nvarchar](255) NULL,
            [phone_number] [nvarchar](50) NULL,
            [address] [nvarchar](max) NULL,
            [account_number] [nvarchar](20) NULL,
            [account_type] [nvarchar](50) NULL,
            [balance] [decimal](18, 2) NULL,
            [gender] [nvarchar](10) NULL,
            [age] [int] NULL,
            [occupation] [nvarchar](255) NULL,
            [income] [decimal](18, 2) NULL,
            [income_source] [nvarchar](100) NULL,
            [income_category] [nvarchar](50) NULL,
            [previous_loans_count] [int] NULL,
            [credit_score] [int] NULL,
            [loan_eligible] [bit] NULL,
            [eligible_loan_amount] [decimal](18, 2) NULL,
            [loan_amount_applied_for] [decimal](18, 2) NULL,
            [loan_status] [nvarchar](50) NULL,
            [loan_tenure] [int] NULL,
            [loan_interest_rate] [decimal](5, 2) NULL,
            [loan_purpose] [nvarchar](100) NULL,
            [loan_application_date] [datetime] NULL,
            [last_login] [datetime] NULL,
            [product_holding] [nvarchar](max) NULL,
            [no_product_holding] [int] NULL,
            [entrenchment_score] [decimal](5, 2) NULL,
            CONSTRAINT [PK_{table_name}] PRIMARY KEY CLUSTERED ([id] ASC)
        )
        """
        cursor.execute(sql_create_table)
        cursor.commit()
        print(f"Table '{table_name}' created in SQL Server")
    except Exception as e:
        print(f"Error creating SQL Server table: {e}")
        sys.exit(1)

def insert_data_into_sql_server(conn, cursor, df, table_name="customer_information"):
    """Insert data from DataFrame into SQL Server table"""
    try:
        # Print debug information about DataFrame columns
        print(f"DataFrame columns: {df.columns.tolist()}")
        print(f"product_holding type: {df['product_holding'].dtype}")
        print(f"Sample product_holding: {df['product_holding'].iloc[0]}")
        
        # Insert data row by row
        count = 0
        for index, row in df.iterrows():
            try:
                # Convert loan_eligible to bit (0/1)
                loan_eligible_bit = 1 if row['loan_eligible'] else 0
                
                # Handle NULL values for dates
                loan_application_date = row['loan_application_date'] if pd.notna(row['loan_application_date']) else None
                last_login = row['last_login'] if pd.notna(row['last_login']) else None
                
                # Handle product_holding - ensure it's a string for SQL Server
                # In SQLite, it's stored as a JSON string but might be parsed as a Python object in pandas
                product_holding_str = row['product_holding']
                if pd.notna(product_holding_str):
                    # If it's already a string but contains object notation, keep it as is
                    # If it's a Python object (list, dict), convert it to a JSON string
                    if isinstance(product_holding_str, (list, dict)):
                        product_holding_str = json.dumps(product_holding_str)
                    # Otherwise, ensure it's a string
                    elif not isinstance(product_holding_str, str):
                        product_holding_str = str(product_holding_str)
                else:
                    product_holding_str = None
                    
                # Insert query with pyodbc parameter style (?)
                insert_query = f"""
                INSERT INTO [dbo].[{table_name}] (
                    [id], [full_name], [email], [phone_number], [address], [account_number], [account_type], 
                    [balance], [gender], [age], [occupation], [income], [income_source], [income_category], 
                    [previous_loans_count], [credit_score], [loan_eligible], [eligible_loan_amount], 
                    [loan_amount_applied_for], [loan_status], [loan_tenure], [loan_interest_rate], [loan_purpose], 
                    [loan_application_date], [last_login], [product_holding], [no_product_holding], [entrenchment_score]
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                cursor.execute(insert_query, (
                    int(row['id']), 
                    row['full_name'], 
                    row['email'], 
                    row['phone_number'], 
                    row['address'], 
                    row['account_number'], 
                    row['account_type'],
                    float(row['balance']), 
                    row['gender'], 
                    int(row['age']), 
                    row['occupation'], 
                    float(row['income']), 
                    row['income_source'], 
                    row['income_category'],
                    int(row['previous_loans_count']), 
                    int(row['credit_score']), 
                    loan_eligible_bit, 
                    float(row['eligible_loan_amount']),
                    float(row['loan_amount_applied_for']), 
                    row['loan_status'], 
                    None if pd.isna(row['loan_tenure']) else int(row['loan_tenure']), 
                    None if pd.isna(row['loan_interest_rate']) else float(row['loan_interest_rate']), 
                    row['loan_purpose'],
                    loan_application_date, 
                    last_login, 
                    product_holding_str, 
                    int(row['no_product_holding']), 
                    float(row['entrenchment_score'])
                ))
                
                count += 1
                
                # Commit every 100 records to avoid large transactions
                if count % 100 == 0:
                    conn.commit()
                    print(f"Inserted {count} records...")
            except Exception as e:
                print(f"Error inserting row {index} with ID {row['id']}: {e}")
                print(f"Problem row data: {row}")
                continue
        
        # Final commit
        conn.commit()
        print(f"Successfully inserted {count} records into SQL Server table '{table_name}'")
    except Exception as e:
        print(f"Error inserting data into SQL Server: {e}")
        conn.rollback()
        sys.exit(1)

def verify_sql_server_data(conn, cursor, table_name="customer_information"):
    """Verify that data was successfully inserted into SQL Server"""
    try:
        # Get count of records
        cursor.execute(f"SELECT COUNT(*) FROM [dbo].[{table_name}]")
        count = cursor.fetchone()[0]
        print(f"Verification: {count} records found in SQL Server table '{table_name}'")
        
        # Get sample data
        cursor.execute(f"SELECT TOP 1 * FROM [dbo].[{table_name}]")
        row = cursor.fetchone()
        if row:
            print("First record successfully retrieved from SQL Server")
        return count
    except Exception as e:
        print(f"Error verifying SQL Server data: {e}")
        return 0

def main():
    """Main function to generate data and create SQL Server table"""
    # Connect to SQL Server
    conn, cursor = connect_to_sql_server()
    
    # Generate customer data
    print("Generating customer data...")
    df = generate_customer_data(n=70)  # Generate 70 customers
    print(f"Generated {len(df)} customer records")
    
    # Create table in SQL Server
    create_sql_server_table(cursor)
    
    # Insert data into SQL Server
    insert_data_into_sql_server(conn, cursor, df)
    
    # Verify the data was inserted correctly
    verify_sql_server_data(conn, cursor)
    
    # Close SQL Server connection
    cursor.close()
    conn.close()
    print("Data generation and loading complete!")

if __name__ == "__main__":
    main()