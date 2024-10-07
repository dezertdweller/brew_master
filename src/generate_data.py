import os
import pandas as pd
from faker import Faker
from faker.providers import address
import random
from datetime import datetime

# initialize Faker
random.seed(42)
fake = Faker()
fake.seed_instance(42)

# BrewMaster Stores
cities = ['New York', 'Austin', 'San Francisco', 'Denver', 'Seattle', 'Portland']
states = ['NY', 'TX', 'CA', 'CO', 'WA', 'OR']

store_opening_dates = {
    'Seattle': '2019-01-01',
    'Portland': '2019-06-01',
    'San Francisco': '2021-01-01',
    'New York': '2021-05-01',
    'Denver': '2022-10-01',
    'Austin': '2023-04-01'
}

def generate_store_data():
    stores = []
    for i, city in enumerate(cities):
        stores.append({
            'store_id': i + 1,
            'store_name': f"BrewMasters {city}",
            'city': city,
            'state': states[i],
            'opening_date': store_opening_dates[city]  # Assign opening date
        })
    
    # Add dummy store for online sales
    stores.append({
        'store_id': 9999,
        'store_name': "BrewMasters Online",
        'city': "N/A",
        'state': "N/A",
        'opening_date': '2019-01-01'  # Online store is always open
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
gender_weights = [0.40, 0.40, 0.05, 0.02, 0.03]

# Age range for employees
age_range = (20, 65)

def generate_employees(store_open_dates, current_year='2024', growth_rate=2):
    employees = []
    
    for store in store_open_dates:
        opening_date = store_open_dates[store]
        store_id = cities.index(store) + 1
        store_opening_year = datetime.strptime(opening_date, "%Y-%m-%d").year

        for position, salary_range in positions.items():
            employees.append({
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'position': position,
                'store_id': store_id,
                'age': random.randint(*age_range),
                'gender': random.choices(genders, weights=gender_weights)[0],
                'salary': round(random.uniform(*salary_range), 2),
                'hire_date': opening_date
                })

        # Calculate the number of years the store has been open
        current_year_int = int(current_year)
        years_open = current_year_int - store_opening_year
        
        # Add gradual employee growth for each year since opening
        for year in range(1, years_open + 1):
            hire_year = store_opening_year + year
            hire_date_start = datetime.strptime(f"{hire_year}-01-01", "%Y-%m-%d")
            hire_date_end = datetime.strptime(f"{hire_year}-12-31", "%Y-%m-%d")
            
            # Add a certain number of employees based on the growth rate
            num_new_employees = random.randint(1, growth_rate)  # Randomly add 1 to 'growth_rate' employees per year
            for _ in range(num_new_employees):
                position = random.choice(list(positions.keys()))  # Randomly assign a position
                salary_range = positions[position]
                
                employees.append({
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'position': position,
                    'store_id': store_id,
                    'age': random.randint(*age_range),
                    'gender': random.choices(genders, weights=gender_weights)[0],
                    'salary': round(random.uniform(*salary_range), 2),
                    'hire_date': fake.date_between_dates(hire_date_start, hire_date_end)  # Hire date within the year
                })

    # Add dummy employee with 'No Sales Associate' position
    employees.append({
        'first_name': 'N/A',
        'last_name': 'N/A',
        'position': 'No Sales Associate',
        'store_id': 9999,
        'age': 9999,
        'gender': "N/A",
        'salary': 0,
        'hire_date': '2000-01-01'
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

# Cities to target with increased online sales before store openings
online_boost_cities = {
    'San Francisco': '2020',
    'New York': '2020',
    'Denver': '2021',
    'Austin': '2022'
}

# Add corresponding states for the targeted cities
city_state_map = {
    'San Francisco': 'CA',
    'New York': 'NY',
    'Denver': 'CO',
    'Austin': 'TX'
}

# BrewMaster Customers with year-based growth
def generate_customer_data(start_year=2019, end_year=2023, online_customers_ratio=0.65, base_customers_per_year=1000, online_boost=0.15):
    customers = []
    
    # Generate customers for each year in the range
    for year in range(start_year, end_year + 1):
        num_customers = base_customers_per_year * (1 + (year - start_year) * 0.1)  # Simulate growth over time
        num_online_customers = int(num_customers * online_customers_ratio)
        num_store_customers = int(num_customers * (1 - online_customers_ratio))

        # Step 1: Generate customers for in-store sales (only for stores that have opened by this year)
        open_stores = [city for city, open_date in store_opening_dates.items() if datetime.strptime(open_date, '%Y-%m-%d').year <= year]
        open_states = [states[cities.index(city)] for city in open_stores]  # Corresponding states

        for _ in range(num_store_customers):
            if open_states:  # Only generate in-store customers if stores are open
                customers.append({
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'city': fake.city(),
                    'state': random.choice(open_states),  # Only states with open stores
                    'customer_type': 'In-Store',
                    'signup_year': year
                })

        # Step 2: Generate customers for online sales (from any state in the US)
        for _ in range(num_online_customers):
            # Check if we should boost online customers from specific cities
            boosted_city = None
            if str(year) in [boost_year for boost_year in online_boost_cities.values()]:
                # Pick the corresponding city and boost its chances
                for city, boost_year in online_boost_cities.items():
                    if str(year) == boost_year:
                        # Apply the boost for this city
                        if random.random() < online_boost:  # Apply a 15% boost chance
                            boosted_city = city
                            break

            if boosted_city:
                # Boosted online customer from the target city
                customers.append({
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'city': boosted_city,
                    'state': city_state_map[boosted_city],
                    'customer_type': 'Online',
                    'signup_year': year
                })
            else:
                # Regular online customer
                customers.append({
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'city': fake.city(),
                    'state': random.choice(us_states),  # Any US state
                    'customer_type': 'Online',
                    'signup_year': year
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
        start_date = fake.date_between(start_date='-5y', end_date='today')
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
    df_employees = generate_employees(store_opening_dates, current_year='2024', growth_rate=2)
    df_customers = generate_customer_data(start_year=2019, end_year=2023, online_customers_ratio=0.65, base_customers_per_year=1000, online_boost=0.15)
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
