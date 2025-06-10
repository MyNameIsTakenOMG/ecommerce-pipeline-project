SELECT customerid,
  ROUND(SUM(quantity * unitprice), 2) AS total_sales
FROM clean_batch
GROUP BY customerid
ORDER BY total_sales DESC
LIMIT 10;
-- This query calculates and lists the top 10 total sales by customer from the clean_batch table.