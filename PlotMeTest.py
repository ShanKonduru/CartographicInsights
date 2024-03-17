import pandas as pd
from PlotMe import PlotMe
from CustomLogger import CustomLogger

# Create an instance of CustomLogger with both console and file logging
logger = CustomLogger(debug_mode=True, log_file="app.log")

# Read sales data from CSV file
sales_data_df = pd.read_csv("GeographicDataAnalysis.csv")
logger.debug(sales_data_df.head())
logger.debug(sales_data_df.columns)

# Convert DataFrame to dictionary
sales_data = {
    'State': sales_data_df['State'].to_list(),
    'SalesPerson': sales_data_df['SalesPerson'].to_list(),
    'SalesValue': sales_data_df['SalesValue'].to_list(),
    'Region': sales_data_df['Region'].to_list(),
    'Country' : sales_data_df['Country'].to_list(),
    'StateName' : sales_data_df['StateName'].to_list(),
    'SalesManager' : sales_data_df['SalesManager'].to_list(),
    'DateOfSale' : sales_data_df['DateOfSale'].to_list(),
    'YearOfSale' : sales_data_df['YearOfSale'].to_list(),
    'MonthOfSale' : sales_data_df['MonthOfSale'].to_list(),
    'Season' : sales_data_df['Season'].to_list()
}

logger.debug(sales_data)

# Instantiate SalesMap class and generate the map
sales_map = PlotMe("ne_110m_admin_1_states_provinces.shp", sales_data_df, sales_data, logger)

# to Generate MAP for total sales
# sales_map.generate_total_sales_map()
# logger.info("Generated MAP for total sales")

# to Generate MAP for specific Filter
sales_map.generate_filtered_sales_map(State="Utah", Season="Spring")
logger.info("Generated MAP for specific Filters")
