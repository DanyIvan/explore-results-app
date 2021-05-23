import os
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.colors as colors
from pathlib import Path

def plot_flow_O2_vs_mixrat(data, species):
    data = data.iloc[0:-1:4]
    data = data.astype({'temp_lb': str})
    ncolors = len(data.temp_lb.unique())
    palette = sns.color_palette("coolwarm", ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(data[species].min(), 1e-50)
    fig = px.scatter(data_frame=data, x='flow_O2', y=species,
                     symbol='converged', color='temp_lb', log_y=True, 
                     range_x=[2e10, 4e13],
                     range_y=[range_y_min, data[species].max()],
                     log_x=True, labels={
                         'flow_O2': 'Ground level O2 flux [pu]',
                         species: 'Mixig Ratio at LB',
                         'temp_lb': 'Temp [K]',
                         'converged': 'Converged',
                         'ALT': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame='ALT',
                    title=species)
    fig.layout.xaxis.tickformat = '.2e'
    fig.layout.yaxis.tickformat = '.2e'
    return fig

def plot_flow_O2_vs_atm_cols(data, species):
    species_data = data[data.species == species]
    species_data = species_data.astype({'temp_lb': str})
    ncolors = len(species_data.temp_lb.unique())
    palette = sns.color_palette("coolwarm", ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(species_data.atm_columns.min(), 1e-50)
    fig = px.scatter(data_frame=species_data, x='flow_O2', y='atm_columns',
                     symbol='converged', color='temp_lb', log_y=True,
                     range_x=[2e10, 4e13],
                     range_y=[range_y_min, species_data.atm_columns.max()],
                     log_x=True, labels={
                         'flow_O2': 'Ground level O2 flux [pu]',
                         'atm_columns': 'Atmospheric column [molecules /cm^2]',
                         'temp_lb': 'Temp [k]',
                         'converged': 'Converged',
                         'ALT': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    title=species_data['species'].values[0])
    fig.layout.xaxis.tickformat = '.2e'
    fig.layout.yaxis.tickformat = '.2e'
    return fig

def plot_vars_vs_alt_by_flowO2(data, species):
    data = data.iloc[0:-1:2]
    temps = data.temp_lb.unique()
    group_by_count = data[data.ALT == 0.25].groupby('flow_O2').sum()
    fluxes = group_by_count[group_by_count.temp_lb == temps.sum()].index
    idxs = np.round(np.linspace(0, len(fluxes) - 1, 50)).\
            astype(int)
    fluxes = fluxes[idxs]
    data = data[data.flow_O2.isin(fluxes)]
    data = data.astype({'temp_lb': str})
    data.flow_O2 = data.flow_O2.apply(lambda col: '{:.2E}'.format(col))
    ncolors = len(temps)
    palette = sns.color_palette("coolwarm", ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_x_min = max(data[species].min(), 1e-30)
    fig = px.line(data_frame=data, x=species, y='ALT', color='temp_lb', 
                     range_x = [range_x_min, data[species].max()],
                     range_y = [0, 81],
                     log_x=True, labels={
                         'flow_O2': r'Ground level O2 flux [pu]',
                         species: 'Mixig Ratio at LB',
                         'temp_lb': 'Temp [k]',
                         'converged': 'Converged',
                         'ALT': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame='flow_O2',
                    title=species)
    fig.layout.xaxis.tickformat = '.2e'
    return fig

        
def plot_flow_O2_vs_rates(data, reaction):
    data = data.iloc[0:-1:4]
    data = data.astype({'temp_lb': str})
    ncolors = len(data.temp_lb.unique())
    palette = sns.color_palette("coolwarm", ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(data[reaction].min(), 1e-50)
    fig = px.scatter(data_frame=data, x='flow_O2', y=reaction,
                     symbol='converged', color='temp_lb', log_y=True, 
                     range_x=[2e10, 4e13],
                     range_y=[range_y_min, data[reaction].max()],
                     log_x=True, labels={
                         'flow_O2': 'Ground level O2 flux [pu]',
                         reaction: 'Reaction rate [molecules/cm^3 s]',
                         'temp_lb': 'Temp [K]',
                         'converged': 'Converged',
                         'ALT': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame='ALT',
                    title=reaction)
    fig.layout.xaxis.tickformat = '.2e'
    fig.layout.yaxis.tickformat = '.2e'
    return fig

def plot_flow_O2_vs_integrated_rates(data, reaction):
    reaction_data = data[data.reaction == reaction]
    reaction_data = reaction_data.astype({'temp_lb': str})
    ncolors = len(reaction_data.temp_lb.unique())
    palette = sns.color_palette("coolwarm", ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(reaction_data.integrated_rates.min(), 1e-50)
    fig = px.scatter(data_frame=reaction_data, x='flow_O2', y='integrated_rates',
                     symbol='converged', color='temp_lb', log_y=True, 
                     range_x=[2e10, 4e13],
                     range_y=[range_y_min, reaction_data.integrated_rates.max()],
                     log_x=True, labels={
                         'flow_O2': 'Ground level O2 flux [pu]',
                         'integrated_rates': 'Integrated reaction rate [molecules / cm^2 s]',
                         'temp_lb': 'Temp [K]',
                         'converged': 'Converged',
                         'ALT': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    title=reaction)
    fig.layout.xaxis.tickformat = '.2e'
    fig.layout.yaxis.tickformat = '.2e'
    return fig

def plot_rates_vs_alt(data, reaction):
    # find fluxes that all temperatures have and only use 90 of them
    data = data.iloc[0:-1:2]
    temps = data.temp_lb.unique()
    group_by_count = data[data.ALT == 1].groupby('flow_O2').sum()
    fluxes = group_by_count[group_by_count.temp_lb == temps.sum()].index
    idxs = np.round(np.linspace(0, len(fluxes) - 1, 50)).\
            astype(int)
    fluxes = fluxes[idxs]
    data = data[data.flow_O2.isin(fluxes)]
    data = data.astype({'temp_lb': str})
    data.flow_O2 = data.flow_O2.apply(lambda col: '{:.2E}'.format(col))
    ncolors = len(temps)
    palette = sns.color_palette("coolwarm", ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_x_min = max(data[reaction].min(), 1e-30)
    range_x_min = max(data[reaction].min(), 1e-30)
    fig = px.line(data_frame=data, x=reaction, y='ALT', color='temp_lb', 
                     range_x = [range_x_min, data[reaction].max()],
                     range_y = [0, 81],
                     log_x=True, labels={
                         'flow_O2': 'Ground level O2 flux [pu]',
                         reaction: 'Reaction rate [molecules / cm^3 s]',
                         'temp_lb': 'Temp [k]',
                         'converged': 'Converged',
                         'ALT': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame='flow_O2',
                    title=reaction)
    fig.layout.xaxis.tickformat = '.2e'
    return fig


def make_reactions_plots(reaction_data, integrated_rates_data, folder):
    folder_flow_O2_vs_rates = os.path.join(folder, 'flow_O2_vs_rates', '')
    folder_flow_O2_vs_integrated_rates = os.path.join(folder, 'flow_O2_vs_integrated_rates', '')
    folder_rates_vs_alt = os.path.join(folder, 'rates_vs_alt', '')
    Path(folder).mkdir(exist_ok=True)
    Path(folder_flow_O2_vs_rates).mkdir(exist_ok=True)
    Path(folder_flow_O2_vs_integrated_rates).mkdir(exist_ok=True)
    Path(folder_rates_vs_alt).mkdir(exist_ok=True)
    for reaction in integrated_rates_data.reaction.unique():
        print(reaction)
        fig1 = plot_flow_O2_vs_rates(reaction_data, reaction)
        fig2 = plot_flow_O2_vs_integrated_rates(integrated_rates_data, reaction)
        fig3 = plot_rates_vs_alt(reaction_data, reaction)
        reaction = reaction.replace(' ', '')
        fig1.write_html(folder_flow_O2_vs_rates + reaction + '.html', 
            full_html=False, include_plotlyjs='cdn', auto_play=False)
        fig2.write_html(folder_flow_O2_vs_integrated_rates + reaction + '.html', 
            full_html=False, include_plotlyjs='cdn')
        fig3.write_html(folder_rates_vs_alt + reaction + '.html', 
            full_html=False, include_plotlyjs='cdn', auto_play=False)
        
def make_species_plots(species_data, atm_cols_data, folder):
    folder_flow_O2_vs_mixrat = os.path.join(folder, 'flow_O2_vs_mixrat', '')
    folder_flow_O2_vs_atm_cols = os.path.join(folder, 'flow_O2_vs_atm_cols', '')
    folder_vars_vs_alt_by_flowO2 = os.path.join(folder, 'vars_vs_alt_by_flowO2', '')
    Path(folder).mkdir(exist_ok=True)
    Path(folder_flow_O2_vs_mixrat).mkdir(exist_ok=True)
    Path(folder_flow_O2_vs_atm_cols).mkdir(exist_ok=True)
    Path(folder_vars_vs_alt_by_flowO2).mkdir(exist_ok=True)
    for species in atm_cols_data.species.unique():
        print(species)
        fig1 = plot_flow_O2_vs_mixrat(species_data, species)
        fig2 = plot_flow_O2_vs_atm_cols(atm_cols_data, species)
        fig3 = plot_vars_vs_alt_by_flowO2(species_data, species)
        fig1.write_html(folder_flow_O2_vs_mixrat + species + '.html', 
            full_html=False, include_plotlyjs='cdn', auto_play=False)
        fig2.write_html(folder_flow_O2_vs_atm_cols + species + '.html', 
            full_html=False, include_plotlyjs='cdn')
        fig3.write_html(folder_vars_vs_alt_by_flowO2 + species + '.html', 
            full_html=False, include_plotlyjs='cdn', auto_play=False)

def split_species_data(species_data, folder):
    Path(folder).mkdir(exist_ok=True)
    not_species = ['PRESS', 'TEMP', 'ALT', 'EDD', 'DEN', 'H2OSAT', 'RELH', 
        'CONDEN', 'FLUX', 'converged', 'flow_O2', 'temp_lb', 'idx']
    species = [x for x in species_data.columns if x not in not_species]
    for s in species:
        print(s)
        new_data = species_data[['ALT', 'temp_lb', 'converged',
            'flow_O2', s]]
        path = os.path.join(folder, s) + '.csv'
        new_data.to_csv(path, index=False, compression='gzip')

def split_reaction_data(reaction_data, folder):
    Path(folder).mkdir(exist_ok=True)
    not_reaction = ['TEMP', 'ALT','converged', 'flow_O2', 'temp_lb', 'idx']
    reactions = [x for x in reaction_data.columns if x not in not_reaction]
    for r in reactions:
        print(r)
        new_data = reaction_data[['ALT', 'temp_lb', 'converged',
            'flow_O2', r]]
        path = os.path.join(folder, r.replace(' ', '')) + '.csv'
        new_data.to_csv(path, index=False, compression='gzip')

