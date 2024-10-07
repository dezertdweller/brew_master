import os
import random
import pandas as pd
import numpy as np
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

# Temporal weights for variability
daily_variation = {
    "Monday": 0.8,
    "Tuesday": 0.9,
    "Wednesday": 0.95,
    "Thursday": 1.0,
    "Friday": 1.2,
    "Saturday": 1.5,
    "Sunday": 1.4
}

monthly_variation = {
    '01': 1.1, 
    '02': 0.9,
    '06': 1.2, 
    '07': 1.4, 
    '12': 1.5
}

# Simulate an increasing trend over time
def simulate_trend(sale_date):
    """Simulate increasing sales over time, e.g., as the store grows."""
    base_date = pd.Timestamp("2019-01-01")
    delta_days = (pd.Timestamp(sale_date) - base_date).days
    return 1 + (delta_days / 365) * 0.1

# Define random scaling factors for each store
store_scaling_factors = {
    1: np.random.uniform(0.8, 1.2),  # Scale sales for store 1
    2: np.random.uniform(0.5, 1.0),  # Scale sales for store 2
    3: np.random.uniform(0.9, 1.5),  # Scale sales for store 3
    4: np.random.uniform(0.6, 1.4),  # Scale sales for store 4
    5: np.random.uniform(0.9, 1.5),  # Scale sales for store 5
    6: np.random.uniform(0.9, 1.4),  # Scale sales for store 6
}

# Simulate economic fluctuations
def economic_multiplier(sale_date):
    """Simulate economic changes with random shifts over time."""
    year = pd.Timestamp(sale_date).year
    if year == 2020:  # Simulate pandemic downturn
        return 0.7
    elif year == 2021:  # Recovery period
        return 1.2
    return 1.0  # Normal years

# Customer segmentation based on spending behavior
def customer_segment_multiplier(segment):
    """Return a multiplier based on customer segment."""
    segment_multipliers = {
        'Frequent Buyer': 1.8,
        'First-Time': 1.0,
        'Loyalty Member': 2.5
    }
    return segment_multipliers.get(segment, 1.0)

# Fetch customer IDs and states from the database
def fetch_customer_data():
    """Fetch customer_id and state pairs from the database."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    # Query the database to get the customer_id and state
    cursor.execute("SELECT customer_id, state FROM Customers;")
    customer_data = cursor.fetchall()  # List of tuples (customer_id, state)

    cursor.close()
    conn.close()
    return customer_data

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

def fetch_store_data():
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    # Fetch store_id and opening_date from the Stores table
    cursor.execute("SELECT store_id, opening_date FROM Stores WHERE store_id != 9999;")  # Exclude dummy store
    store_data = {row[0]: row[1] for row in cursor.fetchall()}  # Return as a dictionary {store_id: opening_date}

    cursor.close()
    conn.close()
    return store_data

# Fetch product IDs from the database
def fetch_product_data():
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT product_id, price FROM Products;")
    product_data = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.close()
    conn.close()
    return product_data


# Generate sales data
def generate_sales_data(num_sales=100):
    sales = []

    # Fetch employee-store pairs, product_ids, and customer data
    store_data = fetch_store_data()
    employee_store_pairs = fetch_employee_store_pairs()
    product_data = fetch_product_data()
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

    # Simulate customer segments
    customer_segments = ['Frequent Buyer', 'First-Time', 'Loyalty Member']

    def generate_seasonal_multiplier():
        """Generate a random seasonal multiplier between 0.5 and 1.8."""
        return np.random.uniform(0.5, 1.8)

    for _ in range(num_sales):
        product_id = random.choice(list(product_data.keys()))
        product_price = product_data[product_id]
        customer_id, customer_state = random.choice(customer_data)
        sale_date = str(fake.date_between(start_date='-5y', end_date='today'))
        sale_datetime = pd.Timestamp(sale_date)
        sale_day = sale_datetime.strftime("%A")
        sale_month = sale_datetime.strftime("%m")

        # Check if store is open based on the sale date
        store_id = None
        for store, opening_date in store_data.items():
            if pd.Timestamp(sale_date) >= pd.Timestamp(opening_date):
                store_id = store
                break

        # Continue only if store is open or if it’s an online sale
        if store_id is not None:
            quantity = random.randint(1, 5)
            # Apply temporal, seasonal, and economic multipliers to add variability
            daily_multiplier = daily_variation.get(sale_day, 1.0)
            monthly_multiplier = monthly_variation.get(sale_month, 1.0)
            seasonal_multiplier = generate_seasonal_multiplier()
            trend_multiplier = simulate_trend(sale_date)
            economic_fluctuation = economic_multiplier(sale_date)

            # Calculate new quantity
            quantity = round(quantity * daily_multiplier * monthly_multiplier * seasonal_multiplier * trend_multiplier * economic_fluctuation)

            # Ensure quantity is at least 1
            if quantity < 1:
                quantity = 1
            
            # Assign a customer segment
            customer_segment = random.choice(customer_segments)
            customer_multiplier = customer_segment_multiplier(customer_segment)

            # Apply customer segment multiplier to the quantity
            quantity = round(quantity * customer_multiplier)

            # Apply customer segment multiplier to the total price
            total_price = product_price * quantity

            # Assign random channel
            channel = random.choice(['Online', 'In-Store'])

            if channel == 'In-Store':
                employee_store_weighted = random.choices(
                    employee_store_pairs, 
                    weights=[position_weights[emp[2]] for emp in employee_store_pairs],
                    k=1
                )[0]
                employee_id, store_id, _ = employee_store_weighted

                # Ensure the customer is from the same state as the store for in-store sales
                while customer_state not in states:
                    customer_id, customer_state = random.choice(customer_data)
                
                # Apply scaling factor based on store
                quantity = round(quantity * store_scaling_factors[store_id])
                total_price = quantity * product_price
                heard_about_us = None
            else:
                # Use dummy store and employee for online sales
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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/generated_data')

    # Generate the sales data based on what's in the database
    df_sales = generate_sales_data(3000000)  # Generate 3M sales

    # Save to CSV for further insertion
    df_sales.to_csv(os.path.join(data_path, 'sales.csv'), index=False)

    print(f"Generated sales data saved to {data_path}")
