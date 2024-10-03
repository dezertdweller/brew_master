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
        for i, row in df.iterrows():
            cursor.execute(insert_query, row.to_dict())
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Load CSV files
    data_path = "../data/generated_data/"
    
    # Insert Stores data
    df_stores = pd.read_csv(f"{data_path}/stores.csv")
    insert_data("Stores", df_stores)

    # Insert Products data
    df_products = pd.read_csv(f"{data_path}/products.csv")
    insert_data("Products", df_products)

    # Insert Employees data
    df_employees = pd.read_csv(f"{data_path}/employees.csv")
    insert_data("Employees", df_employees)

    # Insert Customers data
    df_customers = pd.read_csv(f"{data_path}/customers.csv")
    insert_data("Customers", df_customers)

    # Insert Marketing Campaigns data
    df_campaigns = pd.read_csv(f"{data_path}/marketing_campaigns.csv")
    insert_data("Marketing_Campaigns", df_campaigns)

    # Insert Marketing Spend data
    df_spend = pd.read_csv(f"{data_path}/marketing_spend.csv")
    insert_data("Marketing_Spend", df_spend)

    # Insert Sales data (this could take longer due to large volume)
    df_sales = pd.read_csv(f"{data_path}/sales.csv")
    insert_data("Sales", df_sales)
