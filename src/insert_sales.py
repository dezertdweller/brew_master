import os
import pandas as pd
from utils import get_db_connection

def insert_sales_data(df_sales):
    """Inserts sales data into the Sales table in the database."""
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    insert_query = """
    INSERT INTO Sales (product_id, store_id, customer_id, sale_date, quantity, total_price, channel, heard_about_us, sales_associate_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        for _, row in df_sales.iterrows():
            cursor.execute(insert_query, (
                row['product_id'],
                row['store_id'],
                row['customer_id'],
                row['sale_date'],
                row['quantity'],
                row['total_price'],
                row['channel'],
                row['heard_about_us'],
                row['sales_associate_id']
            ))
        conn.commit()
        print(f"Inserted {len(df_sales)} rows into the Sales table successfully.")
    except Exception as e:
        print(f"Error inserting data into Sales: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Define the data path using an absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/generated_data/sales.csv')

    # Load the sales data from the CSV
    df_sales = pd.read_csv(data_path)

    # Insert sales data into the database
    insert_sales_data(df_sales)
