SELECT country, ROUND(SUM(quantity * unitprice),2) AS total_sales
FROM clean_batch
GROUP BY country
ORDER BY total_sales DESC
LIMIT 10;
-- This query calculates and lists the top 10 total sales by country from the clean_batch table.