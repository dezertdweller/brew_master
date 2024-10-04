TRUNCATE TABLE Sales, Marketing_Spend, Marketing_Campaigns, Customers, Employees, Products, Stores CASCADE;
ALTER SEQUENCE products_product_id_seq RESTART WITH 1;
ALTER SEQUENCE employees_employee_id_seq RESTART WITH 1;
ALTER SEQUENCE customers_customer_id_seq RESTART WITH 1;
ALTER SEQUENCE marketing_campaigns_campaign_id_seq RESTART WITH 1;
ALTER SEQUENCE marketing_spend_spend_id_seq RESTART WITH 1;
ALTER SEQUENCE sales_sale_id_seq RESTART WITH 1;
