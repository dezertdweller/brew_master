import os
import random
import pandas as pd
from faker import Faker
from utils import get_db_connection

fake = Faker()

def fetch_employee_store_pairs():
    """Fetch employee_id and store_id pairs for Sales Associates."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    # Query the database to get the employee_id and store_id for Sales Associates
    cursor.execute("""
        SELECT employee_id, store_id
        FROM Employees
        WHERE position = 'Sales Associate';
    """)
    employee_store_pairs = cursor.fetchall()  # List of tuples (employee_id, store_id)
    
    cursor.close()
    conn.close()
    return employee_store_pairs

def fetch_dummy_employee_id():
    """Fetch the employee_id for the 'No Sales Associate' role."""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    # Query the database to get the employee_id for 'No Sales Associate'
    cursor.execute("""
        SELECT employee_id
        FROM Employees
        WHERE position = 'No Sales Associate';
    """)
    result = cursor.fetchone()  # Fetch the first result
    dummy_employee_id = result[0] if result else None  # Return the employee_id or None

    cursor.close()
    conn.close()
    return dummy_employee_id

def fetch_store_ids():
    """Fetch all store_ids from the Stores table."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    # Query the database to get the store_id for all stores
    cursor.execute("SELECT store_id FROM Stores;")
    store_ids = [row[0] for row in cursor.fetchall()]  # List of store_ids

    cursor.close()
    conn.close()
    return store_ids

def fetch_product_ids():
    """Fetch all product_ids from the Products table."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    # Query the database to get the product_id for all products
    cursor.execute("SELECT product_id FROM Products;")
    product_ids = [row[0] for row in cursor.fetchall()]  # List of product_ids

    cursor.close()
    conn.close()
    return product_ids

def generate_sales_data(num_sales=100):
    """Generate sales data."""
    sales = []

    # Fetch employee-store pairs, store_ids, product_ids, and dummy employee ID
    employee_store_pairs = fetch_employee_store_pairs()
    store_ids = fetch_store_ids()
    product_ids = fetch_product_ids()
    dummy_employee_id = fetch_dummy_employee_id()

    # Dummy store for online sales
    dummy_store_id = 9999

    heard_about_us_options = ['Instagram', 'Facebook', 'YouTube', 'Friend', 'Google', 'Other']

    for _ in range(num_sales):
        product_id = random.choice(product_ids)  # Use product_ids fetched from the database
        customer_id = random.randint(1, 50)  # Assuming you have 50 customers
        sale_date = str(fake.date_between(start_date='-1y', end_date='today'))
        quantity = random.randint(1, 5)
        total_price = round(random.uniform(20, 500), 2)
        channel = random.choice(['Online', 'In-Store'])

        if channel == 'In-Store':
            # Choose a random (employee_id, store_id) pair for in-store sales
            employee_id, store_id = random.choice(employee_store_pairs)
            heard_about_us = None
        else:
            # Use dummy store and dummy employee for online sales
            store_id = dummy_store_id
            employee_id = dummy_employee_id
            heard_about_us = random.choice(heard_about_us_options)

        # Append the sale data to the sales list
        sales.append({
            'product_id': product_id,
            'store_id': store_id,
            'customer_id': customer_id,
            'sale_date': sale_date,
            'quantity': quantity,
            'total_price': total_price,
            'channel': channel,
            'heard_about_us': heard_about_us,
            'sales_associate_id': employee_id
        })

    return pd.DataFrame(sales)

if __name__ == "__main__":
    # Define the data path using an absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/generated_data')

    # Generate the sales data based on what's in the database
    df_sales = generate_sales_data(1000000)  # Generate 1000 sales

    # Save to CSV for further insertion
    df_sales.to_csv(os.path.join(data_path, 'sales.csv'), index=False)

    print(f"Generated sales data saved to {data_path}")
