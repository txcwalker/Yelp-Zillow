from flask import Flask, render_template, Blueprint, request, jsonify
from .yelp_search_score import df_top_search

#python code to display the top ten restaurants based on yelp search score of any zip code
#Date of last edit: 03/08/2024

yelp_search_score_report = Blueprint("yelp_search_score", __name__, template_folder='templates')

#Route to show search score page
@yelp_search_score_report.route('/YelpData/search_score', methods=['GET'])
def show_search_score():
    zip_codes = df_top_search['location.zip_code'].sort_values().unique()
    return render_template('yelp_search_score.html', zip_codes=zip_codes)

#Route to load the search score table
@yelp_search_score_report.route('/YelpData/search_score', methods=['POST'])
def search_score_table():

    #Zip codes sorted numerically to load the dropdown menu
    zip_codes = df_top_search['location.zip_code'].sort_values().unique()

    #selected zip code
    search_target = request.form.getlist('target_zip_code')

    #If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        selected_columns = ['name', 'rating', 'review_count', 'search_score']
        data = df_top_search[df_top_search['location.zip_code'].isin(search_target)][selected_columns][:10].to_dict(orient='records')
        return jsonify(data=data)

    #If it's a regular form submission, render the template
    selected_columns = ['name', 'rating', 'review_count', 'search_score']
    data = df_top_search[df_top_search['location.zip_code'].isin(search_target)][selected_columns][:10]
    return render_template('yelp_search_score.html', data=data, zip_codes=zip_codes)







