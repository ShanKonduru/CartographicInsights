import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from ipywidgets import interact, widgets
import pandas as pd

# Load shapefile data
shapefile_path = "ne_110m_admin_1_states_provinces.shp"
gdf = gpd.read_file(shapefile_path)

# Parse the dataset
sales_data = pd.read_csv('GeographicDataAnalysis.csv')  
print(sales_data.columns)
print(sales_data.head)

# Merge sales data with shapefile data
merged_data = gdf.merge(sales_data, left_on='name', right_on='State')
print(merged_data.columns)
print(merged_data.head)

# Create a map centered around the USA
usa_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Create a MarkerCluster object
marker_cluster = MarkerCluster().add_to(usa_map)

# Function to handle dropdown selection change event
def on_dropdown_change(sales_person):
    # Clear existing markers
    marker_cluster.clear_layers()
    
    # Filter sales data based on selected sales person
    filtered_data = merged_data[merged_data['SalesPerson'] == sales_person]
    
    # Iterate through filtered data and add markers to the map
    for index, row in filtered_data.iterrows():
        state = row['name']
        sales = row['Sales']
        tooltip = f"State: {state}<br>Sales: ${sales:,.2f}"

        # Add a marker to the map
        folium.Marker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            popup=tooltip,
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)

# Get unique salesperson names
sales_persons = sales_data['SalesPerson'].unique()

# Create dropdown widget
sales_person_dropdown = widgets.Dropdown(options=sales_persons, description='Sales Person')

# Register the callback function with the dropdown widget
interact(on_dropdown_change, sales_person=sales_person_dropdown)

# Save the map to an HTML file
usa_map.save('usa_sales_map.html')