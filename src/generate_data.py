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
            'store_name': f"BrewMasters {cities[i]}",
            'city': cities[i],
            'state': states[i]
        }
        stores.append(store)
    
    return pd.DataFrame(stores)

if __name__ == "__main__":
    # Generate the store data and print to verify
    df_stores = generate_store_data()
    print(df_stores)
    
    # Define the data path using an absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/generated_data')

    # Print the DataFrame and save to CSV
    print(df_stores)
    stores_csv = os.path.join(data_path, 'stores.csv')
    df_stores.to_csv(stores_csv, index=False)