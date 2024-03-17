import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import numpy as np
from  Utilities.CustomLogger import CustomLogger


class PlotMe:
    def __init__(self, shapefile_path, sales_data_df, sales_data, logger):
        self.sales_data_df = sales_data_df
        self.shapefile_path = shapefile_path
        self.sales_data = sales_data
        self.gdf = gpd.read_file(shapefile_path)
        self.merged_data = None
        self.usa_map = None
        self.marker_cluster = None
        self.logger = logger

        # Remove '$' and 'K' characters and convert the column to numeric
        self.sales_data_df['SalesValue'] = sales_data_df['SalesValue'].str.replace('$', '').str.replace(',', '').str.replace('K', '000').astype(float)
        
        # Calculate average and 90th percentile of sales values
        self.average_sales_value = sales_data_df['SalesValue'].mean()
        self.percentile_90 = np.percentile(sales_data_df['SalesValue'], 90)

    def get_color(self, sales_value):
        sales_value = float(sales_value.replace(',', ''))
        if sales_value < self.average_sales_value:
            return 'red'
        elif sales_value >= self.percentile_90:
            return 'green'
        else:
            return 'yellow'
        
    def merge_sales_data(self):
        self.merged_data = self.gdf.merge(pd.DataFrame(self.sales_data), left_on='name', right_on='State')

    def create_map(self):
        self.usa_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    def create_marker_cluster(self):
        self.marker_cluster = MarkerCluster().add_to(self.usa_map)

    def add_markers_filtered(self, **kwargs):
        filtered_data = self.merged_data.copy()
        popup_text = ""
        for key, value in kwargs.items():
            filtered_data = filtered_data[filtered_data[key] == value]
            popup_text += "<br>" + key + ": <strong>" + str(value) + "</strong>"
        
        self.logger.debug('Popup message:')
        self.logger.debug(popup_text)

        self.logger.debug('filtered data columns')
        self.logger.debug(filtered_data.columns)
        
        self.logger.debug('filtered data head')
        self.logger.debug(filtered_data.head())

        for index, row in filtered_data.iterrows():
            state = row['name']
            sales_value = row['SalesValue']
            print(f"Sale Value :{sales_value}")
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                popup=folium.Popup(popup_text +f"<br>Sales Value:<strong>{sales_value}</strong>", max_width=300),
                icon=folium.Icon(color=self.get_color(sales_value))
            ).add_to(self.marker_cluster)

    def add_markers(self, sales_person):
        filtered_data = self.merged_data[self.merged_data['SalesPerson'] == sales_person]
        for index, row in filtered_data.iterrows():
            state = row['name']
            sales_value = row['SalesValue']
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                popup=folium.Popup(f"State:<strong>{state}</strong><br>Sales Person:<strong>{sales_person}</strong><br>Sales Value:<strong>{sales_value}</strong>", max_width=300),
                icon=folium.Icon(color=self.get_color(sales_value))
            ).add_to(self.marker_cluster)

    def generate_filtered_sales_map(self,OutputHtmlFileName,  **kwargs):
        self.merge_sales_data()
        self.create_map()
        self.create_marker_cluster()
        self.add_markers_filtered(**kwargs)
        self.usa_map.save(OutputHtmlFileName)

    def generate_total_sales_map(self, OutputHtmlFileName):
        self.merge_sales_data()
        self.create_map()
        self.create_marker_cluster()
        sales_persons = self.merged_data['SalesPerson'].unique()
        for sales_person_name in sales_persons:
            self.add_markers(sales_person_name)
        self.usa_map.save(OutputHtmlFileName)