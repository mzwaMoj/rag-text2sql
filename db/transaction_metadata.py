"""
Comprehensive Transaction History Table Metadata for LLM SQL Query Generation
This file contains detailed metadata about the transaction_history table structure,
data types, relationships, and common query patterns for use in LLM prompts.
"""

import json
from datetime import datetime

def get_transaction_history_metadata():
    """
    Generate comprehensive metadata for the transaction_history table
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
            "table_name": "transaction_history",
            "full_table_name": "[dbo].[transaction_history]",
            "description": "Comprehensive transaction history table containing all customer financial transactions including deposits, withdrawals, transfers, payments, and purchases",
            "total_records": "5000+",  # Configurable based on user input
            "primary_key": "transaction_id",
            "foreign_keys": ["customer_id"],
            "creation_date": "2025-06-09",
            "time_range": "Last 2 years of transaction data"
        },
        
        "columns": [
            {
                "column_name": "transaction_id",
                "data_type": "bigint",
                "sql_type": "[bigint] NOT NULL",
                "is_nullable": False,
                "is_primary_key": True,
                "description": "Unique transaction identifier, 12-digit number",
                "example_values": [679551814302, 376513881618, 994709101726],
                "value_range": "100000000000 to 999999999999",
                "business_rules": "Auto-generated unique identifier for each transaction"
            },
            {
                "column_name": "customer_id",
                "data_type": "int",
                "sql_type": "[int] NOT NULL",
                "is_nullable": False,
                "is_foreign_key": True,
                "references": "customer_information.id",
                "description": "Customer identifier linking to customer_information table",
                "example_values": [10000001, 10000002, 10000003],
                "value_range": "10000000 to 99999999",
                "business_rules": "Must exist in customer_information table"
            },
            {
                "column_name": "transaction_date",
                "data_type": "datetime",
                "sql_type": "[datetime] NOT NULL",
                "is_nullable": False,
                "description": "Date and time when the transaction occurred",
                "example_values": ["2023-06-15 14:30:22", "2024-11-28 09:15:45", "2025-01-12 16:45:33"],
                "date_range": "2023-06-09 to present",
                "business_rules": "Cannot be future date, used for transaction ordering and reporting"
            },
            {
                "column_name": "transaction_type",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NOT NULL",
                "max_length": 50,
                "is_nullable": False,
                "description": "Type of transaction performed",
                "example_values": ["Deposit", "Withdrawal", "Transfer", "Payment", "Purchase"],
                "valid_values": ["Deposit", "Withdrawal", "Transfer", "Payment", "Purchase", "Refund", "Fee", "Interest", "Loan Payment", "Salary"],
                "business_rules": "Determines transaction processing rules and account impact"
            },
            {
                "column_name": "amount",
                "data_type": "decimal",
                "sql_type": "[decimal](18, 2) NOT NULL",
                "precision": 18,
                "scale": 2,
                "is_nullable": False,
                "description": "Transaction amount in specified currency (negative for debits, positive for credits)",
                "example_values": [1500.50, -89.99, 25000.00, -1250.75],
                "value_range": "-100000.00 to 100000.00",
                "business_rules": "Negative values represent debits (withdrawals, payments, fees), positive values represent credits (deposits, refunds, interest)"
            },
            {
                "column_name": "currency",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](3) NOT NULL",
                "max_length": 3,
                "is_nullable": False,
                "description": "ISO 4217 currency code for the transaction",
                "example_values": ["ZAR", "USD", "EUR", "GBP"],
                "valid_values": ["ZAR", "USD", "EUR", "GBP", "JPY"],
                "business_rules": "Primarily ZAR (85%), with some international currencies for forex transactions"
            },
            {
                "column_name": "description",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](500) NULL",
                "max_length": 500,
                "is_nullable": True,
                "description": "Human-readable description of the transaction",
                "example_values": ["Groceries purchase at Woolworths", "Transfer to John Smith", "Salary payment from ABC Corp"],
                "business_rules": "Auto-generated based on transaction type and context"
            },
            {
                "column_name": "category",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](100) NULL",
                "max_length": 100,
                "is_nullable": True,
                "description": "Transaction category for spending analysis",
                "example_values": ["Groceries", "Gas", "Restaurant", "Shopping", "Utilities"],
                "valid_values": ["Groceries", "Gas", "Restaurant", "Shopping", "Utilities", "Healthcare", "Entertainment", "Travel", "Education", "Insurance", "Banking", "Investment", "Salary", "Bonus", "Refund", "Other"],
                "business_rules": "Used for budgeting and spending pattern analysis"
            },
            {
                "column_name": "channel",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NULL",
                "max_length": 50,
                "is_nullable": True,
                "description": "Channel through which the transaction was made",
                "example_values": ["ATM", "Online Banking", "Mobile App", "Branch"],
                "valid_values": ["ATM", "Online Banking", "Mobile App", "Branch", "POS Terminal", "Wire Transfer", "ACH", "Check", "Direct Deposit"],
                "business_rules": "Tracks customer behavior and channel preference"
            },
            {
                "column_name": "status",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](20) NOT NULL",
                "max_length": 20,
                "is_nullable": False,
                "description": "Current status of the transaction",
                "example_values": ["Completed", "Pending", "Failed", "Cancelled"],
                "valid_values": ["Completed", "Pending", "Failed", "Cancelled"],
                "business_rules": "Only Completed transactions affect account balance"
            },
            {
                "column_name": "reference_number",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](50) NULL",
                "max_length": 50,
                "is_nullable": True,
                "description": "Unique reference number for transaction tracking",
                "example_values": ["REF1234AB5678", "REF9876XY1234"],
                "pattern": "REF####??####",
                "business_rules": "Used for transaction inquiries and dispute resolution"
            },
            {
                "column_name": "merchant_name",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](255) NULL",
                "max_length": 255,
                "is_nullable": True,
                "description": "Name of merchant for purchase and payment transactions",
                "example_values": ["Woolworths", "Shell Garage", "Amazon", "Pick n Pay"],
                "business_rules": "Only populated for Purchase and Payment transaction types"
            },
            {
                "column_name": "merchant_category",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](100) NULL",
                "max_length": 100,
                "is_nullable": True,
                "description": "Category of merchant for purchase and payment transactions",
                "example_values": ["Groceries", "Gas", "Shopping", "Utilities"],
                "business_rules": "Matches category field for Purchase and Payment transactions"
            },
            {
                "column_name": "account_from",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](20) NULL",
                "max_length": 20,
                "is_nullable": True,
                "description": "Source account number for the transaction",
                "example_values": ["1234567890", "9876543210"],
                "business_rules": "10-digit account number, links to customer's account"
            },
            {
                "column_name": "account_to",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](20) NULL",
                "max_length": 20,
                "is_nullable": True,
                "description": "Destination account number for transfer transactions",
                "example_values": ["5555666677", "1111222233"],
                "business_rules": "Only populated for Transfer transaction types"
            },
            {
                "column_name": "balance_after",
                "data_type": "decimal",
                "sql_type": "[decimal](18, 2) NULL",
                "precision": 18,
                "scale": 2,
                "is_nullable": True,
                "description": "Account balance after the transaction was processed",
                "example_values": [15420.50, 8750.25, 45000.00],
                "value_range": "0.00 to 100000.00",
                "business_rules": "Snapshot of balance immediately after transaction completion"
            },
            {
                "column_name": "location",
                "data_type": "nvarchar",
                "sql_type": "[nvarchar](255) NULL",
                "max_length": 255,
                "is_nullable": True,
                "description": "Geographic location where the transaction occurred",
                "example_values": ["Johannesburg, South Africa", "Cape Town, South Africa", "London, United Kingdom"],
                "business_rules": "Used for fraud detection and geographic spending analysis"
            },
            {
                "column_name": "created_at",
                "data_type": "datetime",
                "sql_type": "[datetime] NOT NULL",
                "is_nullable": False,
                "description": "Timestamp when the transaction record was created in the system",
                "example_values": ["2025-06-09 10:30:22", "2025-06-09 11:15:45"],
                "business_rules": "System audit field, automatically populated"
            },
            {
                "column_name": "updated_at",
                "data_type": "datetime",
                "sql_type": "[datetime] NOT NULL",
                "is_nullable": False,
                "description": "Timestamp when the transaction record was last updated",
                "example_values": ["2025-06-09 10:30:22", "2025-06-09 11:15:45"],
                "business_rules": "System audit field, automatically updated on changes"
            }
        ],
        
        "relationships": {
            "foreign_keys": [
                {
                    "column": "customer_id",
                    "references_table": "customer_information",
                    "references_column": "id",
                    "relationship_type": "many_to_one",
                    "description": "Each transaction belongs to one customer, customers can have many transactions"
                }
            ],
            
            "internal_relationships": [
                {
                    "type": "conditional_field",
                    "source": "transaction_type",
                    "target": "merchant_name",
                    "rule": "merchant_name is only populated when transaction_type is 'Purchase' or 'Payment'"
                },
                {
                    "type": "conditional_field",
                    "source": "transaction_type",
                    "target": "account_to",
                    "rule": "account_to is only populated when transaction_type is 'Transfer'"
                },
                {
                    "type": "sign_convention",
                    "field": "amount",
                    "rule": "Negative amounts for debits (Withdrawal, Payment, Purchase, Fee, Loan Payment), positive for credits (Deposit, Salary, Interest, Refund)"
                },
                {
                    "type": "status_constraint",
                    "field": "balance_after",
                    "rule": "balance_after only reflects completed transactions, not pending/failed ones"
                }
            ]
        },
        
        "indexes": [
            {
                "name": "PK_transaction_history",
                "type": "PRIMARY KEY",
                "columns": ["transaction_id"],
                "description": "Primary key constraint"
            },
            {
                "name": "IX_transaction_history_customer_id",
                "type": "INDEX",
                "columns": ["customer_id"],
                "description": "Index for customer-based queries"
            },
            {
                "name": "IX_transaction_history_date",
                "type": "INDEX", 
                "columns": ["transaction_date"],
                "description": "Index for date range queries"
            },
            {
                "name": "IX_transaction_history_type_status",
                "type": "INDEX",
                "columns": ["transaction_type", "status"],
                "description": "Composite index for transaction type and status queries"
            }
        ],
        
        "common_queries": {
            "customer_transactions": [
                "SELECT * FROM [dbo].[transaction_history] WHERE customer_id = ? ORDER BY transaction_date DESC",
                "SELECT transaction_type, SUM(amount) as total FROM [dbo].[transaction_history] WHERE customer_id = ? AND status = 'Completed' GROUP BY transaction_type"
            ],
            
            "date_range_queries": [
                "SELECT * FROM [dbo].[transaction_history] WHERE transaction_date BETWEEN ? AND ? ORDER BY transaction_date DESC",
                "SELECT customer_id, COUNT(*) as transaction_count, SUM(amount) as total_amount FROM [dbo].[transaction_history] WHERE transaction_date >= DATEADD(month, -1, GETDATE()) GROUP BY customer_id"
            ],
            
            "transaction_analysis": [
                "SELECT transaction_type, category, AVG(amount) as avg_amount, COUNT(*) as count FROM [dbo].[transaction_history] WHERE status = 'Completed' GROUP BY transaction_type, category",
                "SELECT channel, COUNT(*) as usage_count FROM [dbo].[transaction_history] WHERE status = 'Completed' GROUP BY channel ORDER BY usage_count DESC"
            ],
            
            "spending_patterns": [
                "SELECT category, SUM(ABS(amount)) as total_spent FROM [dbo].[transaction_history] WHERE amount < 0 AND status = 'Completed' GROUP BY category ORDER BY total_spent DESC",
                "SELECT DATEPART(month, transaction_date) as month, SUM(amount) as net_flow FROM [dbo].[transaction_history] WHERE status = 'Completed' GROUP BY DATEPART(month, transaction_date)"
            ],
            
            "merchant_analysis": [
                "SELECT merchant_name, COUNT(*) as transaction_count, SUM(ABS(amount)) as total_spent FROM [dbo].[transaction_history] WHERE merchant_name IS NOT NULL AND status = 'Completed' GROUP BY merchant_name ORDER BY total_spent DESC",
                "SELECT merchant_category, AVG(ABS(amount)) as avg_transaction FROM [dbo].[transaction_history] WHERE merchant_category IS NOT NULL AND status = 'Completed' GROUP BY merchant_category"
            ],
            
            "balance_tracking": [
                "SELECT transaction_date, balance_after FROM [dbo].[transaction_history] WHERE customer_id = ? ORDER BY transaction_date DESC",
                "SELECT customer_id, MAX(balance_after) as peak_balance, MIN(balance_after) as lowest_balance FROM [dbo].[transaction_history] WHERE balance_after IS NOT NULL GROUP BY customer_id"
            ]
        },
        
        "query_tips": {
            "performance_tips": [
                "Always use indexes on customer_id and transaction_date for better performance",
                "Filter by status = 'Completed' when calculating balances or totals",
                "Use date range filters to limit large result sets",
                "Consider using EXISTS instead of IN when joining with customer table"
            ],
            
            "data_interpretation": [
                "Negative amounts represent money leaving the account (debits)",
                "Positive amounts represent money entering the account (credits)", 
                "Only 'Completed' transactions should be used for balance calculations",
                "merchant_name and merchant_category are only populated for Purchase/Payment types",
                "account_to is only populated for Transfer transactions"
            ],
            
            "common_patterns": [
                "Use SUM(amount) for net flow analysis (positive = net inflow, negative = net outflow)",
                "Use SUM(ABS(amount)) WHERE amount < 0 for total spending analysis",
                "Use SUM(amount) WHERE amount > 0 for total deposits/income analysis",
                "Group by DATEPART functions for time-based analysis (day, month, year)"
            ],
            
            "aggregation_tips": [
                "Use COUNT(*) for transaction frequency analysis",
                "Use AVG(ABS(amount)) for average transaction size by category",
                "Use MAX(transaction_date) to find most recent transaction per customer",
                "Use ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date DESC) for latest N transactions per customer"
            ]
        }
    }
    
    return metadata

def generate_llm_prompt_metadata():
    """
    Generate formatted metadata specifically for LLM prompts.
    Returns a formatted string ready to be used in text-to-SQL prompts.
    """
    metadata = get_transaction_history_metadata()
    
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
**Records**: {metadata['table_info']['total_records']} transactions
**Primary Key**: {metadata['table_info']['primary_key']}
**Foreign Keys**: {', '.join(metadata['table_info']['foreign_keys'])}
**Time Range**: {metadata['table_info']['time_range']}

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
            
        if 'pattern' in col:
            prompt_metadata += f"- Pattern: {col['pattern']}\n"
            
        prompt_metadata += "\n"
    
    # Add important relationships
    prompt_metadata += "### Key Relationships & Rules\n\n"
    
    # Foreign key relationships
    for fk in metadata['relationships']['foreign_keys']:
        prompt_metadata += f"- **{fk['column']}** references **{fk['references_table']}.{fk['references_column']}**: {fk['description']}\n"
    
    # Internal relationships
    for rel in metadata['relationships']['internal_relationships']:
        if rel['type'] == 'conditional_field':
            prompt_metadata += f"- **{rel['target']}** depends on **{rel['source']}**: {rel['rule']}\n"
        elif rel['type'] == 'sign_convention':
            prompt_metadata += f"- **Amount Sign Convention**: {rel['rule']}\n"
        else:
            prompt_metadata += f"- **{rel['type'].replace('_', ' ').title()}**: {rel['rule']}\n"
    
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
    metadata = get_transaction_history_metadata()
    with open('transaction_history_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
    
    # Save LLM prompt version as text
    prompt_metadata = generate_llm_prompt_metadata()
    with open('transaction_history_metadata_for_llm.md', 'w', encoding='utf-8') as f:
        f.write(prompt_metadata)
    
    print("Transaction history metadata files generated:")
    print("- transaction_history_metadata.json (Complete metadata)")
    print("- transaction_history_metadata_for_llm.md (LLM prompt format)")

if __name__ == "__main__":
    save_metadata_files()
    
    # Also print the LLM version for immediate use
    print("\n" + "="*80)
    print("TRANSACTION HISTORY LLM PROMPT METADATA")
    print("="*80)
    print(generate_llm_prompt_metadata())
