from flask import render_template, request, Blueprint
import plotly.express as px
from .yelp_data import df5
import pandas as pd

#Date of last edit: 03/08/2024

yelp_heat_map_tool = Blueprint("heat_map_tool", __name__, template_folder = 'templates')

#route to load page
@yelp_heat_map_tool.route('/YelpData/heat_map_tool', methods=['GET'])
def get_heat_map():
    #Sorts unique cities alphabetically and sets up drop down for all cities
    #Taking cities with 10 or greater observations as a work around for misspellings, unintentional observatoins, etc
    approved_cities = [
        'Chicago', 'New York', 'Los Angeles', 'Portland', 'Honolulu', 'Nashville', 'Brooklyn',
        'San Francisco', 'Seattle', 'San Diego', 'Las Vegas', 'Houston', 'Dallas', 'Philadelphia',
        'Denver', 'Austin', 'Sacramento', 'Phoenix', 'Atlanta', 'Long Beach', 'Tucson', 'San Antonio',
        'Charlotte', 'Albuquerque', 'Pittsburgh', 'Raleigh', 'Fresno', 'Baltimore', 'Tampa', 'New Orleans',
        'Charleston', 'Columbus', 'Orlando', 'San Jose', 'Kansas City', 'Richmond', 'Louisville',
        'Minneapolis', 'Fort Worth', 'Tulsa', 'Indianapolis', 'Jacksonville', 'Omaha', 'Oklahoma City',
        'Boston', 'Reno', 'Salt Lake City', 'Rochester', 'Milwaukee', 'Boise', 'Cleveland', 'Oakland',
        'Memphis', 'Miami', 'Buffalo', 'Cincinnati', 'Detroit', 'Anchorage', 'El Paso', 'Birmingham',
        'Providence', 'New Haven', 'Des Moines', 'Anaheim', 'Wilmington', 'Mobile', 'Little Rock', 'Santa Fe',
        'Saint Louis', 'Sioux Falls', 'Montgomery', 'Manchester', 'Hartford', 'Billings', 'Orange', 'St. Louis',
        'Culver City', 'Dover', 'Van Nuys', 'Cheyenne', 'Burlington', 'Sparks', 'Compton', 'West Hartford',
        'Coral Gables', 'Berkeley', 'Gardena', 'Flushing', 'Fullerton', 'Cambridge', 'Windsor', 'Queens',
        'South Portland', 'Astoria', 'Hamden', 'Alameda', 'Garden Grove', 'Jackson', 'Sherman Oaks',
        'North Charleston', 'Santa Monica', 'Cranston', 'West Haven', 'Mission', 'West Hollywood',
        'North Hollywood', 'Santa Clara', 'Homewood', 'Carson', 'Covington', 'Shawnee', 'Bronx', 'Elmhurst',
        'Lakewood', 'Forest Hills', 'Doral', 'Fargo', 'Pawtucket', 'Jackson Heights', 'Campbell',
        'Long Island City', 'Newport', 'Johnston', 'Cheektowaga', 'Santa Ana', 'South Burlington',
        'Vestavia Hills', 'Somerville', 'Lynwood', 'Clovis', 'North Little Rock', 'St Louis', 'West Valley City',
        'East Hartford', 'South Gate', 'Marina Del Rey', 'Glastonbury', 'Encino', 'North Haven',
        'Wethersfield', 'East Providence', 'Northridge', 'Ridgewood', 'Venice', 'Newington', 'Dearborn',
        'Beverly Hills', 'East Haven', 'Paramount', 'Emeryville', 'Brookline', 'Garden City', 'Wauwatosa',
        'North Providence', 'Amherst', 'West Allis', 'Tonawanda', 'Studio City', 'La Vista', 'Clayton', 'Downey',
        'Woodside', 'Williamsville', 'Decatur', 'Henrico', 'Glendale', 'Jamaica', 'Panorama City', 'Haltom City',
        'Torrance', 'Hoover', 'Arlington', 'Maplewood', 'Bedford', 'Scarborough', 'Westbrook', 'Mountain Brook',
        'Brea', 'San Fernando Valley', 'Mount Pleasant', 'Jeffersonville', 'Kirkwood', 'Hamtramck', 'Parma',
        'South Salt Lake', 'Seal Beach', 'Hooksett', 'North Kansas City', 'Sunnyside', 'West Des Moines',
        'Signal Hill', 'Urban Honolulu', 'Tampa Bay', 'New Castle', 'Bloomfield', 'Inglewood', 'Camden',
        'Webster Groves', 'Gretna', 'Colchester', 'Independence', 'Falmouth', 'South Miami', 'Corona', 'Winooski',
        'South Charleston', 'Jenks', 'Brentwood', 'Rego Park', 'University City', 'Papillion', 'Newark',
        'Metairie', 'Bellevue', 'Bellflower', 'Coronado', 'Artesia', 'Granada Hills', 'Cerritos', 'Miami Springs',
        'Johns Island', 'Richmond Heights', 'Reseda', 'Ridgeland', 'Huntington Park', 'West Sacramento', 'Warr Acres',
        'El Segundo', 'Valley Village', 'North Hills', 'Tarzana', 'Tustin', 'Greenfield', 'Bayside', 'San Fernando',
        'Edina', 'Saint Paul', 'Upper Arlington', 'Kenmore', 'Merriam', 'Placentia', 'Kew Gardens', 'Pearl',
        'New Britain', 'Glen Allen', 'Irondale', 'Edgewater', 'North Salt Lake', 'Fort Bliss', 'West Milwaukee',
        'Hollywood', 'Central Falls', 'Coconut Grove', 'Londonderry', 'Windsor Heights', 'Towson', 'Shelburne',
        'Dorchester', 'Urbandale', 'Harvey', 'Maspeth', 'Worthington', 'Shorewood', 'Seekonk', 'Parkville',
        'Los Gatos', 'Chamblee', 'St Louis Park', 'Moorhead', 'Henrietta', 'Ciudad Juarez', 'Castle Hills', 'Bell',
        'Brookhaven', 'Crescent Springs', 'Bellaire', 'Lake Worth', 'Essex Junction', 'Fresh Meadows', 'Riverside',
        'Sun Valley', 'Lincoln', 'South Windsor', 'Branford', 'Garnet Valley', 'Mission Hills', 'Woodbridge',
        'Fort Lee', 'Rocky Hill', 'Playa Del Rey', 'Orinda', 'Highland Park', 'Bell Gardens', 'St. Louis Park',
        'Milford', 'Sausalito', 'Woodhaven', 'Yorba Linda', 'Warwick', 'Bartlett', 'East Elmhurst', 'Hialeah',
        'Overland Park', 'Middle Village', 'Pacoima', 'Greenville', 'Cape Elizabeth', 'Valley View', 'Farmington',
        'Crown Heights', 'West Fargo', 'National City', 'Bexley', 'Beech Grove', 'Phila', 'Jamaica Plain',
        'Richmond Hill', 'West Miami', 'Ft. Worth', 'San Leandro', 'Glen Mills', 'Juarez', 'Goffstown', 'Greece',
        'Cliffside Park', 'Irondequoit', 'Prairie Village', 'Albany', 'Chadds Ford', 'Arleta', 'Columbia Heights'
    ]
    df10 = df5[df5['location.city'].isin(approved_cities)]
    heat_cities = sorted(df10['location.city'].unique())
    return render_template('yelp_heat_map_tool.html', cities = heat_cities)

#Route to update heat map
@yelp_heat_map_tool.route('/YelpData/heat_map_tool', methods=['POST'])
def update_heat_map():

    #Taking cities with 10 or greater observations as a work around for misspellings, unintentional observatoins, etc
    approved_cities = [
        'Chicago', 'New York', 'Los Angeles', 'Portland', 'Honolulu', 'Nashville', 'Brooklyn',
        'San Francisco', 'Seattle', 'San Diego', 'Las Vegas', 'Houston', 'Dallas', 'Philadelphia',
        'Denver', 'Austin', 'Sacramento', 'Phoenix', 'Atlanta', 'Long Beach', 'Tucson', 'San Antonio',
        'Charlotte', 'Albuquerque', 'Pittsburgh', 'Raleigh', 'Fresno', 'Baltimore', 'Tampa', 'New Orleans',
        'Charleston', 'Columbus', 'Orlando', 'San Jose', 'Kansas City', 'Richmond', 'Louisville',
        'Minneapolis', 'Fort Worth', 'Tulsa', 'Indianapolis', 'Jacksonville', 'Omaha', 'Oklahoma City',
        'Boston', 'Reno', 'Salt Lake City', 'Rochester', 'Milwaukee', 'Boise', 'Cleveland', 'Oakland',
        'Memphis', 'Miami', 'Buffalo', 'Cincinnati', 'Detroit', 'Anchorage', 'El Paso', 'Birmingham',
        'Providence', 'New Haven', 'Des Moines', 'Anaheim', 'Wilmington', 'Mobile', 'Little Rock', 'Santa Fe',
        'Saint Louis', 'Sioux Falls', 'Montgomery', 'Manchester', 'Hartford', 'Billings', 'Orange', 'St. Louis',
        'Culver City', 'Dover', 'Van Nuys', 'Cheyenne', 'Burlington', 'Sparks', 'Compton', 'West Hartford',
        'Coral Gables', 'Berkeley', 'Gardena', 'Flushing', 'Fullerton', 'Cambridge', 'Windsor', 'Queens',
        'South Portland', 'Astoria', 'Hamden', 'Alameda', 'Garden Grove', 'Jackson', 'Sherman Oaks',
        'North Charleston', 'Santa Monica', 'Cranston', 'West Haven', 'Mission', 'West Hollywood',
        'North Hollywood', 'Santa Clara', 'Homewood', 'Carson', 'Covington', 'Shawnee', 'Bronx', 'Elmhurst',
        'Lakewood', 'Forest Hills', 'Doral', 'Fargo', 'Pawtucket', 'Jackson Heights', 'Campbell',
        'Long Island City', 'Newport', 'Johnston', 'Cheektowaga', 'Santa Ana', 'South Burlington',
        'Vestavia Hills', 'Somerville', 'Lynwood', 'Clovis', 'North Little Rock', 'St Louis', 'West Valley City',
        'East Hartford', 'South Gate', 'Marina Del Rey', 'Glastonbury', 'Encino', 'North Haven',
        'Wethersfield', 'East Providence', 'Northridge', 'Ridgewood', 'Venice', 'Newington', 'Dearborn',
        'Beverly Hills', 'East Haven', 'Paramount', 'Emeryville', 'Brookline', 'Garden City', 'Wauwatosa',
        'North Providence', 'Amherst', 'West Allis', 'Tonawanda', 'Studio City', 'La Vista', 'Clayton', 'Downey',
        'Woodside', 'Williamsville', 'Decatur', 'Henrico', 'Glendale', 'Jamaica', 'Panorama City', 'Haltom City',
        'Torrance', 'Hoover', 'Arlington', 'Maplewood', 'Bedford', 'Scarborough', 'Westbrook', 'Mountain Brook',
        'Brea', 'San Fernando Valley', 'Mount Pleasant', 'Jeffersonville', 'Kirkwood', 'Hamtramck', 'Parma',
        'South Salt Lake', 'Seal Beach', 'Hooksett', 'North Kansas City', 'Sunnyside', 'West Des Moines',
        'Signal Hill', 'Urban Honolulu', 'Tampa Bay', 'New Castle', 'Bloomfield', 'Inglewood', 'Camden',
        'Webster Groves', 'Gretna', 'Colchester', 'Independence', 'Falmouth', 'South Miami', 'Corona', 'Winooski',
        'South Charleston', 'Jenks', 'Brentwood', 'Rego Park', 'University City', 'Papillion', 'Newark',
        'Metairie', 'Bellevue', 'Bellflower', 'Coronado', 'Artesia', 'Granada Hills', 'Cerritos', 'Miami Springs',
        'Johns Island', 'Richmond Heights', 'Reseda', 'Ridgeland', 'Huntington Park', 'West Sacramento', 'Warr Acres',
        'El Segundo', 'Valley Village', 'North Hills', 'Tarzana', 'Tustin', 'Greenfield', 'Bayside', 'San Fernando',
        'Edina', 'Saint Paul', 'Upper Arlington', 'Kenmore', 'Merriam', 'Placentia', 'Kew Gardens', 'Pearl',
        'New Britain', 'Glen Allen', 'Irondale', 'Edgewater', 'North Salt Lake', 'Fort Bliss', 'West Milwaukee',
        'Hollywood', 'Central Falls', 'Coconut Grove', 'Londonderry', 'Windsor Heights', 'Towson', 'Shelburne',
        'Dorchester', 'Urbandale', 'Harvey', 'Maspeth', 'Worthington', 'Shorewood', 'Seekonk', 'Parkville',
        'Los Gatos', 'Chamblee', 'St Louis Park', 'Moorhead', 'Henrietta', 'Ciudad Juarez', 'Castle Hills', 'Bell',
        'Brookhaven', 'Crescent Springs', 'Bellaire', 'Lake Worth', 'Essex Junction', 'Fresh Meadows', 'Riverside',
        'Sun Valley', 'Lincoln', 'South Windsor', 'Branford', 'Garnet Valley', 'Mission Hills', 'Woodbridge',
        'Fort Lee', 'Rocky Hill', 'Playa Del Rey', 'Orinda', 'Highland Park', 'Bell Gardens', 'St. Louis Park',
        'Milford', 'Sausalito', 'Woodhaven', 'Yorba Linda', 'Warwick', 'Bartlett', 'East Elmhurst', 'Hialeah',
        'Overland Park', 'Middle Village', 'Pacoima', 'Greenville', 'Cape Elizabeth', 'Valley View', 'Farmington',
        'Crown Heights', 'West Fargo', 'National City', 'Bexley', 'Beech Grove', 'Phila', 'Jamaica Plain',
        'Richmond Hill', 'West Miami', 'Ft. Worth', 'San Leandro', 'Glen Mills', 'Juarez', 'Goffstown', 'Greece',
        'Cliffside Park', 'Irondequoit', 'Prairie Village', 'Albany', 'Chadds Ford', 'Arleta', 'Columbia Heights'
    ]
    df10 = df5[df5['location.city'].isin(approved_cities)]

    #Sets target variables
    #City selected from dropdown
    target_city = request.form.get("target_city")

    #Target variable selected from dropdown
    target_variable = request.form.get("target_variable")

    #Filter the DataFrame based on the target city
    df_filtered = df10[df10['location.city'] == target_city].dropna(subset=[target_variable])

    #Graphs by target variable
    #px.scatter_plot plots points on map, color and size variables assign scale values to observations
    if target_variable == 'review_count':
        # Combined Map of US Cities and number of restaurant reviews
        fig = px.scatter_mapbox(df_filtered, lat='coordinates.latitude', lon='coordinates.longitude',
                                color='review_count', size='review_count', color_continuous_scale='Plasma', hover_name= 'name',
                                center=dict(lat=df_filtered['coordinates.latitude'].mean(),
                                            lon=df_filtered['coordinates.longitude'].mean()), zoom=10,
                                mapbox_style="carto-positron", title=f'{target_city} Yelp Reviews Scatter Map',
                                size_max=15)

    elif target_variable == 'price':
        # Combined Map of US Cities and number of restaurant reviews
        fig = px.scatter_mapbox(df_filtered, lat='coordinates.latitude', lon='coordinates.longitude',
                                color='price', size='price', color_continuous_scale='Plotly3', hover_name= 'name',
                                center=dict(lat=df_filtered['coordinates.latitude'].mean(),
                                            lon=df_filtered['coordinates.longitude'].mean()), zoom=10,
                                mapbox_style="carto-positron", title=f'{target_city} Yelp Price Scatter Map',
                                size_max=8)

    else:
        # Combined Map of US Cities and number of restaurant reviews
        fig = px.scatter_mapbox(df_filtered, lat='coordinates.latitude', lon='coordinates.longitude',
                                color='rating', size='rating', color_continuous_scale='YlGnBu', hover_name= 'name',
                                center=dict(lat=df_filtered['coordinates.latitude'].mean(),
                                            lon=df_filtered['coordinates.longitude'].mean()), zoom=10,
                                mapbox_style="carto-positron", title=f'{target_city} Yelp Rating Scatter Map',
                                size_max=6)
    return fig.to_json()