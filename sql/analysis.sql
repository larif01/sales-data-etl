-- Run with: sqlite3 outputs/sales.db < sql/analysis.sql
-- Total revenue
SELECT ROUND(SUM(total_amount), 2) AS revenue FROM sales;

-- Revenue by category
SELECT category, ROUND(SUM(total_amount), 2) AS revenue
FROM sales GROUP BY category ORDER BY revenue DESC;

-- Monthly revenue
SELECT SUBSTR(sale_date, 1, 7) AS month, ROUND(SUM(total_amount), 2) AS revenue
FROM sales GROUP BY month ORDER BY month;

-- Top selling products by revenue
SELECT product, SUM(quantity) AS units_sold, ROUND(SUM(total_amount), 2) AS revenue
FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 5;
