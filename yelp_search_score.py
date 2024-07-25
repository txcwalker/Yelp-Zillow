from .yelp_data import df7
import numpy as np

#Program used to create search score
#Date of last edit: 03/08/2024

df7 = df7.drop_duplicates(subset = 'id')
zip_occ = df7['location.zip_code'].value_counts()

#Removing zip codes which have less than 5 observations
zip_removal = []
for index, count in zip_occ.items():
    if count <=5:
        zip_removal.append(index)

#If zip code is not in zip_removal then keep and make a data frame
df_zip_search = df7[~df7['location.zip_code'].isin(zip_removal)]

#Same zip codes 'code' but for cities
city_occ = df7['location.city'].value_counts()

city_removal = []
for index, count in city_occ.items():
    if count <=5:
        city_removal.append(index)

#If city is not in "city removal" keep otherwise discard
df_city_search = df7[~df7['location.city'].isin(city_removal)]

#Creating Search Score
df_search = df7
#Use .loc to modify the DataFrame
#Actual metric creation score = rating^2 * ln(review_count)
df_search.loc[:, 'search_score'] = np.square(df_search['rating']) * np.log(df_search['review_count'])

#top serach scores
df_top_search = df_search.sort_values(by = 'search_score', ascending = False)

#Getting Search score Summary statistics by zip, city and state
#For some reason when this is not commented out it prevents the search_score_report from running so it commented it our
#for now...
"""df_zip_search['search_score'] = np.square(df_zip_search['rating'])*np.log(df_zip_search['review_count'])
df_top_zip_search = df_zip_search.sort_values(by = 'search_score', ascending = False)

df_city_search['search_score'] = np.square(df_city_search['rating'])*np.log(df_city_search['review_count'])
df_top_city_search = df_city_search.sort_values(by = 'search_score', ascending = False)

df_zip_avg_search_score = df_zip_search.groupby('location.zip_code').mean()['search_score']
df_zip_med_search_score = df_zip_search.groupby('location.zip_code').median()['search_score']

df_city_avg_search_score = df_city_search.groupby('location.city').mean()['search_score']
df_city_med_search_score = df_city_search.groupby('location.city').median()['search_score']

df_state_avg_search_score = df_state_search.groupby('location.state').mean()['search_score']
df_state_med_search_score = df_state_search.groupby('location.state').median()['search_score']

#Overall search score mean/median
overall_search_mean = df_top_zip_search['search_score'].mean()
overall_search_median = df_top_zip_search['search_score'].median()

#Sorting to show best first
df_top_zip = df_zip_med_search_score.sort_values(ascending = False)
df_top_city = df_city_med_search_score.sort_values(ascending = False)
df_top_state = df_state_med_search_score.sort_values(ascending = False)"""

#Choosing targets
#Zip Target
search_target =['10025'] #These can be changed to fit the situation

zip_search_score = df_top_search[df_top_search['location.zip_code'].isin(search_target)]
zip_search_output = zip_search_score

#City Target
city_target = ['Pinecrest']

city_search_score = df_top_search[df_top_search['location.city'].isin(city_target)]
city_score_output = city_search_score