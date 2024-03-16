import pandas as pd
from PlotMe import PlotMe

# Read sales data from CSV file
sales_data_df = pd.read_csv('GeographicDataAnalysis.csv')
# print(sales_data_df.head())
# print(sales_data_df.columns)

sales_data = {
    'State': ['New York', 'California', 'Texas', 'New York', 'California', 'Texas', 'New York', 'California', 'Texas', 'New York', 'California', 'Texas'],
    'SalesPerson': ['John', 'Alice', 'Bob', 'John', 'Alice', 'Bob', 'John', 'Alice', 'Bob', 'John', 'Alice', 'Bob'],
    'SalesValue': ['$10K', '$20K', '$13K', '$10K', '$20K', '$13K', '$10K', '$20K', '$13K', '$10K', '$20K', '$13K'],
    'Region': ['East', 'West', 'North-East', 'East', 'West', 'North-East', 'East', 'West', 'North-East', 'East', 'West', 'North-East']
}

# Instantiate SalesMap class and generate the map
sales_map = PlotMe("ne_110m_admin_1_states_provinces.shp", sales_data)

# to Generate MAP for all sales folks
# sales_map.generate_total_sales_map()

sales_map.generate_sales_map(SalesPerson='John', Region='East')