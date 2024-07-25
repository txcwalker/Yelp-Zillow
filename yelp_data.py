#General Data cleaning for the Yelp Data
#Date of last edit:03/07/2024

#Import statements
import pandas as pd
import seaborn as sns
#Imported for apache/ubuntu otherwise data files could not be read in properly on the live site
import os
#imported to handle the non ascii characters - this was something that was only needed on the live site and a problem
#brought up by ubuntu/apache
import unicodedata


#Columns names for df5 (df used in all analysis)
new_column_names = column_names = [
    'id',
    'name',
    'url',
    'review_count',
    'rating',
    'transactions',
    'price',
    'distance',
    'coordinates.latitude',
    'coordinates.longitude',
    'location.address1',
    'location.city',
    'location.zip_code',
    'location.country',
    'location.state',
    'location.display_address',
    'all_categories'
]

#Approved states list used to cut any observations not in the US, CA or MX
approved_states = approved_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
                   'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
                   'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
                   'AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT',  # Canadian provinces and territories
                   'AGU', 'BCS', 'BCN', 'CAM', 'CHH', 'COA', 'COL', 'DIF', 'DUR', 'GRO', 'GUA', 'HID', 'JAL', 'MEX', 'MIC',
                   'MOR', 'NAY', 'NLE', 'OAX', 'PUE', 'QUE', 'ROO', 'SLP', 'SIN', 'SON', 'TAB', 'TAM', 'TLA', 'VER', 'YUC',
                   'ZAC',  # Mexican states
                   'AS', 'GU', 'MP', 'PR', 'VI']  # US overseas territories




#Reading in the data_file, using this method for Apache/ubunutu
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'data', 'yelp_cities_food_restaurant.csv')
df5 = pd.read_csv(data_path, header=None, names=new_column_names, encoding = 'utf-8')

#Replacing non ascii characters
def replace_non_ascii_in_object_columns(df):
    for column in df.select_dtypes(include='object').columns:
        df[column] = df[column].apply(replace_non_ascii)

def replace_non_ascii(cell):
    return ''.join(char if ord(char) < 128 else unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('utf-8') for char in str(cell))

# Example usage:
# Assuming df is your DataFrame
replace_non_ascii_in_object_columns(df5)

#Making sure only states from the approved states list are in the final df. Do not need states from Argentina, Malysia, etc etc
df5 = df5[df5['location.state'].isin(approved_states)]


#Dropping duplicate rows and any row that does not have at least 5 reviews
df5 = df5.drop_duplicates()
df5 = df5[df5['review_count'] >= 5]

#Setting all city names to have first letter capital and others lowercase
df5['location.city'] = df5['location.city'].str.title()

#Strips the extra space (before and after) the cities and states
df5[['location.state','location.city']] = df5[['location.state','location.city']].apply(lambda x: x.strip() if isinstance(x, str) else x)

df5[['location.city', 'location.state']] = df5[['location.city', 'location.state']].apply(lambda x: x.str.strip().str.replace(r'\s+', ' ', regex=True))

#Converting "$" to numerical variable
#Creating Dictionary Dollar to Numbers
money_dict = {'$': 1,'$$': 2,'$$$': 3,'$$$$': 4}

df5['price'] = df5['price'].map(money_dict)

# Tag Extraction
##Function to convert the object to a list to utilize pd.explode
# Increase the size of the df by 2.5x , not ideal but best way I found/know
def str_to_list(cell):
    if isinstance(cell, float):
        #If the cell is a float (NaN), return an empty list
        return []

    #Remove characters '[]' and split by ', '
    cell = ''.join(c for c in cell if c not in "'[]")
    cell = cell.split(', ')
    return cell


#Apply the function to the 'all_categories' column
df5['tags'] = df5['all_categories'].apply(str_to_list)


#df6 is the df used for looking at all things tags
df6 = df5.explode('tags')
total_tags = df6.tags.value_counts()

#Bar Graph of the top X Tags
data_tags_graph = total_tags[:25]
df_tags_graph = pd.DataFrame(data_tags_graph)

#Set the style of the plot
sns.set(style="whitegrid")

#Renaming Count to avoid any confusion with preset variables and for loops
df_tags_graph = df_tags_graph.rename(columns={'count': 'total'})

# Ensure there are no leading or trailing whitespaces in the column name
df_tags_graph.columns = df_tags_graph.columns.str.strip()



"""#Create a bar plot using Seaborn
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
# Plot the bar graph
total_tags_graph = sns.barplot(x=df_tags_graph.index, y=df_tags_graph['total'], data=df_tags_graph, palette='viridis')
#Rotate x-axis labels for better readability
total_tags_graph.set_xticklabels(total_tags_graph.get_xticklabels(), rotation=45, ha='right')
#Set labels and title
plt.xlabel('Tags')
plt.ylabel('Total Count')
plt.title('Most Common Restaurant Tags')"""

#Show the plot
#plt.show() #muting the output

#This is muted because it is not needed for now
#Sorting by zip code, city and state and creating some metrics to review/compare
#Sorting by ZipCode
#df5.groupby('location.zip_code').mean()[['review_count','rating','price']]
#df5.groupby('location.zip_code').sum()['review_count']
#df5.groupby('location.zip_code').median()[['review_count','rating','price']]

#Sorting by City
#df5.groupby('location.city').mean()[['review_count','rating','price']]
#df5.groupby('location.city').sum()['review_count']
#df5.groupby('location.city').median()[['review_count','rating','price']]

#Sorting by State
#df5.groupby('location.state').mean()[['review_count','rating','price']]
#df5.groupby('location.state').sum()['review_count']
#df5.groupby('location.state').median()[['review_count','rating','price']]

#Fillna with Average for Zip Code for price. Its not great for either but it is better than a bunch of missing data

#Fill NaN in 'price' with the average 'price' based on 'location.zip_code'
df5['price'] = df5.groupby('location.zip_code')['price'].transform(lambda x: x.fillna(x.mean()))
df7 = df5.dropna()

"""#Fill NaN in 'rating' with the average 'rating' based on 'location.zip_code'
df5['rating'] = df5.groupby('location.zip_code')['rating'].transform(lambda x: x.fillna(x.mean()))
df7 = df5.dropna()"""





