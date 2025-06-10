SELECT stockcode,
  SUM(quantity) AS total_quantity
FROM clean_batch -- WHERE country = 'united kingdom' # Uncomment this line to filter by a specific country
GROUP BY stockcode
ORDER BY total_quantity DESC
LIMIT 10;
-- This query calculates and lists the top 10 products by total quantity sold from the clean_batch table.