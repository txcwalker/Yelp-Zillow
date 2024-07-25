from flask import render_template, request, Blueprint
import plotly.express as px
from .yelp_data import df5, df6

#Python code for page dedicated to showing tag (bar) graphs of any city, state or zip code
#Date of last edit: 03/08/2024

yelp_tag_graph_tool = Blueprint("tag_graph_tool", __name__, template_folder = 'templates')

#Route for showing the tag graphs page
@yelp_tag_graph_tool.route('/YelpData/tag_graph_tool', methods=['GET']) #path name
def get_yelp_data():
    #Grabbing the cities, states and zip codes to be used in the dropdown menus
    states = sorted(df5['location.state'].unique())

    # Taking cities with 10 or greater observations as a work around for misspellings, unintentional observatoins, etc
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
        'Johns Island', 'Richmond Heights', 'Reseda', 'Ridgeland', 'Huntington Park', 'West Sacramento',
        'Warr Acres',
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
    # Applying the above

    df10 = df5[df5['location.city'].isin(approved_cities)]

    cities = sorted(df10['location.city'].unique())
    zip_codes = df5['location.zip_code'].sort_values().unique()
    return render_template('yelp_tag_graph_tool.html', states=states, cities = cities, zip_codes = zip_codes) #file name

#Route for updating the tag graphs (all of them but can be updated one at a time
@yelp_tag_graph_tool.route('/YelpData/tag_graph_tool', methods=['POST'])#path name
def update_tag_graph():

    #Determining which graph to update from user input
    form_type = request.form.get("form_type")

    if form_type == 'states':
        #Determing which state(s) were selected by the user
        target_states = request.form.getlist('target_states')

        #Filtering top x tags in state(s) selected
        df_states_tags_filtered = df6[df6['location.state'].isin(target_states)]
        df_states_graph_filtered = df_states_tags_filtered.tags.value_counts()[:10]

        #Defines the bar graph
        fig = px.bar(x=df_states_graph_filtered.index, y=df_states_graph_filtered,
                     labels={'index': 'Tags', 'y': 'Total Count'},
                     title=f'Most Common Restaurant Tags in: {", ".join(target_states)}',
                     color_discrete_sequence = px.colors.sequential.Viridis,
                     color = df_states_graph_filtered)
        #Customizing the appearance of the bar chart
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text=f'Most Common Restaurant Tags in: {", ".join(target_states)}',
                          title_x=0.5,  # Center the title
                          xaxis_title='Tags',
                          yaxis_title='Total Count',
                          font=dict(family='Arial, sans-serif', size=12, color='darkgrey'),
                          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                          plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                          margin=dict(l=50, r=50, b=50, t=80))  # Adjust margins

        #Render the template with the graph data
        return fig.to_json()

    elif form_type == 'cities':
        #Determines which city(ies) were selected by the user
        target_cities = request.form.getlist('target_cities')

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
            'Johns Island', 'Richmond Heights', 'Reseda', 'Ridgeland', 'Huntington Park', 'West Sacramento',
            'Warr Acres',
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

        #Applying the above
        df10 = df6[df6['location.city'].isin(approved_cities)]

        #Filtering DF by selected city(ies) for top x tags
        df_cities_tags_filtered = df10[df10['location.city'].isin(target_cities)]
        df_cities_graph_filtered = df_cities_tags_filtered.tags.value_counts()[:10]

        #Defining the graph
        fig = px.bar(x=df_cities_graph_filtered.index, y=df_cities_graph_filtered,
                     labels={'index': 'Tags', 'y': 'Total Count'},
                     title=f'Most Common Restaurant Tags in: {", ".join(target_cities)}',
                     color_discrete_sequence=px.colors.sequential.Viridis,
                     color =df_cities_graph_filtered)
        # Customizing the appearance of the bar chart
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text=f'Most Common Restaurant Tags in: {", ".join(target_cities)}',
                          title_x=0.5,
                          xaxis_title='Tags',
                          yaxis_title='Total Count',
                          font=dict(family='Arial, sans-serif', size=12, color='darkgrey'),
                          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                          plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                          margin=dict(l=50, r=50, b=50, t=80))  # Adjust margins

        #Render the template with the graph data
        return fig.to_json()

    else:
        #Determining which zip code(s) were selected by the user
        target_zip_codes = request.form.getlist('target_zip_codes')

        #Filters top x tags from the requested zip codes
        df_zip_codes_tags_filtered = df6[df6['location.zip_code'].isin(target_zip_codes)]
        df_zip_codes_graph_filtered = df_zip_codes_tags_filtered.tags.value_counts()[:10]

        #Defines the Bar graph
        fig = px.bar(x=df_zip_codes_graph_filtered.index, y=df_zip_codes_graph_filtered,
                     labels={'index': 'Tags', 'y': 'Total Count'},
                     title=f'Most Common Restaurant Tags in: {", ".join(target_zip_codes)}',
                     color_discrete_sequence=px.colors.sequential.Viridis,
                     color = df_zip_codes_graph_filtered)

        #Customizing the appearance of the bar chart
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text=f'Most Common Restaurant Tags in: {", ".join(target_zip_codes)}',
                          title_x=0.5,  # Center the title
                          xaxis_title='Tags',
                          yaxis_title='Total Count',
                          font=dict(family='Arial, sans-serif', size=12, color='darkgrey'),
                          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                          plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                          margin=dict(l=50, r=50, b=50, t=80))  # Adjust margins

    # Render the template with the graph data
    return fig.to_json()

