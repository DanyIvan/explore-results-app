from flask import Flask, render_template, jsonify, request
import pandas as pd
from flask_cors import CORS, cross_origin
import json
import os
import time
from make_plots import *
 
app = Flask(__name__)
CORS(app)

atm_cols_data = pd.read_csv('data/atm_cols_datacase1_0.3_20210518.csv', compression='gzip')
# species_data = pd.read_csv('data/species_data_case1_0.3_20210518.csv', compression='gzip')
# reactions_data = pd.read_csv('data/reaction_data_case1_0.3_20210518.csv', compression='gzip')
int_rates_data = pd.read_csv('data/integrated_rates_datacase1_0.3_20210518.csv', compression='gzip')

species_list = atm_cols_data.species.unique()
reaction_list = int_rates_data.reaction.unique()

@app.route('/')
def main():
    return render_template('index.html')
 
@app.route("/species",methods=["POST","GET"])
def species(): 
    return render_template('species_choice.html', species_list=species_list)

@app.route("/species/<variable>",methods=["GET"])
def species_var(variable): 
    print(variable)
    species_data = pd.read_csv('data/species_case10.3/' + variable + '.csv',
        compression='gzip')
    atm_cols_file = "static/plots/species_atm_cols_" + variable + ".html"
    mixrat_scatter_file = "static/plots/species_mixrat_file_" + variable + ".html"
    altitude_file = "static/plots/species_altitude_" + variable + ".html"
    for filename in os.listdir('static/plots/'):
        if filename.startswith('species_'):  # not to remove other images
            os.remove('static/plots/' + filename)
    fig1 = plot_flow_O2_vs_atm_cols(atm_cols_data, variable)
    fig2 = plot_flow_O2_vs_mixrat(species_data, variable)
    fig3 = plot_vars_vs_alt_by_flowO2(species_data, variable)
    fig1.write_html(atm_cols_file, full_html=False, include_plotlyjs='cdn', 
        auto_play=False)
    fig2.write_html(mixrat_scatter_file, full_html=False, include_plotlyjs='cdn', 
        auto_play=False)
    fig3.write_html(altitude_file, full_html=False, include_plotlyjs='cdn', 
        auto_play=False)
    print('wrote_html')
    return render_template('species.html', species_list=species_list,
        atm_cols_html='/' + atm_cols_file,
        mixrat_html='/' + mixrat_scatter_file,
        alt_html='/'+altitude_file)

@app.route("/reactions",methods=["POST","GET"])
def reactions(): 
    return render_template('reactions_choice.html', reaction_list=reaction_list)

@app.route("/reactions/<variable>",methods=["GET"])
def reactions_var(variable): 
    print(variable)
    reactions_data = pd.read_csv('data/reaction_data_case10.3/' + variable + '.csv',
        compression='gzip')
    rates_file= "static/plots/reactions_rates_" + variable + ".html"
    integrated_rates_file = "static/plots/reactions_integrated_rates_" + variable + ".html"
    rates_alt_file = "static/plots/reactions_rates_alt_" + variable + ".html"
    for filename in os.listdir('static/plots/'):
        if filename.startswith('reactions_'):  # not to remove other images
            os.remove('static/plots/' + filename)
    reaction = reactions_data.columns[-1]
    fig1 = plot_flow_O2_vs_integrated_rates(int_rates_data, reaction)
    fig2 = plot_flow_O2_vs_rates(reactions_data, reaction)
    fig3 = plot_rates_vs_alt(reactions_data, reaction)
    fig1.write_html(rates_file, full_html=False, include_plotlyjs='cdn', 
        auto_play=False)
    fig2.write_html(integrated_rates_file, full_html=False, include_plotlyjs='cdn', 
        auto_play=False)
    fig3.write_html(rates_alt_file, full_html=False, include_plotlyjs='cdn', 
        auto_play=False)
    print('wrote_html')
    return render_template('reactions.html', reaction_list=reaction_list,
        rates_html='/' + rates_file,
        integrated_rates_html='/' + integrated_rates_file,
        rates_alt_html='/'+rates_alt_file)

     
if __name__ == '__main__':
    app.run(debug=True)