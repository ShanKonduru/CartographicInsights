import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import pandas as pd

class PlotMe:
    def __init__(self, shapefile_path, sales_data):
        self.shapefile_path = shapefile_path
        self.sales_data = sales_data
        self.gdf = gpd.read_file(shapefile_path)
        self.merged_data = None
        self.usa_map = None
        self.marker_cluster = None

    def merge_sales_data(self):
        self.merged_data = self.gdf.merge(pd.DataFrame(self.sales_data), left_on='name', right_on='State')

    def create_map(self):
        self.usa_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    def create_marker_cluster(self):
        self.marker_cluster = MarkerCluster().add_to(self.usa_map)

    def add_markers_filtered(self, **kwargs):
        filtered_data = self.merged_data.copy()
        for key, value in kwargs.items():
            filtered_data = filtered_data[filtered_data[key] == value]
            
        for index, row in filtered_data.iterrows():
            state = row['name']
            sales_value = row['SalesValue']
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                popup=folium.Popup(f"State:<strong>{state}</strong><br>Sales Person:<strong>{kwargs['SalesPerson']}</strong><br>Sales Value:<strong>{sales_value}</strong>", max_width=300),
                icon=folium.Icon(color='blue')
            ).add_to(self.marker_cluster)

    def add_markers(self, sales_person):
        filtered_data = self.merged_data[self.merged_data['SalesPerson'] == sales_person]
        for index, row in filtered_data.iterrows():
            state = row['name']
            sales_value = row['SalesValue']
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                popup=folium.Popup(f"State:<strong>{state}</strong><br>Sales Person:<strong>{sales_person}</strong><br>Sales Value:<strong>{sales_value}</strong>", max_width=300),
                icon=folium.Icon(color='blue')
            ).add_to(self.marker_cluster)

    def generate_sales_map(self, **kwargs):
        self.merge_sales_data()
        self.create_map()
        self.create_marker_cluster()
        self.add_markers_filtered(**kwargs)
        self.usa_map.save('Filtered_usa_sales_map.html')

    def generate_total_sales_map(self):
        self.merge_sales_data()
        self.create_map()
        self.create_marker_cluster()
        sales_persons = self.merged_data['SalesPerson'].unique()
        for sales_person_name in sales_persons:
            self.add_markers(sales_person_name)
        self.usa_map.save('total_usa_sales_map.html')