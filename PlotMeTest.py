from PlotMe import PlotMe


# Dummy sales data (replace this with your actual sales data)
sales_data = {
    'State': ['New York', 'California', 'Texas'],
    'SalesPerson': ['John', 'Alice', 'Bob'],
    'SalesValue': ['$10K', '$20K', '$13K']
}

# Instantiate SalesMap class and generate the map
sales_map = PlotMe("ne_110m_admin_1_states_provinces.shp", sales_data)

# to Generate MAP for all sales folks
sales_map.generate_total_sales_map()

# to Generate MAP for one sales person
sales_map.generate_sales_map('John')

