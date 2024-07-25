import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap
from .yelp_data import df5, df7

#Creating Three Heat maps (one for each yelp variable, This was not used in the code but the visuals created could be
#used later in a report or somewhere else on the site, They are saved in the graphs and charts file
#Date of last edit: 03/08/2024

#Combined Map of US Cities and number of restaurant reviews
#Create a map centered around US
US_map_yelp_reviews = folium.Map(location=[36.966428, -95.844032], zoom_start=5)

#Creating a list of all the coordinate pairs and the variable being measured (review_count) in this case
locations_reviews = []
for index, row in df5.iterrows():
    lat, lon = row['coordinates.latitude'], row['coordinates.longitude']
    reviews = row['review_count']
    locations_reviews.append([lat, lon, reviews])

#Create a HeatMap layer based on review counts
heat_map = folium.plugins.HeatMap(locations_reviews, radius=15, legend_name='Review Counts',
                                  #Gradient is the variable to set up a color scale
                                  gradient ={0:'violet',.166:'indigo',.33:'blue',.5:'green',.666:'yellow',.833:'orange',
                                             1:'red'})

#Add the HeatMap layer to the map
heat_map.add_to(US_map_yelp_reviews)

#Create a linear colormap for the legend
reviews_colormap = LinearColormap(colors=['violet','indigo','blue','green', 'yellow','orange','red'],
                                  vmin=min(df5['review_count']), vmax=max(df5['review_count']))

#Add legend to the map
reviews_colormap.add_to(US_map_yelp_reviews)

#Save the map as an HTML file
US_map_yelp_reviews.save('US_Number_of_Reviews_HeatMap.html')

#Combined Map of US Cities and price
#Create a map centered around US
US_map_yelp_price = folium.Map(location=[36.966428, -95.844032], zoom_start=5)

#Creating a list of all the coordinate pairs and the variable being measured (price) in this case
locations_price = []
for index, row in df7.iterrows():
    lat, lon = row['coordinates.latitude'], row['coordinates.longitude']
    price = row['price']
    locations_price.append([lat, lon, price])

#Create a HeatMap layer based on review counts
heat_map = folium.plugins.HeatMap(locations_price, radius=12,
                                  gradient ={0:'violet',.166:'indigo',.33:'blue',.5:'green',.666:'yellow',.833:'orange'
                                             ,1:'red'} )

#Add the HeatMap layer to the map
heat_map.add_to(US_map_yelp_price)

#Create a linear colormap for the legend
price_colormap = LinearColormap(colors=['violet','indigo','blue','green', 'yellow','orange','red'],
                                vmin=min(df7['price']), vmax=max(df7['price']))

#Add legend to the map
price_colormap.add_to(US_map_yelp_price)

#Save the map as an HTML file
US_map_yelp_price.save('US_Yelp_Price_HeatMap.html')

#Combined Map of US Cities and number of restaurant rating

#Create a map centered around US
US_map_yelp_rating = folium.Map(location=[36.966428, -95.844032], zoom_start=5)

#Creating a list of all the coordinate pairs and the variable being measured (RATING) in this case
locations_rating = []
for index, row in df7.iterrows():
    lat, lon = row['coordinates.latitude'], row['coordinates.longitude']
    rating = row['rating']
    locations_rating.append([lat, lon, rating])

#Create a HeatMap layer based on review counts
heat_map = folium.plugins.HeatMap(locations_rating, radius=12,
                                  gradient ={0:'violet',.166:'indigo',.33:'blue',.5:'green',.666:'yellow',.833:'orange'
                                             ,1:'red'})

#Create a linear colormap for the legend
price_colormap = LinearColormap(colors=['green', 'yellow', 'red'], vmin=min(df7['rating']), vmax=max(df7['rating']))

#Add the HeatMap layer to the map
heat_map.add_to(US_map_yelp_rating)

#Create a linear colormap for the legend
rating_colormap = LinearColormap(colors=['violet','indigo','blue','green', 'yellow','orange','red'],
                                 vmin=min(df7['rating']), vmax=max(df7['rating']))

#Add legend to the map
rating_colormap.add_to(US_map_yelp_rating)

#Save the map as an HTML file
US_map_yelp_rating.save('US_Yelp_Rating_HeatMap.html')
