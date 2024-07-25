import plotly.express as px
import yelp_data

#Code used in the heat_maps_tool. no differences
#Date of last edit: 03/08/2024


df5 = yelp_data.df5
df7 = yelp_data.df7

# Combined Map of US Cities and number of restaurant reviews
fig_reviews = px.scatter_mapbox(df5, lat='coordinates.latitude', lon='coordinates.longitude', color='review_count',
                                size='review_count', color_continuous_scale='Deep',
                                center=dict(lat=36.966428, lon=-95.844032), zoom=5, mapbox_style="carto-positron",
                                title='US Yelp Reviews Scatter Map', size_max=15)
fig_reviews.show()

# Combined Map of US Cities and price
fig_price = px.scatter_mapbox(df7, lat='coordinates.latitude', lon='coordinates.longitude', color='price',
                              size='price', color_continuous_scale='Algae',
                              center=dict(lat=36.966428, lon=-95.844032), zoom=5,
                              mapbox_style="carto-positron", title='US Yelp Price Scatter Map', size_max=7)
fig_price.show()

# Combined Map of US Cities and number of restaurant rating
fig_rating = px.scatter_mapbox(df7, lat='coordinates.latitude', lon='coordinates.longitude', color='rating',
                               size='rating', color_continuous_scale='Tempo',
                               center=dict(lat=36.966428, lon=-95.844032), zoom=5,
                               mapbox_style="carto-positron", title='US Yelp Rating Scatter Map', size_max=5)
fig_rating.show()

