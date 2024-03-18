import pandas as pd
from PlotMe import PlotMe
from  Utilities.CustomLogger import CustomLogger

# Create an instance of CustomLogger with both console and file logging
logger = CustomLogger(debug_mode=True, log_file="Logs/app.log")

# Read sales data from CSV file
sales_data_df = pd.read_csv("Dataset/GeographicDataAnalysis.csv")
logger.debug(sales_data_df.head())
logger.debug(sales_data_df.columns)

# Instantiate SalesMap class and generate the map
sales_map = PlotMe("MapData/ne_110m_admin_1_states_provinces.shp", sales_data_df, logger)

# to Generate MAP for total sales
sales_map.generate_total_sales_map("TotalSales.html")
logger.info("Generated MAP for total sales")

# to Generate MAP for specific Filter
sales_map.generate_filtered_sales_map("FilterUtahSpringSales.html", State="Utah", Season="Spring")
logger.info("Generated MAP for specific Filters")

# to Generate MAP for specific Filter - Spring Season
sales_map.generate_filtered_sales_map("FilterSpringSales.html", Season="Spring")
logger.info("Generated MAP for specific Filters Spring Season")

# to Generate MAP for specific Filter - Timezone based
sales_map.generate_filtered_sales_map("FilterTimeZoneYearOfSales.html", TimeZone='Eastern Standard Time (EST)', YearOfSale=2015 )
logger.info("Generated MAP for specific Filters Timezone")
