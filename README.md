# BrewMaster Supply - Sales and Marketing Performance Tracker

BrewMaster Supply is a fictional company that specializes in selling craft beer brewing kits, supplies, and ingredients to home brewers. This project simulates the company's business operations, tracking store sales, employee performance, customer interactions, marketing campaigns, and sales data.

## Project Overview

The purpose of this project is to build a relational database to track and analyze BrewMaster Supply's sales and marketing performance. The project showcases data generation, database insertion, and reporting using SQL and Python. The data spans store locations, products, employees, customers, and marketing campaigns, with dynamically generated sales data.

### Key Features
- **Stores**: Includes brick-and-mortar store locations and an online store.
- **Products**: Represents brewing kits, ingredients, and equipment offered by BrewMaster Supply.
- **Employees**: Tracks Store Managers, Sales Associates, and other roles within each store.
- **Customers**: Contains customer details for generating sales transactions.
- **Marketing Campaigns**: Simulates marketing activities with budget tracking and spend details.
- **Sales Data**: Dynamically generated sales transactions, linked to specific products, customers, and employees.

## Project File Structure

/src
  |-- generate_data.py        # Generates store, product, employee, customer, and marketing campaign data
  |-- insert_data.py          # Inserts generated data into the database (except sales)
  |-- generate_sales.py       # Generates sales data using store and employee data from the database
  |-- insert_sales.py         # Inserts sales data into the database
  |-- main.py                 # Script to run the entire pipeline from data generation to sales insertion

/data
  |-- generated_data/         # Folder where CSV files are generated and stored

/utils
  |-- db_connection.py        # Contains the database connection logic

/README.md                    # Project documentation


## Setup Instructions

1. **Clone the repository**:


2. **Create and set up the database**:
- Ensure that PostgreSQL or another compatible database is installed.
- Run the SQL schema script to create the required tables in the database.
- Update your database credentials in the `utils/db_connection.py` file.

3. **Install dependencies**:
- Install the required Python packages using pip:
  ```
  pip install -r requirements.txt
  ```

4. **Run the data pipeline**:
- To generate data and insert it into the database, run the main script:
  ```
  python src/main.py
  ```

This script runs the full data generation and insertion process for stores, products, employees, customers, marketing campaigns, and sales.

## Generated Data

- **Stores**: Six store locations plus an online store.
- **Products**: BrewMaster's offerings include brewing kits, ingredients, and equipment.
- **Employees**: Each store is assigned employees including Store Managers, Sales Associates, Brewing Experts, and Inventory Specialists.
- **Customers**: Data generated for 50 customers.
- **Marketing Campaigns**: Campaigns are created with a start date, end date, and budget.
- **Sales**: Sales data generated dynamically based on real-time employee and product data.

## Future Enhancements
- **Data Visualization**: Create interactive dashboards using Tableau or PowerBI.
- **Advanced Analytics**: Analyze marketing spend effectiveness and predict sales growth trends.
- **Business Insights**: Use machine learning to uncover patterns in customer purchases and employee performance.

## License

