import os
import pandas as pd
from utils import get_db_connection

def insert_data(table_name, df):
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()

    # Generate the INSERT INTO SQL command dynamically based on DataFrame columns
    columns = ', '.join(df.columns)
    values = ', '.join([f"%({col})s" for col in df.columns])

    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    try:
        print(f"Inserting data into {table_name}...")
        for i, row in df.iterrows():
            cursor.execute(insert_query, row.to_dict())
        conn.commit()
        print(f"Data inserted into {table_name} successfully!")
    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Define the base directory as the parent directory of the current file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Parent directory of src
    data_path = os.path.join(base_dir, 'data/generated_data/')  # Absolute path to data directory

    # Load CSV files and insert into respective tables
    try:
        df_stores = pd.read_csv(os.path.join(data_path, 'stores.csv'))
        insert_data("Stores", df_stores)

        df_products = pd.read_csv(os.path.join(data_path, 'products.csv'))
        insert_data("Products", df_products)

        df_employees = pd.read_csv(f"{data_path}/employees.csv")
        insert_data("Employees", df_employees)

        df_customers = pd.read_csv(os.path.join(data_path, 'customers.csv'))
        insert_data("Customers", df_customers)

        df_campaigns = pd.read_csv(os.path.join(data_path, 'marketing_campaigns.csv'))
        insert_data("Marketing_Campaigns", df_campaigns)

        df_spend = pd.read_csv(os.path.join(data_path, 'marketing_spend.csv'))
        insert_data("Marketing_Spend", df_spend)

    except Exception as e:
        print(f"An error occurred during data insertion: {e}")
