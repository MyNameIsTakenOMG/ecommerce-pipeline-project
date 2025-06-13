SELECT t.customerid,
  t.invoicedate,
  t.quantity,
  t.unitprice,
  ROUND(t.quantity * t.unitprice, 2) AS total_price,
  s.segment
FROM ecommerce_data_lake.clean_batch t
  LEFT JOIN ecommerce_data_lake.customer_segments s ON t.customerid = s.customerid
WHERE s.segment = 'vip'
LIMIT 10;