"""CSC110 Fall 2020: prediction

Module Description
==================
This module contains the code to create polynomial and linear
regression models on specific datasets.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Wang, Kevin Wang, Samraj Aneja and Abdus Shaikh.
"""

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import plotly.express as px
import plotly.graph_objects as go

from typing import List

import dataset_processing


def sea_level_prediction(filepath_sea_level: str, filepath_co2: str, co2_input: float,
                         display_graph: bool, years: int) -> List[float]:
    """
    Display a graph of the regression and then return the sea level rise points.
    <co2_input> represents the user-decided total co2 emissions output in metric tons.
    <years> represents the total years the prediction algorithm will run for.
    <display_graph> represents whether the graph should be shown at the end of calculation.

    Preconditions:
        - co2_input >= 1
        - years >= 1
    """
    # mappings from Year (datetime.date) to Value (float)
    sea_level_data = dataset_processing.process_sea_level(filepath_sea_level)
    co2_data = dataset_processing.process_co2(filepath_co2)

    x_list = [co2_data[year] for year in co2_data]
    y_list = [sea_level_data[year] for year in sea_level_data]

    # x_future = x_list + list(range(int(x_list[-1]), int(x_list[-1] + co2_input), 350))
    x_future = list(np.linspace(x_list[-1], x_list[-1] + co2_input, years))

    sea_level_points = regression_points(x_list, y_list, x_future, degree=1)

    if display_graph:
        show_graph(x_list, y_list, x_future, sea_level_points,
                   ['Sea Level Rise vs. CO2 Emissions', 'CO2 Emissions (metric tons)', 'Sea Level (mm)'])

    return sea_level_points


def land_loss_prediction(filepath_land_loss: str, sea_level_rise: float, country_code: str) -> float:
    """
    Return the total land loss percentage.

    Preconditions:
      - country_code is a three-letter ISO3166-1 alpha-3 code representing a country name
    """
    land_loss_data = dataset_processing.process_land_loss(filepath_land_loss)

    x_list = [sea_level for sea_level in range(1, 6)]
    y_list = [land_loss_data[country_code][sea_level - 1] for sea_level in x_list]

    x_future = [sea_level_rise]

    # turn x-values from m to mm to match other graphs
    x_list = [sea_level * 1000 for sea_level in x_list]

    land_loss_points = regression_points(x_list, y_list, x_future, 2)

    # land_loss_points is a list with only 1 point
    # this check is to ensure that due to errors in regression, the land loss is never negative
    if land_loss_points[0] < 0:
        return 0.0
    else:
        return land_loss_points[0]


def pop_displacement_prediction(filepath_pop_displacement: str, sea_level_rise: float, country_code: str) -> float:
    """
    Return the total population displacement percentage.

    Preconditions:
      - country_code is a three-letter ISO3166-1 alpha-3 code representing a country name
    """
    pop_displacement_data = dataset_processing.process_pop_displacement(filepath_pop_displacement)

    x_list = [sea_level for sea_level in range(1, 6)]
    y_list = [pop_displacement_data[country_code][sea_level - 1] for sea_level in x_list]

    x_future = [sea_level_rise]

    # turn x-values from m to mm to match other graphs
    x_list = [sea_level * 1000 for sea_level in x_list]

    pop_displacement_points = regression_points(x_list, y_list, x_future, 2)

    # pop_displacement_points is a list with one point
    # this check is to ensure that due to errors in regression, the population displacement is never negative
    if pop_displacement_points[0] < 0:
        return 0.0
    else:
        return pop_displacement_points[0]


def land_loss_national_stats(filepath_land_loss: str, sea_level_rise: float) -> List[float]:
    """
    Return a list of predicted national land-loss percentages in the same order of countries as in land_loss.csv.
    """
    land_loss_data = dataset_processing.process_land_loss(filepath_land_loss)

    national_land_loss = []
    for country_code in land_loss_data:
        national_land_loss.append(land_loss_prediction(filepath_land_loss, sea_level_rise, country_code))

    return national_land_loss


def pop_displacement_national_stats(filepath_pop_displacement: str, sea_level_rise: float) -> List[float]:
    """
    Return a list of predicted national population displacement percentages in the same
    order of countries as in pop_displacement.csv.
    """
    pop_displacement_data = dataset_processing.process_pop_displacement(filepath_pop_displacement)

    national_pop_displacement = []
    for country_code in pop_displacement_data:
        national_pop_displacement.append(pop_displacement_prediction(filepath_pop_displacement,
                                                                     sea_level_rise, country_code))

    return national_pop_displacement


def regression_points(x_list: List[float], y_list: List[float], x_future: List[float],
                      degree: int) -> List[float]:
    """
    Return a dict of predicted (regressed) y-coordinates.

    Preconditions:
      - degree >= 1
    """
    x = np.array(x_list).reshape((-1, 1))
    y = np.array(y_list)
    x_future = np.array(x_future)

    model = LinearRegression()

    poly_regression = PolynomialFeatures(degree=degree)
    poly_regression.fit(x)

    x_poly = poly_regression.transform(x)

    model.fit(x_poly, y)

    x_prediction = poly_regression.transform(x_future.reshape(-1, 1))
    y_prediction = model.predict(x_prediction)

    return [y_coord for y_coord in y_prediction]


def show_graph(x_existing: List[float], y_existing: List[float],
               x_future: List[float], y_future: List[float],
               graph_titles: List[str]) -> None:
    """
    Show a scatter graph of the given information with a regression line.
    <graph_titles> is a list of strings in the order: [title, x-axis title, y-axis title].

    Preconditions:
      - len(graph_titles) == 3
    """
    fig = px.scatter(x=x_existing, y=y_existing, opacity=0.8)

    fig.add_traces(go.Scatter(x=x_future, y=y_future, name='Regression'))
    fig.update_layout(title=graph_titles[0], xaxis_title=graph_titles[1], yaxis_title=graph_titles[2])

    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['numpy', 'sklearn', 'plotly', 'typing',
                          'dataset_processing'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
