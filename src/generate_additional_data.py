import os
import random
import pandas as pd
from faker import Faker
from utils import get_db_connection

random.seed(42)
fake = Faker()
fake.seed_instance(42)

us_states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 
    'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 
    'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
    'WI', 'WY'
]

states = ['NY', 'TX', 'CA', 'CO', 'WA', 'OR']

# Fetch employee-store pairs from the database
def fetch_employee_store_pairs():
    """Fetch employee_id, store_id, and position for relevant employee positions."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("""
        SELECT employee_id, store_id, position
        FROM Employees
        WHERE position IN ('Sales Associate', 'Store Manager', 'Brewing Expert');
    """)
    employee_store_pairs = cursor.fetchall()

    cursor.close()
    conn.close()
    return employee_store_pairs

# Fetch dummy employee ID for online sales
def fetch_dummy_employee_id():
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT employee_id FROM Employees WHERE position = 'No Sales Associate';")
    result = cursor.fetchone()
    dummy_employee_id = result[0] if result else None

    cursor.close()
    conn.close()
    return dummy_employee_id

# Fetch store IDs from the database
def fetch_store_ids():
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT store_id FROM Stores WHERE store_id != 9999;")  # Exclude dummy store
    store_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return store_ids

# Fetch product IDs from the database
def fetch_product_ids():
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT product_id FROM Products;")
    product_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return product_ids

# Fetch customer data (customer_id and state)
def fetch_customer_data():
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, state FROM Customers;")
    customer_data = cursor.fetchall()  # List of tuples (customer_id, state)

    cursor.close()
    conn.close()
    return customer_data

# Generate sales data
def generate_sales_data(num_sales=100):
    """Generate sales data."""
    sales = []

    # Fetch employee-store pairs, product_ids, customer data, and dummy employee ID
    employee_store_pairs = fetch_employee_store_pairs()
    product_ids = fetch_product_ids()
    customer_data = fetch_customer_data()  # (customer_id, state) tuples
    dummy_employee_id = fetch_dummy_employee_id()

    # Dummy store for online sales
    dummy_store_id = 9999
    heard_about_us_options = ['Instagram', 'Facebook', 'YouTube', 'Friend', 'Google', 'Other']

    # Weights for employee positions
    position_weights = {
        "Sales Associate": 0.60,
        "Store Manager": 0.30,
        "Brewing Expert": 0.10
    }

    for _ in range(num_sales):
        product_id = random.choice(product_ids)
        customer_id, customer_state = random.choice(customer_data)
        sale_date = str(fake.date_between(start_date='-1y', end_date='today'))
        quantity = random.randint(1, 5)
        total_price = round(random.uniform(20, 500), 2)
        channel = random.choice(['Online', 'In-Store'])

        if channel == 'In-Store':
            # Select an employee based on weighted position types
            employee_store_weighted = random.choices(
                employee_store_pairs, 
                weights=[position_weights[emp[2]] for emp in employee_store_pairs],  # Weights based on employee position
                k=1
            )[0]
            employee_id, store_id, _ = employee_store_weighted

            # Ensure the customer is from the same state as the store for in-store sales
            while customer_state not in states:  # Reassign customer if they aren't from the store's state
                customer_id, customer_state = random.choice(customer_data)
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
    df_sales = generate_sales_data(10000)  # Generate 1000 sales

    # Save to CSV for further insertion
    df_sales.to_csv(os.path.join(data_path, 'sales.csv'), index=False)

    print(f"Generated sales data saved to {data_path}")
