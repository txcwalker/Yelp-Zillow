from flask import Flask, render_template, Blueprint

#Python code for the YelpData home page on wholisticreview.com
#Nothing requiring python is on this page for now
#Date of last edit 03/08/2024

yelp_data_home = Blueprint("yelp_data_home", __name__, template_folder = 'templates')

@yelp_data_home.route('/YelpData')
def show_yelp_data():
    return render_template('yelp_data_home.html')