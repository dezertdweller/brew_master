-- Active: 1733791264064@@127.0.0.1@5432@brew_master@public
SELECT st.store_name, SUM(s.total_price) AS total_sales
FROM sales AS s
JOIN stores AS st
ON s.store_id = st.store_id
GROUP BY st.store_name
ORDER BY total_sales DESC;

WITH ranked_products AS(
    SELECT 
        store_name,
        product_name,
        RANK() OVER(PARTITION BY store_name ORDER BY total_products_sold DESC) AS product_rank
    FROM (
        SELECT 
            p.product_name,
            p.category, 
            st.store_name,
            SUM(s.quantity) AS total_products_sold
        FROM sales AS s
        JOIN products AS p
        ON s.product_id = p.product_id
        JOIN stores AS st
        ON s.store_id = st.store_id
        GROUP BY 
            p.product_name, 
            p.category,
            st.store_id) AS products_by_store
)
SELECT *
FROM ranked_products
WHERE rank <= 5;

SELECT 
    state, 
    customer_type, 
    COUNT(*)::INTEGER AS total_customers
FROM customers
GROUP BY state, customer_type
ORDER BY state, customer_type;

WITH monthly_sales AS (
    SELECT 
        month,
        year,
        SUM(revenue) AS monthly_revenue
    FROM (
        SELECT 
            EXTRACT(MONTH from sale_date) AS month, 
            EXTRACT(YEAR FROM sale_date) AS year,
            total_price AS revenue
        FROM sales) monthly_sales
    GROUP BY month, year
    ORDER BY year, month
)
SELECT 
    month,
    year,
    monthly_revenue AS current_month_rev,
    COALESCE(LAG(monthly_revenue) OVER (ORDER BY year, month), 0) AS previous_month_rev,
    COALESCE(monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY year, month), 0) AS monthly_change_rev,
    SUM(monthly_revenue) OVER (PARTITION BY year ORDER BY year, month) AS cum_annual_sales
FROM monthly_sales;
    
SELECT *
FROM marketing_campaigns
WHERE start_date BETWEEN '2020-03-01' AND '2021-04-01';

SELECT 
    c.*, 
    total_marketing_spend.total_expenses,
    c.budget - total_marketing_spend.total_expenses AS budget_diff
FROM marketing_campaigns AS c
LEFT JOIN (
    SELECT 
        campaign_id,
        SUM(amount) AS total_expenses
    FROM marketing_spend
    GROUP BY campaign_id) AS total_marketing_spend
ON c.campaign_id = total_marketing_spend.campaign_id;

SELECT 
    e.first_name || ' ' || e.last_name AS employee_name,
    e.position,
    st.store_name,
    SUM(s.total_price) AS total_sales
FROM sales AS s
LEFT JOIN employees AS e
ON s.sales_associate_id = e.employee_id
LEFT JOIN stores AS st
ON e.store_id = st.store_id
GROUP BY employee_name, e.position, st.store_name;

SELECT 
    e.position,
    COUNT(*) AS total_transactions,
    ROUND(AVG(s.total_price), 2) AS avg_sales,
    SUM(s.total_price) AS total_sales,
    EXTRACT(year from s.sale_date) AS year
FROM sales AS s
LEFT JOIN employees AS e
ON s.sales_associate_id = e.employee_id
GROUP BY e.position, year
ORDER BY year, e.position;

SELECT COUNT(DISTINCT customer_id), channel
FROM sales
GROUP BY channel;

SELECT 
    customer_id,
    COUNT(*) AS total_transactions,
    SUM(total_price) AS total_customer_rev
FROM sales
GROUP BY customer_id
ORDER BY total_customer_rev DESC;


SELECT 
    SUM(s.total_price) AS total_sales,
    SUM(s.quantity) AS total_units_sold,
    AVG(s.total_price) AS avg_product_revenue,
    p.product_name,
    p.category
FROM sales AS s
JOIN products AS p
ON s.product_id = p.product_id
GROUP BY p.category, p.product_name
ORDER BY p.category ASC, total_sales DESC;