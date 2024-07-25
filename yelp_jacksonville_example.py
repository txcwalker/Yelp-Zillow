from flask import render_template, request, Blueprint
import plotly.express as px
from .yelp_data import df6

#This is the same code as the Tag Graph tool jsut limited to Florida, Jacksonville and 32202/32207
#Date of last edit: 03/08/2024

yelp_jacksonville_example = Blueprint("jacksonville_example", __name__, template_folder = 'templates')

#Route for loading Jacksonville Example page
@yelp_jacksonville_example.route('/YelpData/tag_graph_tool/jacksonville_example', methods = ['GET']) #path name
def show_jacksonville():
    return render_template('yelp_jacksonville_example.html', state = 'FL', city = 'Jacksonville',
                           zip_codes = ['32202','32207']) #file name

#Route for updating the Jacksonville Example graphs
@yelp_jacksonville_example.route('/YelpData/tag_graph_tool/jacksonville_example', methods = ['POST'])
def update_jacksonville_graph():
    form_type = request.form.get("form_type")

    if form_type == 'states':

        #Isolating state to Florida
        df_states_tags_filtered = df6[df6['location.state'] == 'FL']
        #Top ten Tags taken
        df_states_graph_filtered = df_states_tags_filtered.tags.value_counts()[:10]

        #All three graphs are effectively the same, comments left in the top one

        #Creating the bar graph
        fig = px.bar(x=df_states_graph_filtered.index, y=df_states_graph_filtered,
                     labels={'index': 'Tags', 'y': 'Total Count'},
                     title='Most Common Restaurant Tags in Florida',
                     color_discrete_sequence=px.colors.sequential.Viridis, #Creates color scale
                     color=df_states_graph_filtered) #variable to have color scale

        #Customizing the appearance of the bar chart
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text='Most Common Restaurant Tags in Florida',
                          title_x=0.5,  # Center the title
                          xaxis_title='Tags',
                          yaxis_title='Total Count',
                          font=dict(family='Arial, sans-serif', size=12, color='darkgrey'),
                          paper_bgcolor='rgba(0,0,0,0)',  #Transparent background
                          plot_bgcolor='rgba(0,0,0,0)',  #Transparent plot background
                          margin=dict(l=50, r=50, b=50, t=80))  #Adjust margins

        # Render the template with the graph data
        return fig.to_json()

    elif form_type == 'cities':
        # Handle city-specific graph (Jacksonville)
        df_city_tags_filtered = df6[df6['location.city'] == 'Jacksonville']
        df_city_graph_filtered = df_city_tags_filtered.tags.value_counts()[:10]

        fig = px.bar(x=df_city_graph_filtered.index, y=df_city_graph_filtered,
                     labels={'index': 'Tags', 'y': 'Total Count'},
                     title='Most Common Restaurant Tags in Jacksonville',
                     color_discrete_sequence=px.colors.sequential.Viridis,
                     color=df_city_graph_filtered)

        #Customizing the appearance of the bar chart
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text='Most Common Restaurant Tags in Jacksonville',
                          title_x=0.5,  # Center the title
                          xaxis_title='Tags',
                          yaxis_title='Total Count',
                          font=dict(family='Arial, sans-serif', size=12, color='darkgrey'),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=50, r=50, b=50, t=80))

        #Render the template with the graph data
        return fig.to_json()

    else:
        #Handle zip code-specific graph (32202 and 32207)
        df_zip_codes_tags_filtered = df6[df6['location.zip_code'].isin(['32202', '32207'])]
        df_zip_codes_graph_filtered = df_zip_codes_tags_filtered.tags.value_counts()[:10]

        fig = px.bar(x=df_zip_codes_graph_filtered.index, y=df_zip_codes_graph_filtered,
                     labels={'index': 'Tags', 'y': 'Total Count'},
                     title='Most Common Restaurant Tags in Zip Codes: 32202, 32207',
                     color_discrete_sequence=px.colors.sequential.Viridis,
                     color=df_zip_codes_graph_filtered)

        # Customizing the appearance of the bar chart
        fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text=f'Most Common Restaurant Tags in Zip Codes: 32202, 32207',
                          title_x=0.5,  # Center the title
                          xaxis_title='Tags',
                          yaxis_title='Total Count',
                          font=dict(family='Arial, sans-serif', size=12, color='darkgrey'),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=50, r=50, b=50, t=80))

        #Render the template with the graph data
        return fig.to_json()

