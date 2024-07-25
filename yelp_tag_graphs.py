import seaborn as sns
import matplotlib.pyplot as plt
from  .yelp_data import df6

#Code set up to review top x tags in any city, state or zip code (multiple selections are possible)
#Date of last edit: 03/08/2024

#Jacksonville Zip Codes
target_zipcodes = ['32202', '32207'] #These can be changed to fit the situation

#Top x tags in target zip code(s)
df_zipcode_tags = df6[df6['location.zip_code'].isin(target_zipcodes)]
df_zipcode_graph = df_zipcode_tags.tags.value_counts()[:20]

#Set the style of the plot
sns.set(style="whitegrid")

#Create a bar plot using Seaborn
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
ax = sns.barplot(x=df_zipcode_graph.index, y=df_zipcode_graph,palette='husl')

#Rotate x-axis labels for better readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

#Set labels and title
target_zipcodes_str = ', '.join(target_zipcodes)
plt.xlabel('Tags')
plt.ylabel('Total Count')
plt.title(f'Most Common Restaurant Tags in Zip Codes: {target_zipcodes_str}')

#Show the plot
#plt.show() #muting the output

#Cities
target_cities =['Jacksonville'] #These can be changed to fit the situation
unique_cities = df6['location.city'].unique()


#top x city tags
df_cities_tags = df6[df6['location.city'].isin(target_cities)]
df_cities_graph = df_cities_tags.tags.value_counts()[:20]

#Set the style of the plot
sns.set(style="whitegrid")

#Create a bar plot using Seaborn
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
ax = sns.barplot(x=df_cities_graph.index, y=df_cities_graph, palette='husl')

#Rotate x-axis labels for better readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

#Set labels and title
target_cities_str = ', '.join(target_cities)
plt.xlabel('Tags')
plt.ylabel('Total Count')
plt.title(f'Most Common Restaurant Tags in Cities: {target_cities_str}')

#Show the plot
#plt.show() #muting the output

#State
target_states = ['FL'] #These can be changed to fit the situation, use state abbreviations

#Top x State values
df_states_tags = df6[df6['location.state'].isin(target_states)]
df_states_graph = df_states_tags.tags.value_counts()[:20]

#Set the style of the graph
sns.set(style="whitegrid")

#Create a bar graph
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
ax = sns.barplot(x=df_states_graph.index, y=df_states_graph, palette='husl')

#Rotate x-axis labels for better readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

#Set labels and title
target_states_str = ', '.join(target_states)
plt.xlabel('Tags')
plt.ylabel('Total Count')
plt.title(f'Most Common Restaurant Tags in: {target_states_str}')

#Show the plot
#plt.show() #muting the output

