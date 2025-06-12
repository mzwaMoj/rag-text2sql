# Customer Information Table - Comprehensive Metadata for LLM Text-to-SQL

## Overview
This document provides a comprehensive guide to using the generated metadata for LLM-powered text-to-SQL query generation against the `customer_information` table in SQL Server.

## Generated Files

### 1. Core Metadata Files
- **`customer_table_metadata.json`** - Complete structured metadata in JSON format
- **`customer_table_metadata_for_llm.md`** - Formatted metadata optimized for LLM prompts
- **`table_metadata.py`** - Python module for generating and managing metadata

### 2. Demo and Example Files  
- **`text_to_sql_demo.py`** - Demonstration of how to use metadata for text-to-SQL
- **`sample_sql_queries.sql`** - Collection of example SQL queries with explanations

## Database Schema Summary

### Table: `customer_information`
- **Database**: SQL Server (master)
- **Full Name**: `[dbo].[customer_information]`
- **Records**: ~70 customers
- **Primary Key**: `id`
- **Total Columns**: 28

### Column Categories
1. **Identifiers** (4 columns): `id`, `account_number`, `full_name`, `email`
2. **Demographics** (5 columns): `age`, `gender`, `occupation`, `address`, `phone_number`  
3. **Financial** (5 columns): `income`, `income_source`, `income_category`, `balance`, `credit_score`
4. **Account** (2 columns): `account_type`, `last_login`
5. **Loans** (9 columns): All loan-related fields including eligibility, amounts, status, etc.
6. **Products** (3 columns): `product_holding` (JSON), `no_product_holding`, `entrenchment_score`

## Key Business Rules and Relationships

### Credit Score and Loan Eligibility
- `loan_eligible = 1` when `credit_score >= 580`
- Eligible loan amounts based on credit score tiers:
  - Excellent (750+): $25,000 - $100,000
  - Good (670-749): $10,000 - $50,000  
  - Fair (580-669): $1,000 - $25,000

### Income Classification
- **High**: > $100,000
- **Medium**: $50,000 - $100,000
- **Low**: < $50,000

### Product Entrenchment
- `entrenchment_score = (no_product_holding / 23) * 100`
- Higher scores indicate stronger customer relationships

## Using Metadata for Text-to-SQL

### 1. Basic Usage
```python
from table_metadata import generate_llm_prompt_metadata

# Get formatted metadata for LLM prompts
metadata_text = generate_llm_prompt_metadata()

# Combine with user question
user_question = "Find all high-income customers eligible for loans"
prompt = f"""
{metadata_text}

User Question: {user_question}
Generate SQL query:
"""
```

### 2. LLM Prompt Structure
The generated metadata includes:
- Complete column definitions with types and constraints
- Business rules and relationships
- Example queries by category
- SQL Server specific syntax tips
- JSON handling guidance

### 3. Query Categories Supported
- **Customer Search**: Find customers by various criteria
- **Financial Analysis**: Income, balance, credit score analytics
- **Loan Analysis**: Loan eligibility, applications, performance
- **Product Analysis**: Cross-selling opportunities, product holdings
- **Demographic Analysis**: Age, gender, occupation segmentation

## SQL Server Specific Considerations

### JSON Column Handling
The `product_holding` column stores JSON arrays of banking products:
```sql
-- Find customers with credit cards
SELECT * FROM customer_information 
WHERE product_holding LIKE '%Credit Card%'

-- Extract first product using JSON_VALUE
SELECT id, JSON_VALUE(product_holding, '$[0]') as first_product
FROM customer_information

-- Expand JSON to rows using OPENJSON
SELECT c.id, c.full_name, p.value as product
FROM customer_information c
CROSS APPLY OPENJSON(c.product_holding) p
```

### Date Operations
```sql
-- Customers who haven't logged in for 30+ days
SELECT * FROM customer_information 
WHERE DATEDIFF(day, last_login, GETDATE()) > 30

-- Loan applications by year
SELECT DATEPART(year, loan_application_date) as year, COUNT(*)
FROM customer_information 
WHERE loan_application_date IS NOT NULL
GROUP BY DATEPART(year, loan_application_date)
```

## Sample Use Cases

### 1. Customer Segmentation
```sql
-- Segment customers by value (balance + products)
SELECT 
    CASE 
        WHEN balance > 25000 AND no_product_holding > 5 THEN 'High Value'
        WHEN balance > 10000 AND no_product_holding > 3 THEN 'Medium Value'
        ELSE 'Standard'
    END as customer_segment,
    COUNT(*) as customer_count,
    AVG(entrenchment_score) as avg_entrenchment
FROM customer_information
GROUP BY CASE 
    WHEN balance > 25000 AND no_product_holding > 5 THEN 'High Value'
    WHEN balance > 10000 AND no_product_holding > 3 THEN 'Medium Value'
    ELSE 'Standard'
END
```

### 2. Cross-Selling Opportunities
```sql
-- High-income customers with low product holdings
SELECT id, full_name, income, no_product_holding, entrenchment_score
FROM customer_information
WHERE income_category = 'High' 
  AND no_product_holding <= 3
  AND loan_eligible = 1
ORDER BY income DESC
```

### 3. Risk Assessment
```sql
-- Customers with active loans and changing engagement patterns
SELECT 
    id, full_name, loan_amount_applied_for, loan_status,
    DATEDIFF(day, last_login, GETDATE()) as days_since_login,
    credit_score
FROM customer_information
WHERE loan_status IN ('Active', 'Approved')
  AND DATEDIFF(day, last_login, GETDATE()) > 60
ORDER BY loan_amount_applied_for DESC
```

## Best Practices for LLM Integration

### 1. Prompt Engineering
- Include complete metadata in system message
- Provide clear examples of expected SQL syntax
- Specify SQL Server dialect requirements
- Include error handling guidelines

### 2. Query Validation
- Always validate generated SQL before execution
- Check for proper NULL handling
- Verify JSON function usage
- Ensure appropriate WHERE clauses

### 3. Performance Considerations
- Use indexed columns (id, credit_score) in WHERE clauses
- Limit result sets for large queries
- Consider execution time for complex JSON operations
- Use appropriate data types in comparisons

## Integration with RAG Systems

This metadata can be integrated into RAG (Retrieval-Augmented Generation) systems for:
- **Semantic search** of customer data queries
- **Context-aware** SQL generation based on business rules
- **Multi-step reasoning** for complex analytical questions
- **Error correction** for malformed queries

## Maintenance

### Updating Metadata
When the database schema changes:
1. Update `table_metadata.py` with new column definitions
2. Run `python table_metadata.py` to regenerate files
3. Update business rules and relationships as needed
4. Test sample queries against updated schema

### Version Control
- Track metadata changes alongside schema changes
- Maintain backward compatibility for existing queries
- Document breaking changes in business rules

## Conclusion

This comprehensive metadata system provides a robust foundation for LLM-powered text-to-SQL generation, enabling:
- Accurate query generation based on business context
- Consistent handling of SQL Server syntax and functions
- Scalable integration with various LLM platforms
- Maintainable documentation of database schema and rules

The generated files serve as both documentation and functional components for building intelligent database query systems.
