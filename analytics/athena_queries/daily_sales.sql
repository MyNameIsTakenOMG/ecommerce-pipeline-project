SELECT DATE(invoicedate) AS sales_date,
  country,
  ROUND(SUM(quantity * unitprice), 2) AS total_sales
FROM clean_batch
GROUP BY DATE(invoicedate),
  country
ORDER BY DATE(invoicedate) ASC
LIMIT 10;
-- This query calculates and lists the top 10 countries by total sales from the clean_batch table.