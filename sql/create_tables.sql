CREATE TABLE Stores (
    store_id SERIAL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL
);

CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50),
    store_id INT REFERENCES Stores(store_id)
);

CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
);

CREATE TABLE Sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Products(product_id),
    store_id INT REFERENCES Stores(store_id),
    customer_id INT REFERENCES Customers(customer_id),
    employee_id INT REFERENCES Employees(employee_id),
    sale_date DATE NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    heard_about_us VARCHAR(100)
);

CREATE TABLE Marketing_Campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(15, 2) NOT NULL
);

CREATE TABLE Marketing_Spend (
    spend_id SERIAL PRIMARY KEY,
    campaign_id INT REFERENCES Marketing_Campaigns(campaign_id),
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
);

