import os
import pandas as pd
from faker import Faker
import random

# initialize Faker
fake = Faker()

# BrewMaster Stores
cities = ['New York', 'Austin', 'San Francisco', 'Denver', 'Seattle', 'Portland']
states = ['NY', 'TX', 'CA', 'CO', 'WA', 'OR']

def generate_store_data():
    stores = []
    for i in range(len(cities)):
        stores.append({
            'store_id': i + 1,  # Generate store_id starting from 1
            'store_name': f"BrewMasters {cities[i]}",
            'city': cities[i],
            'state': states[i]
        })
    
    # Add dummy store for online sales with next store_id
    stores.append({
        'store_id': 9999,  # Dummy store gets the next store_id
        'store_name': "BrewMasters Online",
        'city': "N/A",
        'state': "N/A"
    })

    return pd.DataFrame(stores)


# BrewMaster Products
product_data = {
    "Kits": [("Starter Kit", (50, 100)), ("Advanced Kit", (100, 300))],
    "Ingredients": [("Hops", (5, 20)), ("Yeast", (5, 15)), ("Malt", (10, 30))],
    "Equipment": [("Fermenter", (50, 150)), ("Bottling Tools", (30, 80)), ("Brewing Kettle", (100, 200))]
}

def generate_product_data():
    products = []
    for category, items in product_data.items():
        for product_name, price_range in items:
            price = round(random.uniform(*price_range), 2)
            products.append({
                'product_name': product_name, 
                'category': category, 
                'price': price
            })
    return pd.DataFrame(products)

# BrewMaster Employees
positions = ["Store Manager", "Sales Associate", "Brewing Expert", "Inventory Specialist"]

def generate_employees(num_employees=20):
    employees = []
    store_ids = list(range(1, len(cities) + 1))

    # Step 1: Ensure each store has at least one Sales Associate
    for store_id in store_ids:
        employees.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'position': 'Store Manager',
            'store_id': store_id
        })
        employees.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'position': 'Sales Associate',
            'store_id': store_id
        })
        employees.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'position': 'Brewing Expert',
            'store_id': store_id
        })

        employees.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'position': 'Inventory Specialist',
            'store_id': store_id
        })

    # Step 3: Add dummy employee with 'No Sales Associate' position
    employees.append({
        'first_name': 'N/A',
        'last_name': 'N/A',
        'position': 'No Sales Associate',
        'store_id': 9999
    })

    # Step 4: Add employee_id explicitly
    df_employees = pd.DataFrame(employees)

    return df_employees


# BrewMaster Customers
def generate_customer_data(num_customers=50):
    customers = []
    for _ in range(num_customers):
        customers.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'city': fake.city(),
            'state': random.choice(states)
        })
    return pd.DataFrame(customers)

# Marketing Campaigns
campaign_names = [
    "Brew Your Passion, Perfect Your Craft!",
    "Craft Your Own Beer, One Kit at a Time!",
    "From Grain to Glass—Brew Like a Master!",
    "Unleash Your Inner Brewer with Our Premium Kits!",
    "Brew Bold, Brew Better with BrewMasters!",
    "Your Homebrew Journey Starts Here!",
    "Fresh Ingredients, Perfect Brews—Every Time!",
    "Brew Like a Pro—Right in Your Kitchen!",
    "Tap into the Art of Home Brewing!",
    "Master the Craft of Beer Making with BrewMasters!"
]

def generate_marketing_campaign_data(num_campaigns=10):
    campaigns = []
    for i in range(num_campaigns):
        campaign_name = f"{random.choice(campaign_names)} Campaign"  # Use custom catchphrases
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

# Marketing Spend
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

# Generate all the data
if __name__ == "__main__":
    df_stores = generate_store_data()
    df_products = generate_product_data()
    df_employees = generate_employees(20)
    df_customers = generate_customer_data(50)
    df_campaigns = generate_marketing_campaign_data(10)
    df_spend = generate_marketing_spend_data(df_campaigns, 50)

    # Define the data path using an absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/generated_data')

    # Save to CSV
    df_stores.to_csv(os.path.join(data_path, 'stores.csv'), index=False)
    df_products.to_csv(os.path.join(data_path, 'products.csv'), index=False)
    df_employees.to_csv(os.path.join(data_path, 'employees.csv'), index=False)
    df_customers.to_csv(os.path.join(data_path, 'customers.csv'), index=False)
    df_campaigns.to_csv(os.path.join(data_path, 'marketing_campaigns.csv'), index=False)
    df_spend.to_csv(os.path.join(data_path, 'marketing_spend.csv'), index=False)
