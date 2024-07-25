#This was the code used to gather the the Yelp data from the Yelp API. It should be noted this process was not perfect,
#the yelp API calls only allow for a certain amount per day and an even smaller amount per call. So say each call maxes
#out at 2000 observations and you can make 1000 observations a day.
#additionally if trying to get more data on a specific location I tried a few different ways to accomplish this by calling
#the data by there different criteria but ended up getting overwhelmed by duplicates it was not worth the time or calls

#The average time to receive the observations per city was about 50 seconds

#Date of last edit: 03/07/2024

#Import Statements
import requests
import pandas as pd
import math


#Yelp API Key
api_key = 'vQMqGkqCcLaAMG8lAw3SkaXPdSXNAKFiQv6bXI3r0vB0-qK2u6Ybd-gUm_RqgHGugVzINg0agid6434QbXbHW9x2pFz_v2S9JsYG5gYDUavmvaXrqkmMrckLl0LnZHYx'

#API endpoint URL
endpoint = 'https://api.yelp.com/v3/businesses/search'

#Locations to be cycled through. After each time all business from a location are received data is saved as a csv and exported. Then
#a new location from the list below is chosen.
#Cities already run: San Francisco, San Diego, Denver, Chicago, Houston, Dallas, Miami, Austin, San Antonio, Oakland, Boston,
#Phoenix, Nashville, New Orleans, Philadelphia, Washington DC, Las Vegas, Omaha, Baltimore, Atlanta, Tampa Bay, Columbus, Cleveland
#Cincinnati, Orlando, Memphis,



# Set the search parameters for the API
params = {
    'location': 'Fargo',
    'limit': 50,  # Number of results per page
    'offset': 0,  # Initial offset
    'radius': 10000,  # X meters
    'term': 'food'
}

#Set the request headers with the API key
headers = {
    'Authorization': f'Bearer {api_key}'
}

response = requests.get(endpoint, params=params, headers=headers)
response_hold = response.json()

#Create an empty list to store business data
all_businesses = []

#These are all pseudo defined by yelp, the most observations at the start was 1000
page_limit = 50
request_limit = 950
total_obs = (request_limit / page_limit).__int__()
total_pages = math.ceil(response_hold['total'] / request_limit)
#Terms being serached
terms = ['food', 'restaurant']

#Loop until as much data as possible is received
for term in terms:
    params['term'] = term
    params['offset'] = 0
    while params['offset'] <= request_limit:
        response = requests.get(endpoint, params=params, headers=headers)
        #Check the status code
        if response.status_code == 200:
            response_test = response.json()
            all_businesses.append(response_test)  # Add fetched businesses to the list

        else:
            print(f"Request failed with status code: {response.status_code}")
            break
        params['offset'] += params['limit']  # Increase the offset for the next page

combined_df = pd.DataFrame()

for data in all_businesses:
    df_yelp_test = pd.json_normalize(data, 'businesses')
    # Concatenate the two DataFrames vertically
    combined_df = pd.concat([df_yelp_test, combined_df], ignore_index=True)

df2 = combined_df

#Apply a lambda function to extract values from dictionaries
df2['all_categories'] = df2['categories'].apply(lambda dicts_list: [d['title'] for d in dicts_list])

#Dropping a bunch of not needed columns
#Columns to drop (alias, image_url, is closed, catergories, phone, display phone,location,address2, location.address3)
# Columns to drop
columns_to_drop = ['alias', 'image_url', 'is_closed', 'categories', 'phone', 'display_phone', 'location.address2', 'location.address3']
df3 = df2.drop(columns=columns_to_drop)
#Remove dupelicate rows
df4 = df3.drop_duplicates(subset='id')


#Save data for city to csv so it doesnt need to be called from the API everytime
#Save the DataFrame to an existing CSV file without overriding
output_filename = 'yelp_cities_food_resetaurant.csv'
df4.to_csv(output_filename, mode='a', header=False, index=False)

