-- Sample SQL Queries for Customer Information Table
-- Generated on 2025-06-09
-- Database: SQL Server (master)
-- Table: customer_information

-- CUSTOMER DEMOGRAPHICS
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

================================================================================

-- LOAN ELIGIBILITY ANALYSIS
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

================================================================================

-- PRODUCT CROSS SELLING
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

================================================================================

-- JSON PRODUCT SEARCH
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

================================================================================

-- CUSTOMER ENGAGEMENT
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

================================================================================

