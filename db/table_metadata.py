"""
Comprehensive Table Metadata for LLM SQL Query Generation
This file contains detailed metadata about the customer_information table structure,
data types, relationships, and common query patterns for use in LLM prompts.
"""

import json
from datetime import datetime

def get_customer_information_metadata():
    """
    Generate comprehensive metadata for the customer_information table
    to be used in LLM prompts for SQL query generation.
    """
    
    metadata = {
        "database_info": {
            "database_type": "SQL Server",
            "database_name": "master",
            "server": "localhost\\SQLEXPRESS",
            "schema": "dbo",
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        },
        
        "table_info": {
            "table_name": "customer_information",
            "full_table_name": "[dbo].[customer_information]",
            "description": "Comprehensive customer data table containing personal information, financial details, loan information, and product holdings for bank customers",
            "total_records": 70,  # Update this based on actual count
            "primary_key": "id",
            "creation_date": "2025-06-09"
        },
        
        "columns": [
            {
                "column_name": "id",
                "data_type": "int",
                "sql_type": "[int] NOT NULL",
                "is_nullable": False,
                "is_primary_key": True,
                "description": "Unique customer identifier, 8-digit number",
                "example_values": [10474206, 10962741, 13765547],
                "value_range": "10000000 to 99999999",
                "business_rules": "Auto-generated unique identifier for each customer"
            },
            {
                "column_name": "full_name",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](255) NOT NULL",
                "max_length": 255,
                "is_nullable": False,
                "description": "Customer's complete name (first and last name)",
                "example_values": ["Rachel Benitez", "Samuel Anderson", "Austin Perkins"],
                "business_rules": "Required field, contains customer's legal name"
            },
            {
                "column_name": "email",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](255) NULL",
                "max_length": 255,
                "is_nullable": True,
                "description": "Customer's email address for communication",
                "example_values": ["nelsoneddie@example.net", "dillonjodi@example.net"],
                "business_rules": "Must be valid email format, used for notifications"
            },
            {
                "column_name": "phone_number",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NULL",
                "max_length": 50,
                "is_nullable": True,
                "description": "Customer's contact phone number",
                "example_values": ["+1-555-123-4567", "(555) 987-6543"],
                "business_rules": "Various formats accepted, primary contact method"
            },
            {
                "column_name": "address",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](max) NULL",
                "max_length": "unlimited",
                "is_nullable": True,
                "description": "Customer's physical address (street, city, state, zip)",
                "example_values": ["123 Main St, Anytown, ST 12345"],
                "business_rules": "Complete postal address for correspondence"
            },
            {
                "column_name": "account_number",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](20) NULL",
                "max_length": 20,
                "is_nullable": True,
                "description": "Bank account number associated with the customer",
                "example_values": ["1234567890", "9876543210"],
                "business_rules": "10-digit unique account identifier"
            },
            {
                "column_name": "account_type",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NULL",
                "max_length": 50,
                "is_nullable": True,
                "description": "Type of bank account held by the customer",
                "example_values": ["Savings", "Cheque", "Business"],
                "valid_values": ["Savings", "Cheque", "Business"],
                "business_rules": "Determines account features and limitations"
            },
            {
                "column_name": "balance",
                "data_type": "decimal",
                "sql_type": "[decimal](18, 2) NULL",
                "precision": 18,
                "scale": 2,
                "is_nullable": True,
                "description": "Current account balance in local currency",
                "example_values": [8383.72, 19437.26, 45030.79],
                "value_range": "100.00 to 50000.00",
                "business_rules": "Updated in real-time with transactions, minimum balance varies by account type"
            },
            {
                "column_name": "gender",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](10) NULL",
                "max_length": 10,
                "is_nullable": True,
                "description": "Customer's gender identification",
                "example_values": ["Male", "Female"],
                "valid_values": ["Male", "Female"],
                "business_rules": "Used for demographic analysis and targeted marketing"
            },
            {
                "column_name": "age",
                "data_type": "int",
                "sql_type": "[int] NULL",
                "is_nullable": True,
                "description": "Customer's age in years",
                "example_values": [61, 30, 64],
                "value_range": "18 to 75",
                "business_rules": "Must be 18+ to open account, affects product eligibility"
            },
            {
                "column_name": "occupation",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](255) NULL",
                "max_length": 255,
                "is_nullable": True,
                "description": "Customer's current job title or profession",
                "example_values": ["English as a second language teacher", "Engineering geologist", "Information systems manager"],
                "business_rules": "Used for risk assessment and income verification"
            },
            {
                "column_name": "income",
                "data_type": "decimal",
                "sql_type": "[decimal](18, 2) NULL",
                "precision": 18,
                "scale": 2,
                "is_nullable": True,
                "description": "Customer's annual income in local currency",
                "example_values": [45000.00, 32000.00, 85000.00],
                "value_range": "20000.00 to 150000.00",
                "business_rules": "Used for loan eligibility and credit limit determination"
            },
            {
                "column_name": "income_source",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](100) NULL",
                "max_length": 100,
                "is_nullable": True,
                "description": "Primary source of customer's income",
                "example_values": ["Employment", "Self-employment", "Business", "Investments"],
                "valid_values": ["Employment", "Self-employment", "Business", "Investments", "Pension", "Rental", "Freelance"],
                "business_rules": "Affects income stability assessment for lending"
            },
            {
                "column_name": "income_category",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NULL",
                "max_length": 50,
                "is_nullable": True,
                "description": "Income classification based on amount",
                "example_values": ["Low", "Medium", "High"],
                "valid_values": ["Low", "Medium", "High"],
                "calculation_rules": "Low: <30K, Medium: 30K-70K, High: >70K",
                "business_rules": "Determines product offerings and credit limits"
            },
            {
                "column_name": "previous_loans_count",
                "data_type": "int",
                "sql_type": "[int] NULL",
                "is_nullable": True,
                "description": "Number of previous loans taken by the customer",
                "example_values": [0, 2, 5],
                "value_range": "0 to 5",
                "business_rules": "Higher count may affect future loan approval"
            },
            {
                "column_name": "credit_score",
                "data_type": "int",
                "sql_type": "[int] NULL",
                "is_nullable": True,
                "description": "Customer's credit score based on credit history",
                "example_values": [718, 807, 511],
                "value_range": "300 to 850",
                "scoring_ranges": {
                    "Poor": "300-579",
                    "Fair": "580-669", 
                    "Good": "670-739",
                    "Very Good": "740-799",
                    "Excellent": "800-850"
                },
                "business_rules": "Primary factor in loan approval and interest rate determination"
            },
            {
                "column_name": "loan_eligible",
                "data_type": "bit",
                "sql_type": "[bit] NULL",
                "is_nullable": True,
                "description": "Boolean indicating if customer is eligible for loans",
                "example_values": [1, 0],
                "valid_values": [0, 1],
                "calculation_rules": "1 if credit_score >= 580, 0 otherwise",
                "business_rules": "Determines access to lending products"
            },
            {
                "column_name": "eligible_loan_amount",
                "data_type": "decimal",
                "sql_type": "[decimal](18, 2) NULL",
                "precision": 18,
                "scale": 2,
                "is_nullable": True,
                "description": "Maximum loan amount customer is eligible for",
                "example_values": [25000.00, 50000.00, 100000.00],
                "calculation_rules": "Based on credit score: 750+: 25K-100K, 670-749: 10K-50K, 580-669: 1K-25K",
                "business_rules": "Sets upper limit for loan applications"
            },
            {
                "column_name": "loan_amount_applied_for",
                "data_type": "decimal",
                "sql_type": "[decimal](18, 2) NULL",
                "precision": 18,
                "scale": 2,
                "is_nullable": True,
                "description": "Amount of loan currently applied for or received",
                "example_values": [15000.00, 30000.00, 0.00],
                "business_rules": "Cannot exceed eligible_loan_amount, 0 if no loan application"
            },
            {
                "column_name": "loan_status",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NULL",
                "max_length": 50,
                "is_nullable": True,
                "description": "Current status of loan application or existing loan",
                "example_values": ["Active", "Pending", "Approved", "Closed"],
                "valid_values": ["Pending", "Approved", "Active", "Closed", None],
                "status_meanings": {
                    "Pending": "Application under review",
                    "Approved": "Loan approved but not yet disbursed",
                    "Active": "Loan is currently being repaid",
                    "Closed": "Loan has been fully repaid",
                    "None": "No current loan"
                },
                "business_rules": "NULL if no loan application"
            },
            {
                "column_name": "loan_tenure",
                "data_type": "int",
                "sql_type": "[int] NULL",
                "is_nullable": True,
                "description": "Loan repayment period in months",
                "example_values": [12, 24, 60],
                "value_range": "6 to 60 months",
                "business_rules": "Longer tenure increases interest rate, NULL if no loan"
            },
            {
                "column_name": "loan_interest_rate",
                "data_type": "decimal",
                "sql_type": "[decimal](5, 2) NULL",
                "precision": 5,
                "scale": 2,
                "is_nullable": True,
                "description": "Annual interest rate for the loan as a percentage",
                "example_values": [7.50, 12.25, 15.00],
                "value_range": "3.50% to 20.00%",
                "calculation_factors": "Based on credit score, loan tenure, and loan amount",
                "business_rules": "NULL if no loan, calculated using risk-based pricing"
            },
            {
                "column_name": "loan_purpose",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](100) NULL",
                "max_length": 100,
                "is_nullable": True,
                "description": "Reason for taking the loan",
                "example_values": ["Home", "Education", "Vehicle", "Personal", "Business"],
                "valid_values": ["Home", "Education", "Vehicle", "Personal", "Business"],
                "business_rules": "Required for loan applications, affects interest rates"
            },
            {
                "column_name": "loan_application_date",
                "data_type": "datetime",
                "sql_type": "[datetime] NULL",
                "is_nullable": True,
                "description": "Date when loan application was submitted",
                "example_values": ["2023-05-15 10:30:00", "2024-01-20 14:45:00"],
                "format": "YYYY-MM-DD HH:MM:SS",
                "business_rules": "NULL if no loan application, within last 2 years"
            },
            {
                "column_name": "last_login",
                "data_type": "datetime",
                "sql_type": "[datetime] NULL",
                "is_nullable": True,
                "description": "Last time customer accessed online banking",
                "example_values": ["2025-06-08 09:15:00", "2025-06-07 18:30:00"],
                "format": "YYYY-MM-DD HH:MM:SS",
                "business_rules": "Used to track customer engagement and activity"
            },
            {
                "column_name": "product_holding",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](max) NULL",
                "max_length": "unlimited",
                "is_nullable": True,
                "description": "JSON array of bank products held by the customer",
                "example_values": [
                    '["Checking Account", "Overdraft Protection", "Foreign Currency Exchange"]',
                    '["Investment Advisory Services"]',
                    '["Home Mortgages", "Insurance Products", "Savings Account"]'
                ],
                "data_format": "JSON array of strings",
                "product_categories": {
                    "Deposit Products": ["Savings Account", "Checking Account", "Certificates of Deposit (CDs)"],
                    "Credit Products": ["Personal Loans", "Auto Loans", "Home Mortgages", "Credit Cards", "Overdraft Protection"],
                    "Investment Products": ["Brokerage Accounts", "Retirement Accounts (IRA, 401k)", "Investment Advisory Services"],
                    "Service Products": ["Mobile & Online Banking", "Foreign Currency Exchange", "Safe Deposit Boxes", "Insurance Products"]
                },
                "business_rules": "Determines cross-selling opportunities and customer value"
            },
            {
                "column_name": "no_product_holding",
                "data_type": "int",
                "sql_type": "[int] NULL",
                "is_nullable": True,
                "description": "Count of products currently held by the customer",
                "example_values": [3, 1, 9],
                "value_range": "1 to 15",
                "calculation": "COUNT of items in product_holding JSON array",
                "business_rules": "Higher count indicates deeper customer relationship"
            },
            {
                "column_name": "entrenchment_score",
                "data_type": "decimal",
                "sql_type": "[decimal](5, 2) NULL",
                "precision": 5,
                "scale": 2,
                "is_nullable": True,
                "description": "Percentage of total available products held by customer",
                "example_values": [13.04, 4.35, 39.13],
                "value_range": "0.00% to 100.00%",
                "calculation": "(no_product_holding / 23) * 100",
                "business_rules": "Higher score indicates stronger customer relationship and retention likelihood"
            }
        ],
        
        "relationships": {
            "internal_relationships": [
                {
                    "type": "calculated_field",
                    "source": "credit_score",
                    "target": "loan_eligible",
                    "rule": "loan_eligible = 1 if credit_score >= 580, else 0"
                },
                {
                    "type": "calculated_field",
                    "source": "income",
                    "target": "income_category", 
                    "rule": "Low: <30K, Medium: 30K-70K, High: >70K"
                },
                {
                    "type": "calculated_field",
                    "source": "product_holding",
                    "target": "no_product_holding",
                    "rule": "COUNT of JSON array items"
                },
                {
                    "type": "calculated_field",
                    "source": "no_product_holding",
                    "target": "entrenchment_score",
                    "rule": "(no_product_holding / 23) * 100"
                },
                {
                    "type": "constraint",
                    "rule": "loan_amount_applied_for <= eligible_loan_amount"
                },
                {
                    "type": "constraint", 
                    "rule": "loan_interest_rate calculated from credit_score, loan_tenure, loan_amount"
                }
            ]
        },
        
        "common_queries": {
            "customer_search": [
                "SELECT * FROM customer_information WHERE full_name LIKE '%{name}%'",
                "SELECT * FROM customer_information WHERE email = '{email}'",
                "SELECT * FROM customer_information WHERE id = {customer_id}"
            ],
            "financial_analysis": [
                "SELECT AVG(balance) as avg_balance, income_category FROM customer_information GROUP BY income_category",
                "SELECT COUNT(*) as customer_count, credit_score FROM customer_information WHERE credit_score BETWEEN {min} AND {max}",
                "SELECT * FROM customer_information WHERE balance > {amount} ORDER BY balance DESC"
            ],
            "loan_analysis": [
                "SELECT * FROM customer_information WHERE loan_status = 'Active'",
                "SELECT AVG(loan_interest_rate) as avg_rate, loan_purpose FROM customer_information WHERE loan_status IS NOT NULL GROUP BY loan_purpose",
                "SELECT * FROM customer_information WHERE loan_eligible = 1 AND loan_status IS NULL"
            ],
            "product_analysis": [
                "SELECT * FROM customer_information WHERE JSON_VALUE(product_holding, '$') LIKE '%{product_name}%'",
                "SELECT AVG(no_product_holding) as avg_products, income_category FROM customer_information GROUP BY income_category",
                "SELECT * FROM customer_information WHERE entrenchment_score > {threshold} ORDER BY entrenchment_score DESC"
            ],
            "demographic_analysis": [
                "SELECT COUNT(*) as count, gender, age FROM customer_information GROUP BY gender, age",
                "SELECT AVG(income) as avg_income, occupation FROM customer_information GROUP BY occupation HAVING COUNT(*) > 1",
                "SELECT * FROM customer_information WHERE age BETWEEN {min_age} AND {max_age}"
            ]
        },
        
        "query_tips": {
            "json_handling": [
                "Use JSON_VALUE() or OPENJSON() to query product_holding column",
                "Example: JSON_VALUE(product_holding, '$[0]') gets first product",
                "Use LIKE '%product_name%' for simple product searches in JSON"
            ],
            "date_handling": [
                "Use DATEPART() for extracting year, month, day from datetime fields",
                "Use DATEDIFF() to calculate time differences",
                "Format: 'YYYY-MM-DD HH:MM:SS' for datetime comparisons"
            ],
            "aggregations": [
                "Common aggregations: COUNT(), AVG(), SUM(), MIN(), MAX()",
                "Use GROUP BY for categorical analysis",
                "Use HAVING for filtered aggregations"
            ],
            "performance": [
                "Index exists on primary key (id)",
                "Consider filtering by indexed columns first",
                "Use appropriate data types in WHERE clauses"
            ]
        }
    }
    
    return metadata

def generate_llm_prompt_metadata():
    """
    Generate formatted metadata specifically for LLM prompts.
    Returns a formatted string ready to be used in text-to-SQL prompts.
    """
    metadata = get_customer_information_metadata()
    
    prompt_metadata = f"""
# Database Schema Information

## Database Details
- **Database**: {metadata['database_info']['database_type']} ({metadata['database_info']['database_name']})
- **Server**: {metadata['database_info']['server']}
- **Schema**: {metadata['database_info']['schema']}

## Table: {metadata['table_info']['table_name']}
{metadata['table_info']['description']}

### Table Structure
**Full Name**: {metadata['table_info']['full_table_name']}
**Records**: ~{metadata['table_info']['total_records']} customers
**Primary Key**: {metadata['table_info']['primary_key']}

### Column Definitions

"""
      # Add column information
    for col in metadata['columns']:
        prompt_metadata += f"**{col['column_name']}** ({col['data_type']})\n"
        prompt_metadata += f"- Description: {col['description']}\n"
        
        if 'valid_values' in col:
            prompt_metadata += f"- Valid Values: {', '.join(str(v) for v in col['valid_values'])}\n"
        
        if 'value_range' in col:
            prompt_metadata += f"- Range: {col['value_range']}\n"
            
        if 'example_values' in col:
            examples = ', '.join([str(v) for v in col['example_values'][:3]])
            prompt_metadata += f"- Examples: {examples}\n"
            
        if 'business_rules' in col:
            prompt_metadata += f"- Rules: {col['business_rules']}\n"
            
        prompt_metadata += "\n"
    
    # Add important relationships
    prompt_metadata += "### Key Relationships & Rules\n\n"
    for rel in metadata['relationships']['internal_relationships']:
        if rel['type'] == 'calculated_field':
            prompt_metadata += f"- **{rel['target']}** is calculated from **{rel['source']}**: {rel['rule']}\n"
        elif rel['type'] == 'constraint':
            prompt_metadata += f"- Constraint: {rel['rule']}\n"
    
    # Add query examples
    prompt_metadata += "\n### Common Query Patterns\n\n"
    
    for category, queries in metadata['common_queries'].items():
        prompt_metadata += f"**{category.replace('_', ' ').title()}:**\n"
        for query in queries[:2]:  # Show first 2 examples
            prompt_metadata += f"```sql\n{query}\n```\n"
        prompt_metadata += "\n"
    
    # Add important tips
    prompt_metadata += "### Query Tips\n\n"
    for tip_category, tips in metadata['query_tips'].items():
        prompt_metadata += f"**{tip_category.replace('_', ' ').title()}:**\n"
        for tip in tips:
            prompt_metadata += f"- {tip}\n"
        prompt_metadata += "\n"
    
    return prompt_metadata

def save_metadata_files():
    """Save metadata in multiple formats for different use cases"""
    
    # Save complete metadata as JSON
    metadata = get_customer_information_metadata()
    with open('customer_table_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
    
    # Save LLM prompt version as text
    prompt_metadata = generate_llm_prompt_metadata()
    with open('customer_table_metadata_for_llm.md', 'w', encoding='utf-8') as f:
        f.write(prompt_metadata)
    
    print("Metadata files generated:")
    print("- customer_table_metadata.json (Complete metadata)")
    print("- customer_table_metadata_for_llm.md (LLM prompt format)")

if __name__ == "__main__":
    save_metadata_files()
    
    # Also print the LLM version for immediate use
    print("\n" + "="*80)
    print("LLM PROMPT METADATA")
    print("="*80)
    print(generate_llm_prompt_metadata())
