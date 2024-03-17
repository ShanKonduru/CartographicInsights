import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import pandas as pd

# Load shapefile data
shapefile_path = "ne_110m_admin_1_states_provinces.shp"
gdf = gpd.read_file(shapefile_path)

# Dummy sales data (replace this with your actual sales data)
sales_data = {
    'State': ['New York', 'California', 'Texas'],
    'SalesPerson': ['John', 'Alice', 'Bob'],
    'SalesValue': ['$10K', '$20K', '$13K']
}

# Merge sales data with shapefile data
merged_data = gdf.merge(pd.DataFrame(sales_data), left_on='name', right_on='State')

# Create a map centered around the USA
usa_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Create a MarkerCluster object
marker_cluster = MarkerCluster().add_to(usa_map)

# Function to handle dropdown selection change event
def on_dropdown_change(sales_person):
    # Filter sales data based on selected sales person
    filtered_data = merged_data[merged_data['SalesPerson'] == sales_person]
    
    # Iterate through filtered data and add markers to the map
    for index, row in filtered_data.iterrows():
        state = row['name']
        sales_value = row['SalesValue']  # Get sales value

        # Add a marker to the MarkerCluster
        folium.Marker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            popup=folium.Popup(f"State:<strong>{state}</strong><br>Sales Person:<strong>{sales_person}</strong><br>Sales Value:<strong>{sales_value}</strong>", max_width=300),  # Adjust max_width as needed            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)

# Get unique salesperson names
sales_persons = merged_data['SalesPerson'].unique()

# Register the callback function with the dropdown widget for each unique salesperson
for sales_person_name in sales_persons:
    on_dropdown_change(sales_person_name)

# Save the map to an HTML file
usa_map.save('usa_sales_map.html')
