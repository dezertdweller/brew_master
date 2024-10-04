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
    # Define the base directory and data path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data/generated_data/sales.csv')

    # Load and insert the sales data
    df_sales = pd.read_csv(data_path)
    insert_data("Sales", df_sales)
