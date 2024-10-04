import os
import pandas as pd
from faker import Faker
from faker.providers import address
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
    "Equipment": [("Fermenter", (50, 150)), ("Bottling Tools", (30, 80)), ("Brewing Kettle", (100, 200))],
    "Accessories": [("Bottle Caps", (2, 10)), ("Thermometer", (10, 25)), ("Hydrometer", (10, 30))],
    "Cleaning Supplies": [("Sanitizer", (5, 15)), ("Cleaning Brushes", (5, 20)), ("Bottle Cleaners", (8, 25))],
    "Packaging": [("Glass Bottles", (10, 50)), ("Growlers", (15, 60)), ("Bottle Labels", (3, 15))],
    "Merchandise": [
        ("T-Shirt", (15, 30)),
        ("Hoodie", (30, 60)),
        ("Hat", (10, 25)),
        ("Beanie", (10, 20))
    ]
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
positions = {
    "Store Manager": (180000, 21000),
    "Sales Associate": (50000, 70000),
    "Brewing Expert": (80000, 100000),
    "Inventory Specialist": (35000, 55000),
}
# Gender distribution: 70% Male/Female, 30% other options
genders = ["Male", "Female", "Non-Binary", "Other", "Didn't Report"]
gender_weights = [0.35, 0.35, 0.10, 0.10, 0.10]  # 70% for Male/Female, 30% for others

# Age range for employees
age_range = (20, 65)

def generate_employees(num_employees=20):
    employees = []
    store_ids = list(range(1, len(cities) + 1))

    # Ensure each store has at least one employee per position
    for store_id in store_ids:
        for position, salary_range in positions.items():
            employees.append({
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'position': position,
                'store_id': store_id,
                'age': random.randint(*age_range),  # Generate age within range
                'gender': random.choices(genders, weights=gender_weights)[0],  # Randomly assign gender
                'salary': round(random.uniform(*salary_range), 2)  # Randomly assign salary from position's range
            })

    # Add dummy employee with 'No Sales Associate' position
    employees.append({
        'first_name': 'N/A',
        'last_name': 'N/A',
        'position': 'No Sales Associate',
        'store_id': 9999,
        'age': 9999,
        'gender': "N/A",
        'salary': 0  # Dummy employee with no salary
    })

    # Create DataFrame
    df_employees = pd.DataFrame(employees)

    return df_employees

us_states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 
    'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 
    'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
    'WI', 'WY'
]

# BrewMaster Customers
def generate_customer_data(num_customers=5000, online_customers_ratio=0.65):
    customers = []
    num_online_customers = int(num_customers * online_customers_ratio)
    num_store_customers = num_customers - num_online_customers

    # Step 1: Generate customers for in-store sales (states where stores are located)
    for _ in range(num_store_customers):
        customers.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'city': fake.city(),
            'state': random.choice(states)  # States where stores are located
        })

    # Step 2: Generate customers for online sales (from any state in the US)
    for _ in range(num_online_customers):
        customers.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'city': fake.city(),
            'state': random.choice(us_states)  # Any US state
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
    for campaign_name in campaign_names:
        campaign_name = f"{campaign_name} Campaign" 
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

def generate_marketing_spend_data(df_campaigns, num_spend_entries=50):
    spend = []
    
    # Ensure that every campaign gets at least one spend entry
    for campaign_id in df_campaigns.index + 1:  # Add at least one spend for each campaign
        spend_date = fake.date_between(start_date=df_campaigns.loc[campaign_id - 1, 'start_date'], end_date=df_campaigns.loc[campaign_id - 1, 'end_date'])
        amount = round(random.uniform(500, 5000), 2)
        
        spend.append({
            'campaign_id': campaign_id,
            'date': spend_date,
            'amount': amount
        })
    
    # Distribute the remaining spend entries randomly
    remaining_entries = num_spend_entries - len(df_campaigns)
    if remaining_entries > 0:
        for _ in range(remaining_entries):
            campaign_id = random.choice(df_campaigns.index) + 1  # Randomly assign campaigns
            spend_date = fake.date_between(start_date=df_campaigns.loc[campaign_id - 1, 'start_date'], end_date=df_campaigns.loc[campaign_id - 1, 'end_date'])
            amount = round(random.uniform(500, 5000), 2)
            
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
    df_customers = generate_customer_data(5000)
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
