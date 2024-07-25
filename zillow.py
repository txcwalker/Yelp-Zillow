import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .yelp_data import df5

#Random Forest
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

#Imported to handle non ascii characters for ubuntu/apache process
import unicodedata

#Imported to handle loading data for ubuntu/apache process
import os

#Creating the Random Forest model for predict housing price based on Yelp Data
#Date of last edit: 03/08/2024


#Reading in the data_file, using this method for Apache/ubunutu
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'data', 'Zillow_SFR_Smooth_SeasonallyAdjusted_Value.csv')
df_zillow_raw = pd.read_csv(data_path, encoding = 'utf-8')

#Replacing non ascii characters
def replace_non_ascii_in_object_columns(df):
    for column in df.select_dtypes(include='object').columns:
        df[column] = df[column].apply(replace_non_ascii)

def replace_non_ascii(cell):
    return ''.join(char if ord(char) < 128 else unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('utf-8') for char in str(cell))

#Running the above functions
replace_non_ascii_in_object_columns(df_zillow_raw)


#Begining to clean the data, which columns to keep and renaming them
zillow_columns_to_keep = ['RegionName','State','City','Metro','CountyName']
df_zillow = df_zillow_raw[zillow_columns_to_keep + [df_zillow_raw.columns[-1]]]
zillow_rename_dict = {'RegionName': 'Zip_Code','CountyName':'County', '12/31/2023':'Price'}
df_zillow = df_zillow.rename(columns = zillow_rename_dict)

#Sorting by zip code, city and state and creating some metrics to review/compare
#Sorting by ZipCode
yelp_zip_group_mean = df5.groupby('location.zip_code')[['review_count','rating','price']].mean()
yelp_zip_group_sum = df5.groupby('location.zip_code')['review_count'].sum()
yelp_zip_group_med = df5.groupby('location.zip_code')[['review_count','rating','price']].median()

#Sorting by City
#df5.groupby('location.city')[['review_count','rating','price']].mean()
#df5.groupby('location.city')['review_count'].sum()
#df5.groupby('location.city')[['review_count','rating','price']].median()

#Sorting by State
yelp_state_group_mean = df5.groupby('location.state')[['review_count','rating','price']].mean()
yelp_state_group_sum = df5.groupby('location.state')['review_count'].sum()
yelp_state_group_median = df5.groupby('location.state')[['review_count','rating','price']].median()

#Merging the data sets together
#Merge yelp_zip_group_med with yelp_zip_group_sum based on the index
merged_df = pd.merge(yelp_zip_group_med, yelp_zip_group_sum, left_index=True, right_index=True, suffixes=('_med', '_sum'))

#Merge the resulting DataFrame with yelp_zip_group_mean based on the index
merged_df = pd.merge(merged_df, yelp_zip_group_mean, left_index=True, right_index=True, suffixes = (None, '_mean'))


merged_df.index = merged_df.index.astype(str)
df_zillow = df_zillow.set_index('Zip_Code')
df_zillow.index = df_zillow.index.astype(str)

#Merge the resulting DataFrame with df_zillow based on 'Zip Code'
df_zillow_yelp_zip = merged_df.merge(df_zillow, how = 'inner', left_index = True, right_index = True, suffixes = (None, '_zillow'))

#Final dataframe to use in analysis and model
df_zy_zip = df_zillow_yelp_zip.dropna()

#Analysis
#Renaming Columns
new_zy_zip_column_names = ({'rating':'rating_med','price':'price_med', 'Price':'Price_Zillow','review_count':'review_count_mean'})
df_zy_zip = df_zy_zip.rename(columns = new_zy_zip_column_names)

#Converting Categorical to Numerical Variables
label_encoder = LabelEncoder()

df_zy_zip['State'] = label_encoder.fit_transform(df_zy_zip['State'])
df_zy_zip['City'] = label_encoder.fit_transform(df_zy_zip['City'])
df_zy_zip['Metro'] = label_encoder.fit_transform(df_zy_zip['Metro'])
df_zy_zip['County'] = label_encoder.fit_transform(df_zy_zip['County'])

#Scaling not necessary since random forest is the chosen model
#df_zy_zip (unscaled)
X_train, X_test, y_train, y_test_x = train_test_split(
    df_zy_zip.drop(columns='Price_Zillow'),
    df_zy_zip['Price_Zillow'],
    test_size=0.25,
    random_state=42
)

#Creating the actual model (Random Forest)
#Train a Random Forest Regressor on the unscaled data
rf_unscaled = RandomForestRegressor(n_estimators=100, random_state=42)
rf_unscaled.fit(X_train, y_train)

#Predictions
#Unscaled
y_pred_unscaled = rf_unscaled.predict(X_test)

#Evaluate the model
#Unscaled
mse_unscaled = mean_squared_error(y_test_x, y_pred_unscaled)
r2_unscaled = r2_score(y_test_x, y_pred_unscaled)

#Printing MSE and R^2 to evaluate model performance
#Unscaled
#print("Metrics for Unscaled Data:")
#print("Mean Squared Error:", mse_unscaled)
#print("R-squared:", r2_unscaled)

#Ploting the vairables to visualize their importance in the model
#UnScaled

plt.clf()
plt.scatter(y_test_x, y_pred_unscaled)
plt.xlabel("True Values (Unscaled)")
plt.ylabel("Predictions (Unscaled)")
plt.title("Random Forest Regressor - Unscaled Data")


plt.axvline(x=750000, color='g', linestyle='-', label='x = 750000', lw = '2')
plt.axhline(y=750000, color='g', linestyle='-', label='y = 750000', lw = '2')

# Set x-axis limits
plt.xlim(0, 4000000)
plt.xticks(np.linspace(0, 4000000, num=17, endpoint=True))
#plt.show()

# Assuming you have y_test_x and y_pred_unscaled available #380,36,61,23
# Create a boolean mask for values less than 750,000
below_threshold_mask = (y_test_x > 750000) & (y_pred_unscaled < 750000)

# Count the number of True values in the mask
count_below_threshold = np.count_nonzero(below_threshold_mask)
#print(f"Number of observations where both y_test_x and y_pred_unscaled are < 750K: {count_below_threshold}")


#Visualizing individual variable importance
#Unscaled model
feature_importance_unscaled = rf_unscaled.feature_importances_
feature_names_unscaled = X_train.columns

#Sort features based on importance
sorted_idx_unscaled = feature_importance_unscaled.argsort()

#Plotting feature importance
plt.clf()
plt.figure(figsize=(10, 6))
plt.barh(range(len(sorted_idx_unscaled)), feature_importance_unscaled[sorted_idx_unscaled], align="center")
plt.yticks(range(len(sorted_idx_unscaled)), [feature_names_unscaled[i] for i in sorted_idx_unscaled])
plt.xlabel("Feature Importance (Unscaled)")
plt.title("Random Forest Feature Importance - Unscaled Data")

#plt.show()

#Calculate residuals (differences between predictions and true values)
residuals = y_test_x - y_pred_unscaled

#Identify indices of most incorrect and correct predictions
most_incorrect_indices = residuals.abs().sort_values(ascending=False)
most_correct_indices = residuals.abs().sort_values()

#Visualize the residuals
plt.clf()
plt.figure(figsize=(10, 6))
plt.scatter(range(len(residuals)), residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--', label='Zero Residuals')
plt.plot(np.unique(range(len(residuals))), np.poly1d(np.polyfit(range(len(residuals)), residuals, 1))(np.unique(range(len(
                                                    residuals)))), color='black', label='Line of Best Fit')

plt.xlabel("Sample Index")
plt.ylabel("Residuals (True - Predicted)")
plt.title("Residuals Analysis")
plt.yticks(np.linspace(-1400000, 3000000, num=23, endpoint=True))
plt.legend()
#plt.show()

#Create a new column indicating whether the prediction was above or below the actual value
#Unscaled
df_results = pd.DataFrame({'True': y_test_x, 'Predicted': y_pred_unscaled, 'Residual': residuals})

#Create a binary column to maintain whether or not residual was positive or negative
#Unscaled
df_results['Undervalued'] = np.where(df_results['Residual'] > 0, 1, 0)
df_results['Ovevalued'] = np.where(df_results['Residual'] <= 0, 1, 0)

#Sorting by biggest miss
#Unscaled
df_results['Residual_ABS'] = df_results['Residual'].abs()
df_results = df_results.sort_values('Residual_ABS', ascending = False)

#Plotting the results on a map

#Getting the average coordinates by zip code
df8 = df5[['location.zip_code','coordinates.latitude','coordinates.longitude']]
df_avg_coords = df8.groupby('location.zip_code').mean()

#Merge the resulting DataFrame with df_zillow based on 'Zip Code'
#Unscaled
df_results_plot = df_results.merge(df_avg_coords, how = 'inner', left_index = True, right_index = True)

#import Plotly
import plotly.express as px

#Making the figure
fig = px.scatter_mapbox(df_results_plot,
                        lat='coordinates.latitude',
                        lon='coordinates.longitude',
                        color='Residual',
                        size = 'Residual_ABS',
                        title='Residuals Plot',
                        labels={'residuals': 'Residuals', 'Residual': 'Size'},
                        color_continuous_scale='Turbo',
                        size_max=20,
                        hover_name = df_results_plot.index,
                        hover_data={'Residual': True},
                        zoom = 3,
                        mapbox_style='carto-positron')

#fig.show()

#Least Accurate

#Getting 25 most accurate predictions
df_results_plot_least = df_results_plot.sort_values('Residual_ABS',ascending = False)[:25]

fig = px.scatter_mapbox(df_results_plot_least,
                        lat='coordinates.latitude',
                        lon='coordinates.longitude',
                        color='Residual',
                        size = 'Residual_ABS',
                        title='Least Accurate Residuals',
                        labels={'residuals': 'Residuals', 'Residual': 'Size'},
                        color_continuous_scale='Turbo',
                        size_max=20,
                        hover_name = df_results_plot_least.index,
                        hover_data={'Residual': True},
                        zoom = 3,
                        mapbox_style='carto-positron')

# Center the map around the US
#fig.update_layout(mapbox_center=dict(lon=-98, lat=39), style="carto-positron")

#fig.show()

#Most Accurate

#Getting 25 most accurate predictions
df_results_plot_most = df_results_plot.sort_values('Residual_ABS', ascending = False)[-25:]

fig = px.scatter_mapbox(df_results_plot_most,
                        lat='coordinates.latitude',
                        lon='coordinates.longitude',
                        color='Residual',
                        size = 'Residual_ABS',
                        title='Most Accurate Predictions',
                        labels={'residuals': 'Residuals', 'Residual': 'Size'},
                        color_continuous_scale='Turbo',
                        size_max=15,
                        hover_name = df_results_plot_most.index,
                        hover_data={'Residual': True},
                        zoom = 3,
                        mapbox_style='carto-positron')


#fig.show()








