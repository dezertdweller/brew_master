from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="brew_master",
            user=os.getenv("DB_USER"),       # Set your database user in environment variables
            password=os.getenv("DB_PASSWORD"),  # Set your database password in environment variables
            host="localhost"  # Adjust if you’re using a remote server
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
