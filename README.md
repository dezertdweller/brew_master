# BrewMaster Supply - Sales and Marketing Performance Tracker

BrewMaster Supply is a fictional company that specializes in selling craft beer brewing kits, supplies, and ingredients to home brewers. This project simulates the company's business operations, tracking store sales, employee performance, customer interactions, marketing campaigns, and sales data.

## Project Overview

The purpose of this project is to build a relational database to track and analyze BrewMaster Supply's sales and marketing performance. The project showcases data generation, database insertion, and reporting using SQL and Python. The data spans store locations, products, employees, customers, and marketing campaigns, with dynamically generated sales data.

After creating the database, analysts can write queries, analyze data using Pythbon, or connect to a data viz tool to answer analysis questions found in the /sql folder. 

### Key Features
- **Stores**: Includes brick-and-mortar store locations and an online store.
- **Products**: Represents brewing kits, ingredients, and equipment offered by BrewMaster Supply.
- **Employees**: Tracks Store Managers, Sales Associates, and other roles within each store.
- **Customers**: Contains customer details for generating sales transactions.
- **Marketing Campaigns**: Simulates marketing activities with budget tracking and spend details.
- **Sales Data**: Dynamically generated sales transactions, linked to specific products, customers, and employees.

## Project File Structure
```
/src
  |-- generate_data.py              # Generates store, product, employee, customer, and marketing campaign data
  |-- insert_data.py                # Inserts generated data into the database (except sales)
  |-- generate_sales.py             # Generates sales data using store and employee data from the database
  |-- insert_sales.py               # Inserts sales data into the database
  |-- main.py                       # Script to run the entire pipeline from data generation to sales insertion
  |-- generate-additional_data.py   # Generates additional sales data
  |-- main.py                       # Inserts additional sales data into the database
  |-- utils.py                      # Contains the database connection logic

/notebooks
  |-- analysis.ipynb                # Notebook for EDA.

/sql
  |-- create_tables.sql             # File with SQL scripts to create database schema
  |-- questions.sql                 # File with questions to practice SQL queries and answers
  |-- reset_db.sql                  # File with SQL script to reset database if needed
  |-- questions.md                  # File questions for analysis (no answers)

/data
  |-- generated_data/               # Folder where CSV files are generated and stored on your machine

/assets
  |-- brew_master_report.pdf        # Final report for sql questions

/README.md                          # Project documentation

/LICENSE.txt                        # Data license

/requirements.txt                   # Packages

```

## Setup Instructions

1. **Clone the repository**:
```
git clone https://github.com/dezertdweller/brew_master.git
```

2. **Create and set up the database**:
- Ensure that PostgreSQL or another compatible database is installed.
- Run the SQL schema script to create the required tables in the database.
- Update your database credentials in the `utils/db_connection.py` file.

```
psql -h localhost -U <username> -d <database_name> -f sql/create_tables.sql
```

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

To generate additional sales data, run the additional script:
```
python src/additional.py
```
This will generate n number of additional sales that you can specify in `generate_additional_data.py` in the following line:
```
df_sales = generate_sales_data(10000)  # Generate 1000 sales, change to any number. 
```

## Generated Data

- **Stores**: Six store locations plus an online store.
- **Products**: BrewMaster's offerings include brewing kits, ingredients, equipment, accessories, cleaning supplies, packaging and merchandise.
- **Employees**: Each store is assigned employees including Store Managers, Sales Associates, Brewing Experts, and Inventory Specialists.
- **Customers**: Data generated for 5000 customers.
- **Marketing Campaigns**: Campaigns are created with a start date, end date, and budget.
- **Sales**: Sales data generated dynamically based on real-time employee and product data.

## Future Enhancements
- **Data Visualization**: Create interactive dashboards using Tableau or PowerBI.
- **Advanced Analytics**: Analyze marketing spend effectiveness and predict sales growth trends.
- **Business Insights**: Use machine learning to uncover patterns in customer purchases and employee performance.

## License

This project and its generated data are licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License. You are free to:
- Share and adapt the data for non-commercial purposes, provided that you give appropriate credit.
- Attribution: "Data generated by Katia Lopes-Gilbert, used under CC BY-NC 4.0."

For more details, see the full [LICENSE](./LICENSE.txt).

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
