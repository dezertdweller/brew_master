import os
import subprocess
from utils import get_db_connection

# Define SQL reset commands
reset_db_sql = """
    TRUNCATE TABLE Sales, Marketing_Spend, Marketing_Campaigns, Customers, Employees, Products, Stores CASCADE;
    ALTER SEQUENCE products_product_id_seq RESTART WITH 1;
    ALTER SEQUENCE employees_employee_id_seq RESTART WITH 1;
    ALTER SEQUENCE customers_customer_id_seq RESTART WITH 1;
    ALTER SEQUENCE marketing_campaigns_campaign_id_seq RESTART WITH 1;
    ALTER SEQUENCE marketing_spend_spend_id_seq RESTART WITH 1;
    ALTER SEQUENCE sales_sale_id_seq RESTART WITH 1;
"""

# Function to reset the database
def reset_database():
    conn = get_db_connection()
    if not conn:
        print("Error connecting to the database.")
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute(reset_db_sql)
        conn.commit()
        print("Database reset successfully.")
    except Exception as e:
        print(f"Error resetting database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def run_script(script_name):
    """Runs the provided script and handles errors."""
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f"Output from {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e.stderr}")
        raise

if __name__ == "__main__":
    # Define paths to the four scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Adjust this if needed
    
    print("Resetting the database...")
    reset_database()
    
    scripts = [
        os.path.join(base_dir, 'generate_data.py'),
        os.path.join(base_dir, 'insert_data.py'),
        os.path.join(base_dir, 'generate_sales.py'),
        os.path.join(base_dir, 'insert_sales.py')
    ]
    
    # Run each script sequentially
    for script in scripts:
        run_script(script)
