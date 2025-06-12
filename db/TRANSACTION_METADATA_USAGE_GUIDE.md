# Transaction History Metadata Usage Guide

This guide explains how to use the transaction history table metadata for various purposes, particularly for LLM-based SQL query generation and database documentation.

## Files Generated

### 1. `transaction_metadata.py`
The main Python script that generates comprehensive metadata for the transaction_history table. Contains:
- Complete table schema definition
- Column specifications with data types, constraints, and business rules
- Relationship mappings
- Common query patterns
- Performance optimization tips

### 2. `transaction_history_metadata.json`
Complete structured metadata in JSON format, suitable for:
- System integration and automation
- Database documentation tools
- Schema comparison utilities
- Data catalog systems

### 3. `transaction_history_metadata_for_llm.md`
Human-readable metadata formatted specifically for LLM prompts, ideal for:
- Text-to-SQL generation systems
- Database query assistants
- Documentation for developers
- Training data for ML models

## Key Features of Transaction History Metadata

### Comprehensive Column Documentation
Each column includes:
- **Data type and SQL specification**: Exact SQL Server column definition
- **Business description**: What the column represents in business terms
- **Valid values**: Enumerated lists where applicable
- **Value ranges**: Min/max values for numerical fields
- **Example values**: Sample data for context
- **Business rules**: How the column is used and constraints
- **Relationships**: Dependencies and calculations

### Transaction-Specific Features

#### Amount Sign Convention
- **Negative amounts**: Debits (money leaving account)
  - Withdrawals, Payments, Purchases, Fees, Loan Payments
- **Positive amounts**: Credits (money entering account)
  - Deposits, Salary, Interest, Refunds

#### Conditional Fields
- **merchant_name & merchant_category**: Only for Purchase/Payment transactions
- **account_to**: Only for Transfer transactions
- **reference_number**: Generated for tracking and disputes

#### Status-Based Logic
- **Completed**: Transaction processed, affects balance
- **Pending**: Transaction initiated, may not affect balance yet
- **Failed/Cancelled**: Transaction not processed, no balance impact

### Query Pattern Categories

#### 1. Customer-Centric Queries
- All transactions for a specific customer
- Customer transaction summaries by type
- Customer spending patterns

#### 2. Time-Based Analysis
- Date range filtering
- Monthly/quarterly summaries
- Trend analysis over time

#### 3. Transaction Analysis
- Spending by category
- Channel usage patterns
- Merchant analysis

#### 4. Financial Reporting
- Balance tracking over time
- Net cash flow calculations
- Account activity summaries

## Usage Examples

### For LLM Text-to-SQL Systems

Use the `transaction_history_metadata_for_llm.md` content in your system prompts:

```python
# Example system prompt for LLM
system_prompt = f"""
You are a SQL expert. Use this database schema to generate SQL queries:

{transaction_metadata_content}

Generate SQL queries based on user requests, following the query tips and patterns provided.
"""
```

### For Database Documentation

Use the JSON metadata for automated documentation:

```python
import json

# Load metadata
with open('transaction_history_metadata.json', 'r') as f:
    metadata = json.load(f)

# Generate documentation
for column in metadata['columns']:
    print(f"Column: {column['column_name']}")
    print(f"Type: {column['sql_type']}")
    print(f"Description: {column['description']}")
```

### For Query Validation

Use the metadata to validate query patterns:

```python
# Check if query follows recommended patterns
def validate_amount_query(sql_query):
    if "SUM(amount)" in sql_query and "status = 'Completed'" not in sql_query:
        return "Warning: Consider filtering by status = 'Completed' for accurate totals"
    return "Query looks good"
```

## Performance Considerations

### Recommended Indexes
Based on common query patterns, ensure these indexes exist:
1. **Primary Key**: `transaction_id` (automatic)
2. **Customer Queries**: `customer_id`
3. **Date Range Queries**: `transaction_date`
4. **Status Filtering**: `transaction_type, status` (composite)

### Query Optimization Tips
1. **Always filter by status** when calculating financial totals
2. **Use date ranges** to limit large result sets
3. **Leverage composite indexes** for multi-column filters
4. **Consider partitioning** for very large transaction volumes

## Integration with Customer Information

The transaction_history table links to customer_information via `customer_id`. For comprehensive analysis:

```sql
-- Combined customer and transaction analysis
SELECT 
    c.full_name,
    c.income_category,
    COUNT(t.transaction_id) as transaction_count,
    SUM(t.amount) as net_flow,
    SUM(CASE WHEN t.amount < 0 THEN ABS(t.amount) ELSE 0 END) as total_spent
FROM [dbo].[customer_information] c
LEFT JOIN [dbo].[transaction_history] t ON c.id = t.customer_id
WHERE t.status = 'Completed'
GROUP BY c.id, c.full_name, c.income_category
```

## Common Query Patterns

### 1. Customer Transaction Summary
```sql
SELECT 
    customer_id,
    COUNT(*) as total_transactions,
    COUNT(CASE WHEN amount > 0 THEN 1 END) as credits,
    COUNT(CASE WHEN amount < 0 THEN 1 END) as debits,
    SUM(amount) as net_flow
FROM [dbo].[transaction_history]
WHERE status = 'Completed'
GROUP BY customer_id
```

### 2. Monthly Spending by Category
```sql
SELECT 
    YEAR(transaction_date) as year,
    MONTH(transaction_date) as month,
    category,
    SUM(ABS(amount)) as total_spent
FROM [dbo].[transaction_history]
WHERE amount < 0 AND status = 'Completed'
GROUP BY YEAR(transaction_date), MONTH(transaction_date), category
ORDER BY year, month, total_spent DESC
```

### 3. Channel Usage Analysis
```sql
SELECT 
    channel,
    COUNT(*) as transaction_count,
    AVG(ABS(amount)) as avg_amount,
    SUM(ABS(amount)) as total_volume
FROM [dbo].[transaction_history]
WHERE status = 'Completed'
GROUP BY channel
ORDER BY transaction_count DESC
```

## Maintenance and Updates

### Updating Metadata
When the table structure changes:
1. Update the `transaction_metadata.py` script
2. Run the script to regenerate JSON and markdown files
3. Update any dependent systems or documentation

### Version Control
Keep metadata files in version control alongside database migration scripts to maintain synchronization between schema and documentation.

## Best Practices

### For Developers
1. **Reference metadata** before writing queries
2. **Follow naming conventions** established in the metadata
3. **Use provided query patterns** as starting points
4. **Validate business rules** against the metadata

### For Data Analysts
1. **Understand amount sign conventions** before aggregating
2. **Filter by status** for accurate financial calculations
3. **Use provided example queries** for common analysis patterns
4. **Consider time zones** when working with datetime fields

### For System Integration
1. **Use JSON metadata** for programmatic access
2. **Implement validation** based on business rules
3. **Follow relationship constraints** when inserting data
4. **Monitor performance** using recommended indexes

This metadata system provides a single source of truth for the transaction_history table structure and usage patterns, ensuring consistency across applications and reducing development time.
