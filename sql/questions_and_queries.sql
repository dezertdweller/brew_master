-- BrewMasters Supply Data Analysis Queries

-- 1. What are the stores ordered by total sales revenue in descending order?
SELECT st.store_name, SUM(s.total_price) AS total_sales
FROM sales AS s
INNER JOIN stores as st
ON s.store_id = st.store_id
GROUP BY st.store_name
ORDER BY total_sales DESC;

-- 2. Which store has the highest sales volume (in terms of quantity sold)?
SELECT st.store_name, SUM(s.quantity) AS total_units
FROM sales AS s
INNER JOIN stores as st
ON s.store_id = st.store_id
GROUP BY st.store_name
ORDER BY total_units DESC
LIMIT 1;

-- 3. What are the top 5 best-selling products in terms of revenue?
SELECT p.product_name, SUM(s.total_price) AS total_sales
FROM sales AS s
JOIN products AS p
ON s.product_id = p.product_id
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 5;

-- 4. What are the most popular products (based on quantity sold)?
SELECT p.product_name, SUM(s.quantity) AS total_units
FROM sales AS s
JOIN products AS p
ON s.product_id = p.product_id
GROUP BY product_name
ORDER BY total_units DESC
LIMIT 5;

-- 5. What are the total sales by month for each store?
SELECT EXTRACT(MONTH FROM s.sale_date) AS month, SUM(s.total_price) AS total_sales, st.store_name
FROM sales AS s
JOIN stores AS st
ON s.store_id = st.store_id
GROUP BY EXTRACT(MONTH FROM s.sale_date), store_name
ORDER BY month ASC, total_sales DESC;


-- 6. How has revenue trended over the past year for each store?
WITH monthly_sales AS (
	SELECT EXTRACT(MONTH FROM s.sale_date) AS month, SUM(s.total_price) AS total_revenue, st.store_name
	FROM sales AS s
	JOIN stores AS st
	ON s.store_id = st.store_id
	WHERE s.sale_date BETWEEN '2023-10-07' AND '2024-10-07'
	GROUP BY EXTRACT(MONTH FROM s.sale_date), store_name)

SELECT month, total_revenue, store_name,
		LAG (total_revenue) OVER(PARTITION BY store_name
								 ORDER BY month ASC) AS last_month,
		LAG (total_revenue) OVER(PARTITION BY store_name
								 ORDER BY month ASC) - total_revenue AS change_in_rev,
		ROUND((LAG (total_revenue) OVER(PARTITION BY store_name
								   		ORDER BY month ASC) - total_revenue) /
			   LAG (total_revenue) OVER(PARTITION BY store_name
									    ORDER BY month ASC) * 100) AS perc_change
FROM monthly_sales;

-- 7. Which city has the most customers?
SELECT state,  COUNT(customer_id) AS count
FROM customers
GROUP BY state
ORDER BY count DESC
LIMIT 1;


-- 8. Which state has the highest number of customers?
SELECT state,  COUNT(customer_id) AS count
FROM customers
GROUP BY state
ORDER BY count DESC
LIMIT 1;

-- 9. Which sales associate has the highest total sales (revenue generated)?
SELECT city,  COUNT(customer_id) AS count
FROM customers
GROUP BY city
ORDER BY count DESC
LIMIT 1;


-- 10. What is the average sales revenue per sales associate by store?


-- 11. What is the average price of products in each category?


-- 12. How does product pricing vary by category?


-- 13. Which marketing campaign resulted in the highest total sales?


-- 14. What is the total spend by campaign, and how does it correlate with sales performance during the campaign period?


-- 15. What percentage of total revenue comes from each sales channel (e.g., online vs. in-store)?


-- 16. How does sales performance differ by channel for each store?


-- 17. How many customers reported hearing about us from each marketing channel (Instagram, Google, Friend, etc.)?


-- 18. Which marketing channels have resulted in the most revenue?


-- 19. What is the total sales revenue by product category across all stores?


-- 20. What is the average sales per transaction by product category?


-- 21. What is the average sales volume per sales associate in each store?


-- 22. Which sales associate has the highest average sales per customer?


-- 23. Which region (combining cities and states) has the highest total sales?


-- 24. How does sales performance vary across states?


-- 25. Which store has shown the greatest sales growth year-over-year?


-- 26. What is the total revenue per store, and how does it compare to the number of employees at each store?


-- 27. Are higher-priced products correlated with higher sales volumes?


-- 28. How do product prices impact the total sales per transaction?


-- 29. What is the average purchase frequency per customer?


-- 30. What is the average order value for repeat customers versus new customers?


-- 31. What is the ROI (Return on Investment) for each marketing campaign based on sales generated during the campaign period?


-- 32. Which campaign had the best cost per acquisition (CPA) based on total customer growth?


-- 33. How does sales volume differ between male and female sales associates?


-- 34. What is the average age of the top-performing employees by store?


-- 35. Which store has the highest number of transactions during peak hours (e.g., weekends)?


-- 36. What is the average transaction value in urban versus suburban store locations?


-- 37. What is the total sales revenue for brewing kits compared to brewing supplies?


-- 38. What is the sales distribution of products priced below $50 versus above $50?


-- 39. How did sales trends change during the periods of active marketing campaigns?


-- 40. How much revenue was generated during each campaign period, broken down by store?


-- 41. Which months have the highest total sales revenue?


-- 42. How does the sales volume vary across seasons (spring, summer, fall, winter)?


-- 43. What are the top 5 cities by customer lifetime value (total revenue per customer)?


-- 44. How many customers have made more than 3 purchases?


-- 45. What is the most popular product in each store?


-- 46. Which products are most frequently bought together?


-- 47. Based on past sales trends, what are the predicted sales for the next quarter?


-- 48. What is the forecasted demand for each product category?


-- 49. Which sales associate has the highest customer satisfaction (based on quantity sold per interaction)?


-- 50. What is the average sales growth per sales associate over time?


-- 51. What is the average tenure of employees across stores?


-- 52. Is there a correlation between employee age and sales performance?


-- 53. Which campaign had the highest revenue per dollar spent on marketing?


-- 54. How does total marketing spend correlate with customer acquisition rate?


-- 55. How do brewing kit sales compare to ingredients and supplies?


-- 56. Which product group (kits, ingredients, or supplies) has the highest repeat purchase rate?


-- 57. Which day of the week has the highest sales volume for each store?


-- 58. How does sales volume differ on weekends versus weekdays?


-- 59. What is the customer conversion rate for each marketing campaign?


-- 60. Which marketing campaign had the highest number of new customer acquisitions?


