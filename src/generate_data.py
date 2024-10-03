import os
import pandas as pd
from faker import Faker
import random

# initialize Faker
fake = Faker()

# BrewMaster Stores
cities = ['New York', 'Austin', 'San Francisco', 'Denver', 'Seattle', 'Portland']
states = ['NY', 'TX', 'CA', 'CO', 'WA', 'OR']

def generate_store_data(num_stores=6):
    stores = []
    for i in range(num_stores):
        store = {
            'store_id': i + 1,
            'store_name': f"BrewMasters {cities[i]}",
            'city': cities[i],
            'state': states[i]
        }
        stores.append(store)
    
    return pd.DataFrame(stores)

# BrewMaster Products
product_data = {
    "Kits": [
        ("Starter Kit", (50, 100)),
        ("Advanced Kit", (100, 300))
    ],
    "Ingredients": [
        ("Hops", (5, 20)),
        ("Yeast", (5, 15)),
        ("Malt", (10, 30))
    ],
    "Equipment": [
        ("Fermenter", (50, 150)),
        ("Bottling Tools", (30, 80)),
        ("Brewing Kettle", (100, 200))
    ]
}

def generate_product_data(num_products=16):
    products = []

    # generate n number of products
    for _ in range(num_products):

        # Choose random product category
        category = random.choice(list(product_data.keys()))

        # Choose random product from chosen cateogry
        product_name, price_range = random.choice(product_data[category])

        # Generate random price within specified range
        price = round(random.uniform(*price_range), 2)

        products.append({
            'product_name': product_name, 
            'category': category, 
            'price': price
        })

    return pd.DataFrame(products)

# BrewMaster employees

positions = ["Store Manager", "Sales Associate", "Brewing Expert", "Inventory Specialist"]

def generate_employees(num_employees=18):
    employees = []
    store_ids = list(range(1, len(cities) +1))

    for _ in range(num_employees):
        first_name = fake.first_name()
        last_name = fake.last_name()
        position = random.choice(positions)
        store_id = random.choice(store_ids)  # Randomly assign to one of the stores
        
        employees.append({
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'store_id': store_id
        })
    
    return pd.DataFrame(employees)

# BrewMaster customers 
def generate_customer_data(num_customers=50):
    customers = []
    
    for _ in range(num_customers):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        city = fake.city()
        state = random.choice(list(states))  # Randomly assign a state
        
        customers.append({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'city': city,
            'state': state,
        })
    
    return pd.DataFrame(customers)

# BrewMaster campaigns
def generate_marketing_campaign_data(num_campaigns=10):
    campaigns = []
    
    for _ in range(num_campaigns):
        campaign_name = f"{fake.catch_phrase()} Campaign"
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+30d')
        budget = round(random.uniform(5000, 50000), 0)
        
        campaigns.append({
            'campaign_name': campaign_name,
            'start_date': start_date,
            'end_date': end_date,
            'budget': budget
        })
    
    return pd.DataFrame(campaigns)

# BrewMaster campaign spend

def generate_marketing_spend_data(df_campaigns, num_spend_entries=50):
    spend = []
    
    for _ in range(num_spend_entries):
        campaign_id = random.choice(df_campaigns.index) + 1  # Reference campaign_id from the campaigns
        spend_date = fake.date_between(start_date=df_campaigns.loc[campaign_id - 1, 'start_date'], end_date=df_campaigns.loc[campaign_id - 1, 'end_date'])
        amount = round(random.uniform(500, 5000), 2)  # Random spend between $500 and $5000
        
        spend.append({
            'campaign_id': campaign_id,
            'date': spend_date,
            'amount': amount
        })
    
    return pd.DataFrame(spend)

# BrewMaster sales

def generate_sales_data(df_products, df_customers, df_stores, df_employees, num_sales=100000):
    sales = []
    
    # Filter employees to get only sales associates
    sales_associates = df_employees[df_employees['position'] == "Sales Associate"]

    for _ in range(num_sales):
        product_id = random.choice(df_products.index) + 1
        customer_id = random.choice(df_customers.index) + 1
        store_id = random.choice(df_stores.index) + 1
        sale_date = fake.date_between(start_date='-1y', end_date='today')
        quantity = random.randint(1, 5)
        price = df_products.loc[product_id - 1, 'price']
        total_price = round(price * quantity, 2)
        channel = random.choice(['Online', 'In-Store'])  # Randomly assign the sales channel

        # If it's an in-store purchase, assign a sales associate
        if channel == 'In-Store':
            sales_associate_id = random.choice(sales_associates.index) + 1  # Random sales associate
        else:
            sales_associate_id = None  # No sales associate for online sales
        
        heard_about_us = fake.catch_phrase() if channel == 'Online' else None  # Only for online sales
        
        sales.append({
            'product_id': product_id,
            'customer_id': customer_id,
            'store_id': store_id,
            'sale_date': sale_date,
            'quantity': quantity,
            'total_price': total_price,
            'channel': channel,
            'sales_associate_id': sales_associate_id,  # Include the sales associate ID
            'heard_about_us': heard_about_us
        })
    
    return pd.DataFrame(sales)


if __name__ == "__main__":
    # Generate the data
    df_stores = generate_store_data()
    df_products = generate_product_data(16)
    df_employees = generate_employees(20)
    df_customers = generate_customer_data(50)
    df_campaigns = generate_marketing_campaign_data(10)
    df_spend = generate_marketing_spend_data(df_campaigns, 50)
    df_sales = generate_sales_data(df_products, df_customers, df_stores, df_employees, 100000)

    # Define the data path using an absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/generated_data')

    # Save to CSV
    stores_csv = os.path.join(data_path, 'stores.csv')
    products_csv = os.path.join(data_path, 'products.csv')
    employees_csv = os.path.join(data_path, 'employees.csv')
    customers_csv = os.path.join(data_path, 'customers.csv')
    campaigns_csv = os.path.join(data_path, 'marketing_campaigns.csv')
    spend_csv = os.path.join(data_path, 'marketing_spend.csv')
    sales_csv = os.path.join(data_path, 'sales.csv')

    df_stores.to_csv(stores_csv, index=False)
    df_products.to_csv(products_csv, index=False)
    df_employees.to_csv(employees_csv, index=False)
    df_customers.to_csv(customers_csv, index=False)
    df_campaigns.to_csv(campaigns_csv, index=False)
    df_spend.to_csv(spend_csv, index=False)
    df_sales.to_csv(sales_csv, index=False)
