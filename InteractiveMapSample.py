from flask import Flask, render_template, request
from Utilities.CustomLogger import CustomLogger  # Import your custom logger
from PlotMe import PlotMe  # Import the PlotMe class from your code
import pandas as pd
import os
import time

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generatemap', methods=['GET'])
def generatemap():
    # Extract the query parameters from the request
    year = request.args.get('year')
    state = request.args.get('state')

    # Process the query parameters and generate the map (replace this with your logic)
    # Example logic: return a rendered template with the map
    return render_template('map_template.html', year=year, state=state)

@app.route('/totalsales', methods=['GET'])
def generate_total_sales_map():
    # Read sales data from CSV file
    sales_data_df = pd.read_csv("Dataset/GeographicDataAnalysis.csv")

    shapefile_path = 'MapData/ne_110m_admin_1_states_provinces.shp'  # Provide the path to your shapefile
    sales_data_df = sales_data_df  # You need to load your sales data DataFrame here

    # Create an instance of CustomLogger with both console and file logging
    logger = CustomLogger(debug_mode=True, log_file="Logs/app.log")

    plotter = PlotMe(shapefile_path, sales_data_df, logger)
    
    OutputHtmlFileName = f'TotalSales.html'  # Define the output HTML file name

    if(os.path.exists(OutputHtmlFileName)):
        os.remove(OutputHtmlFileName)

    print('***************************  Begin generate_filtered_sales_map')
    plotter.generate_total_sales_map(OutputHtmlFileName)
    print('***************************  End generate_filtered_sales_map')

    print('*************************** Looking for OutputHtmlFileName file exists :' + OutputHtmlFileName)
    # Check if the file exists
    # while not os.path.exists(OutputHtmlFileName):
    time.sleep(2)  # Check every second
    print('*************************** The OutputHtmlFileName file exists :' + OutputHtmlFileName)

    # Render the map in the HTML template
    print('*************************** render_template')
    return render_template("map_template.html", map_file=OutputHtmlFileName, state=state, year=year)

@app.route('/generate_map', methods=['GET'])
def generate_map():
    # Retrieve form data
    # Read sales data from CSV file
    sales_data_df = pd.read_csv("Dataset/GeographicDataAnalysis.csv")

    shapefile_path = 'MapData/ne_110m_admin_1_states_provinces.shp'  # Provide the path to your shapefile
    sales_data_df = sales_data_df  # You need to load your sales data DataFrame here

    # Create an instance of CustomLogger with both console and file logging
    logger = CustomLogger(debug_mode=True, log_file="Logs/app.log")

    plotter = PlotMe(shapefile_path, sales_data_df, logger)
    
    # Extract the year and state parameters from the URL query string
    year = request.args.get('year')
    state = request.args.get('state')

    if not year or not state:
        return "Year and state parameters are required."

    OutputHtmlFileName = f'map_{year}_{state}.html'  # Define the output HTML file name

    if(os.path.exists(OutputHtmlFileName)):
        os.remove(OutputHtmlFileName)

    print('***************************  Begin generate_filtered_sales_map')
    # plotter.generate_filtered_sales_map(OutputHtmlFileName, YearOfSale=year, State=state)
    plotter.generate_filtered_sales_map(OutputHtmlFileName,State="Utah", Season="Spring")
    print('***************************  End generate_filtered_sales_map')

    print('*************************** Looking for OutputHtmlFileName file exists :' + OutputHtmlFileName)
    # Check if the file exists
    # while not os.path.exists(OutputHtmlFileName):
    time.sleep(2)  # Check every second
    print('*************************** The OutputHtmlFileName file exists :' + OutputHtmlFileName)

    # Render the map in the HTML template
    print('*************************** render_template')
    return render_template("map_template.html", map_file=OutputHtmlFileName, state=state, year=year)

if __name__ == '__main__':
    app.run(debug=True)
