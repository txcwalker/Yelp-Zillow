import plotly.express as px
from flask import render_template, Blueprint
from .zillow import df_results_plot
import plotly.io as pio

#File which is effectively end of zillow.py, this allows the maps to be plotted showing the models performance, its
#biggest misses and successes
#Date of last edit: 03/08/2024

zillow_analysis = Blueprint("zillow_analysis", __name__, template_folder='templates', static_folder = 'static/images')

@zillow_analysis.route('/YelpData/housing_price_prediction', methods=['GET'])
def show_zillow_analysis():

    #Figure for overall performance
    fig_residuals = px.scatter_mapbox(df_results_plot,
                                      lat='coordinates.latitude',
                                      lon='coordinates.longitude',
                                      color='Residual',
                                      size='Residual_ABS',
                                      title='All Predictions',
                                      labels={'residuals': 'Residuals', 'Residual': 'Size'},
                                      color_continuous_scale='Turbo',
                                      size_max=20,
                                      hover_name=df_results_plot.index,
                                      hover_data={'Residual': True},
                                      zoom=2,
                                      mapbox_style='carto-positron')

    residuals_json = pio.to_json(fig_residuals)

    # Least Accurate

    #Getting 25 least accurate predictions
    df_results_plot_least = df_results_plot.sort_values('Residual_ABS', ascending=False)[:25]

    fig_least_accurate = px.scatter_mapbox(df_results_plot_least,
                                           lat='coordinates.latitude',
                                           lon='coordinates.longitude',
                                           color='Residual',
                                           size='Residual_ABS',
                                           title='Least Accurate Residuals',
                                           labels={'residuals': 'Residuals', 'Residual': 'Size'},
                                           color_continuous_scale='Turbo',
                                           size_max=20,
                                           hover_name=df_results_plot_least.index,
                                           hover_data={'Residual': True},
                                           zoom=2,
                                           mapbox_style='carto-positron')

    least_accurate_json = pio.to_json(fig_least_accurate)

    #Getting 25 most accurate predictions
    df_results_plot_most = df_results_plot.sort_values('Residual_ABS', ascending=False)[-25:]

    fig_most_accurate = px.scatter_mapbox(df_results_plot_most,
                                          lat='coordinates.latitude',
                                          lon='coordinates.longitude',
                                          color='Residual',
                                          size='Residual_ABS',
                                          title='Most Accurate Predictions',
                                          labels={'residuals': 'Residuals', 'Residual': 'Size'},
                                          color_continuous_scale='Turbo',
                                          size_max=15,
                                          hover_name = df_results_plot_most.index,
                                          hover_data={'Residual': True},
                                          zoom=2,
                                          mapbox_style='carto-positron')

    most_accurate_json = pio.to_json(fig_most_accurate)

    return render_template('zillow_analysis.html', residuals_json=residuals_json, least_accurate_json =
                            least_accurate_json, most_accurate_json = most_accurate_json)


