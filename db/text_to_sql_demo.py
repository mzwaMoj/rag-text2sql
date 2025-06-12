"""
Demo: Using Table Metadata for LLM Text-to-SQL Generation
This script demonstrates how to use the generated metadata for creating 
text-to-SQL prompts that can be used with LLMs like GPT, Claude, etc.
"""

import json
from table_metadata import generate_llm_prompt_metadata, get_customer_information_metadata

def create_text_to_sql_prompt(user_question, metadata_text):
    """
    Create a complete prompt for LLM text-to-SQL generation
    """
    prompt = f"""You are a SQL expert. Given the database schema below, generate a SQL query to answer the user's question.

{metadata_text}

## User Question:
{user_question}

## Instructions:
1. Generate a valid SQL Server query based on the schema above
2. Use proper SQL Server syntax and functions
3. Handle NULL values appropriately
4. For JSON column queries, use JSON_VALUE() or OPENJSON() functions
5. Include helpful comments in your query
6. Return only the SQL query, properly formatted

## SQL Query:
```sql
"""
    return prompt

def demo_text_to_sql_scenarios():
    """
    Demonstrate various text-to-SQL scenarios using our metadata
    """
    
    # Load the metadata
    metadata_text = generate_llm_prompt_metadata()
    
    # Sample user questions that could be asked
    sample_questions = [
        "Find all customers with high income who are eligible for loans but haven't applied for any",
        "What's the average balance for each account type?",
        "Show me customers who have credit cards in their product holdings",
        "Find customers whose last login was more than 30 days ago",
        "What's the average entrenchment score by income category?",
        "Show loan applications from the last 6 months with their approval status",
        "Find customers over 50 with excellent credit scores (>750)",
        "Which loan purposes have the highest average interest rates?",
        "Show customers with more than 5 products and high entrenchment scores",
        "Find young customers (under 30) with business accounts"
    ]
    
    print("=== TEXT-TO-SQL DEMO SCENARIOS ===\n")
    
    for i, question in enumerate(sample_questions, 1):
        print(f"SCENARIO {i}:")
        print(f"Question: {question}")
        print("\nGenerated Prompt:")
        print("-" * 80)
        prompt = create_text_to_sql_prompt(question, metadata_text)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("\n" + "="*100 + "\n")

def get_sample_sql_queries():
    """
    Return sample SQL queries that demonstrate the database capabilities
    """
    return {
        "customer_demographics": """
            -- Customer demographic analysis
            SELECT 
                gender,
                income_category,
                COUNT(*) as customer_count,
                AVG(age) as avg_age,
                AVG(balance) as avg_balance
            FROM customer_information 
            WHERE gender IS NOT NULL 
            GROUP BY gender, income_category
            ORDER BY income_category, gender;
        """,
        
        "loan_eligibility_analysis": """
            -- Loan eligibility and application analysis
            SELECT 
                income_category,
                COUNT(*) as total_customers,
                SUM(CASE WHEN loan_eligible = 1 THEN 1 ELSE 0 END) as eligible_customers,
                SUM(CASE WHEN loan_status IS NOT NULL THEN 1 ELSE 0 END) as applied_customers,
                AVG(CASE WHEN loan_eligible = 1 THEN eligible_loan_amount ELSE 0 END) as avg_eligible_amount
            FROM customer_information
            GROUP BY income_category
            ORDER BY 
                CASE income_category 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                END;
        """,
        
        "product_cross_selling": """
            -- Product holding analysis for cross-selling opportunities
            SELECT 
                no_product_holding as product_count,
                COUNT(*) as customer_count,
                AVG(entrenchment_score) as avg_entrenchment,
                AVG(balance) as avg_balance
            FROM customer_information
            WHERE no_product_holding IS NOT NULL
            GROUP BY no_product_holding
            ORDER BY no_product_holding;
        """,
        
        "json_product_search": """
            -- Find customers with specific products (JSON query example)
            SELECT 
                id,
                full_name,
                product_holding,
                no_product_holding,
                entrenchment_score
            FROM customer_information
            WHERE product_holding LIKE '%Credit Card%'
               OR product_holding LIKE '%Home Mortgage%'
            ORDER BY entrenchment_score DESC;
        """,
        
        "customer_engagement": """
            -- Customer engagement analysis
            SELECT 
                CASE 
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 7 THEN 'Active (last week)'
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 30 THEN 'Regular (last month)'
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 90 THEN 'Occasional (last 3 months)'
                    ELSE 'Inactive (90+ days)'
                END as engagement_level,
                COUNT(*) as customer_count,
                AVG(no_product_holding) as avg_products,
                AVG(balance) as avg_balance
            FROM customer_information
            WHERE last_login IS NOT NULL
            GROUP BY 
                CASE 
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 7 THEN 'Active (last week)'
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 30 THEN 'Regular (last month)'
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 90 THEN 'Occasional (last 3 months)'
                    ELSE 'Inactive (90+ days)'
                END
            ORDER BY 
                CASE 
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 7 THEN 1
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 30 THEN 2
                    WHEN DATEDIFF(day, last_login, GETDATE()) <= 90 THEN 3
                    ELSE 4
                END;
        """
    }

def save_demo_queries():
    """Save sample queries to a file for reference"""
    queries = get_sample_sql_queries()
    
    with open('sample_sql_queries.sql', 'w', encoding='utf-8') as f:
        f.write("-- Sample SQL Queries for Customer Information Table\n")
        f.write("-- Generated on 2025-06-09\n")
        f.write("-- Database: SQL Server (master)\n")
        f.write("-- Table: customer_information\n\n")
        
        for query_name, query_sql in queries.items():
            f.write(f"-- {query_name.upper().replace('_', ' ')}\n")
            f.write(query_sql.strip())
            f.write("\n\n" + "="*80 + "\n\n")
    
    print("Sample queries saved to: sample_sql_queries.sql")

def show_metadata_summary():
    """Display a summary of the generated metadata"""
    metadata = get_customer_information_metadata()
    
    print("=== METADATA SUMMARY ===")
    print(f"Database: {metadata['database_info']['database_type']}")
    print(f"Table: {metadata['table_info']['table_name']}")
    print(f"Total Columns: {len(metadata['columns'])}")
    print(f"Records: ~{metadata['table_info']['total_records']}")
    
    print("\nColumn Categories:")
    categories = {
        "Identifiers": ["id", "account_number", "full_name", "email"],
        "Demographics": ["age", "gender", "occupation", "address", "phone_number"],
        "Financial": ["income", "income_source", "income_category", "balance", "credit_score"],
        "Account": ["account_type", "last_login"],
        "Loans": ["loan_eligible", "eligible_loan_amount", "loan_amount_applied_for", 
                 "loan_status", "loan_tenure", "loan_interest_rate", "loan_purpose", 
                 "loan_application_date", "previous_loans_count"],
        "Products": ["product_holding", "no_product_holding", "entrenchment_score"]
    }
    
    for category, columns in categories.items():
        print(f"  {category}: {len(columns)} columns")
    
    print(f"\nQuery Patterns Available: {len(metadata['common_queries'])}")
    print("Files Generated:")
    print("  - customer_table_metadata.json (Complete metadata)")
    print("  - customer_table_metadata_for_llm.md (LLM prompt format)")

if __name__ == "__main__":
    print("Customer Information Table - Text-to-SQL Demo")
    print("=" * 60)
    
    # Show metadata summary
    show_metadata_summary()
    
    print("\n" + "=" * 60)
    
    # Save sample queries
    save_demo_queries()
    
    print("\n" + "=" * 60)
    
    # Run demo scenarios (commented out to avoid too much output)
    # demo_text_to_sql_scenarios()
    
    print("\nMetadata generation complete!")
    print("\nTo use this for text-to-SQL:")
    print("1. Load the metadata using generate_llm_prompt_metadata()")
    print("2. Combine with user questions to create LLM prompts")
    print("3. Send to your preferred LLM (GPT-4, Claude, etc.)")
    print("4. Execute the generated SQL queries against your database")
