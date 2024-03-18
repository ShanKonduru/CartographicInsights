from flask import Flask, render_template, request
from Utilities.CustomLogger import CustomLogger 
from PlotMe import PlotMe 
import pandas as pd
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/NewIndex')
def newindex():
    return render_template('NewIndex.html')

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
    
    OutputHtmlFileName = f'output_TotalSales.html'  # Define the output HTML file name

    if(os.path.exists(OutputHtmlFileName)):
        os.remove(OutputHtmlFileName)

    logger.debug('***************************  Begin generate_total_sales_map')
    plotter.generate_total_sales_map(OutputHtmlFileName)
    logger.debug('***************************  End generate_total_sales_map')

    logger.debug('*************************** Looking for OutputHtmlFileName file exists :' + OutputHtmlFileName)
    time.sleep(2)  # Check every second
    logger.debug('*************************** The OutputHtmlFileName file exists :' + OutputHtmlFileName)

    # Render the map in the HTML template
    logger.debug('*************************** render_template')
    return render_template("MapTemplate.html", map_file=OutputHtmlFileName, state='All states', year='all years')

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

    OutputHtmlFileName = f'output_{year}_{state}.html'  # Define the output HTML file name

    if(os.path.exists(OutputHtmlFileName)):
        os.remove(OutputHtmlFileName)

    logger.debug('***************************  Begin generate_filtered_sales_map')
    plotter.generate_filtered_sales_map(OutputHtmlFileName, YearOfSale=year, State=state)
    # plotter.generate_filtered_sales_map(OutputHtmlFileName,State="Utah", Season="Spring")
    logger.debug('***************************  End generate_filtered_sales_map')

    logger.debug('*************************** Looking for OutputHtmlFileName file exists :' + OutputHtmlFileName)
    # Check if the file exists
    # while not os.path.exists(OutputHtmlFileName):
    time.sleep(2)  # Check every second
    logger.debug('*************************** The OutputHtmlFileName file exists :' + OutputHtmlFileName)

    # Render the map in the HTML template
    logger.debug('*************************** render_template')
    return render_template("MapTemplate.html", map_file=OutputHtmlFileName, state=state, year=year)

@app.route('/generate_timezone_map', methods=['GET'])
def generate_timezone_map():
    # Retrieve form data
    # Read sales data from CSV file
    sales_data_df = pd.read_csv("Dataset/GeographicDataAnalysis.csv")

    shapefile_path = 'MapData/ne_110m_admin_1_states_provinces.shp'  # Provide the path to your shapefile
    sales_data_df = sales_data_df  # You need to load your sales data DataFrame here

    # Create an instance of CustomLogger with both console and file logging
    logger = CustomLogger(debug_mode=True, log_file="Logs/app.log")
    

    plotter = PlotMe(shapefile_path, sales_data_df, logger)
    
    # Extract the year and state parameters from the URL query string
    timeZone = request.args.get('Timezone')
    salesManager = request.args.get('SalesManager')

    if not timeZone or not salesManager:
        return "'timeZone' and 'salesManager' parameters are required."

    OutputHtmlFileName = f'output_{timeZone}_{salesManager}.html'  # Define the output HTML file name

    if(os.path.exists(OutputHtmlFileName)):
        os.remove(OutputHtmlFileName)

    logger.debug('***************************  Begin generate_filtered_sales_map')
    plotter.generate_filtered_sales_map(OutputHtmlFileName, TimeZone=timeZone, SalesManager=salesManager)
    # plotter.generate_filtered_sales_map(OutputHtmlFileName,State="Utah", Season="Spring")
    logger.debug('***************************  End generate_filtered_sales_map')

    logger.debug('*************************** Looking for OutputHtmlFileName file exists :' + OutputHtmlFileName)
    # Check if the file exists
    # while not os.path.exists(OutputHtmlFileName):
    time.sleep(2)  # Check every second
    logger.debug('*************************** The OutputHtmlFileName file exists :' + OutputHtmlFileName)

    # Render the map in the HTML template
    logger.debug('*************************** render_template')
    return render_template("MapTemplate.html", map_file=OutputHtmlFileName, state='ALL', year='ALL')

@app.route('/generate_filtered_map', methods=['GET'])
def generate_filtered_map():
    
     # Create an instance of CustomLogger with both console and file logging
    logger = CustomLogger(debug_mode=True, log_file="Logs/app.log")

    logger.debug("***************************  Request received at /generate_filtered_map")
    query_params_str = ", ".join([f"{key}={value}" for key, value in request.args.items()])
    logger.debug("***************************  Query parameters: " + query_params_str)
    
    # Retrieve query string parameters
    query_params = request.args.to_dict()
    logger.debug("***************************  Query parameters:" + str(query_params))

    # Remove 'Dropdown' from the keys if present
    for key in list(query_params.keys()):
        if key.endswith('Dropdown'):
            query_params[key[:-8]] = query_params.pop(key)
    
    # Retrieve form data
    # Read sales data from CSV file
    sales_data_df = pd.read_csv("Dataset/GeographicDataAnalysis.csv")

    shapefile_path = 'MapData/ne_110m_admin_1_states_provinces.shp'  # Provide the path to your shapefile
    sales_data_df = sales_data_df  # You need to load your sales data DataFrame here

   
    plotter = PlotMe(shapefile_path, sales_data_df, logger)
    
    # Define the output HTML file name
    OutputHtmlFileName = f'output_{"_".join([f"{key}={value}" for key, value in query_params.items()])}.html'.replace('=', '_')

    if(os.path.exists(OutputHtmlFileName)):
        os.remove(OutputHtmlFileName)

    logger.debug('***************************  Begin generate_filtered_sales_map')
    plotter.generate_filtered_sales_map(OutputHtmlFileName, **query_params)
    logger.debug('***************************  End generate_filtered_sales_map')

    logger.debug('*************************** Looking for OutputHtmlFileName file exists :' + OutputHtmlFileName)
    # Check if the file exists
    # while not os.path.exists(OutputHtmlFileName):
    time.sleep(2)  # Check every second
    logger.debug('*************************** The OutputHtmlFileName file exists :' + OutputHtmlFileName)

    # Render the map in the HTML template
    logger.debug('*************************** render_template')
    return render_template("MapTemplate.html", map_file=OutputHtmlFileName, state='ALL', year='ALL')

if __name__ == '__main__':
    app.run(debug=True)
