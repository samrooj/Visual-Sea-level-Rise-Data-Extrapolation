"""
Copyright Information
"""

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import plotly.express as px
import plotly.graph_objects as go

import csv
import datetime
from typing import Dict, List


# TODO: IMPORTANT SIDE NOTE: the user-inputted carbon emissions are BY YEAR, so to get the total co2, you need
# TODO: multiply years * co2 per year


def str_to_date_sea_level(date_string: str) -> datetime.date:
    """Convert a string in yyyy-mm-dd format to a datetime.date.

    >>> str_to_date_sea_level('2002-02-01')
    datetime.date(year=2002, month=2, day=1)
    """

    split_date = str.split(date_string, '-')
    year = int(split_date[0])
    month = int(split_date[1])
    day = int(split_date[2])

    date = datetime.date(year=year, month=month, day=day)

    return date


def process_sea_level(filepath: str) -> Dict[datetime.date, float]:
    """Transform the dataset into a usable format.

    Return a mapping with the keys being the year, and the value being the Global Mean Sea Level
    of that year.

    filepath is 'csiro_recons_gmsl_yr_2015_csv.csv', if the dataset is in the root folder
    (Same as this py file)

    Preconditions:
    - All dates in the dataset specified by filepath are unique
    """

    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)
        mapping = {}
        for row in reader:
            # row[0] = date as str
            # row[1] = Global Mean Sea Level (mm) as str
            # row[2] = GMSL Uncertainty as str
            str_date = row[0]
            date = str_to_date_sea_level(str_date)
            if 1751 <= date.year <= 2013:
                sea_level = float(row[1])
                mapping[str_to_date_sea_level(str_date)] = sea_level

    return mapping


def process_co2(filepath: str) -> Dict[datetime.date, float]:
    """
    'Project Datasets/annual-co2-emissions-per-country_1.csv'
    """
    dataset_dict = {}

    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            date = datetime.date(int(row[2][0:4]), 1, 1)
            if 1880 <= date.year <= 2013:
                dataset_dict[date] = float(row[3])

    return dataset_dict


def process_land_loss(filepath: str) -> Dict[str, List[float]]:
    """
    'Project Datasets/land_loss.csv'
    Return a mapping from country code to list of land loss percentages from [1m, 2m, ..., 5m] of sea rise.
    """
    dataset_dict = {}
    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            country_code = row[0]
            percent_land_lost = [float(row[i]) for i in range(2, 7)]
            dataset_dict[country_code] = percent_land_lost

    return dataset_dict


def process_pop_displacement(filepath: str) -> Dict[str, List[float]]:
    """
    'Project Datasets/pop_displacement.csv'
    Return a mapping from country code to list of population displacement from [1m, 2m, ..., 5m] of sea rise.
    """
    dataset_dict = {}
    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            country_code = row[0]
            percent_pop_displacement = [float(row[i]) for i in range(2, 7)]
            dataset_dict[country_code] = percent_pop_displacement

    return dataset_dict


def sea_level_prediction(filepath_sea_level: str, filepath_co2: str, co2_input: float) -> List[float]:
    """
    SL path: 'Project Datasets/csiro_recons_gmsl_yr_2015_csv.csv'
    CO2 path: 'Project Datasets/annual-co2-emissions-per-country_1.csv'
    Display a graph of the regression and then return the sea level rise points.
    co2_input represents the user-decided total co2 emissions output in metric tons.

    Preconditions:
        - co2_input >= 1
    """
    # mappings from Year (datetime.date) to Value (float)
    sea_level_data = process_sea_level(filepath_sea_level)
    co2_data = process_co2(filepath_co2)

    x_list = [co2_data[year] for year in co2_data]
    y_list = [sea_level_data[year] for year in sea_level_data]

    x_future = x_list + list(range(int(x_list[-1]), int(x_list[-1] + co2_input), 350))

    sea_level_points = regression_points(x_list, y_list, x_future, 3)

    show_graph(x_list, y_list, x_future, sea_level_points,
               ['Sea Level Rise vs. CO2 Emissions', 'CO2 Emissions (metric tons)',
                'Sea Level (mm)'])

    return sea_level_points


def land_loss_prediction(filepath_land_loss: str, sea_level_rise: float, country_code: str) -> float:
    """
    land_loss path: 'Project Datasets/land_loss.csv'
    Return the total land loss percentage.
    """
    # TODO: shift the data processing OUTSIDE the function to reduce overhead
    land_loss_data = process_land_loss(filepath_land_loss)

    x_list = [sea_level for sea_level in range(1, 6)]
    y_list = [land_loss_data[country_code][sea_level - 1] for sea_level in x_list]

    x_future = [sea_level_rise]

    # turn x-values from m to mm to match other graphs
    x_list = [sea_level * 1000 for sea_level in x_list]

    land_loss_points = regression_points(x_list, y_list, x_future, 2)

    # TODO: REMOVE
    # show_graph(x_list, y_list, x_future, land_loss_points,
    #            ['Land Loss vs. Sea Level Rise', 'Sea Level Rise (mm)', 'Land Loss (sq. km)'])

    # land_loss_points is a list with only 1 point
    # this check is to ensure that due to errors in regression, the land loss is never negative
    if land_loss_points[0] < 0:
        return 0.0
    else:
        return land_loss_points[0]


def pop_displacement_prediction(filepath_pop_displacement: str, sea_level_rise: float, country_code: str) -> float:
    """
    pop_displacement path: 'Project Datasets/slr-impacts_nov2010-_1_.csv'
    Return the total population displacement percentage.
    """
    # TODO: shift the data processing OUTSIDE the function to reduce overhead
    pop_displacement_data = process_pop_displacement(filepath_pop_displacement)

    x_list = [sea_level for sea_level in range(1, 6)]
    y_list = [pop_displacement_data[country_code][sea_level - 1] for sea_level in x_list]

    x_future = [sea_level_rise]

    # turn x-values from m to mm to match other graphs
    x_list = [sea_level * 1000 for sea_level in x_list]

    pop_displacement_points = regression_points(x_list, y_list, x_future, 2)

    # TODO: REMOVE
    # show_graph(x_list, y_list, x_future, pop_displacement_points,
    #            ['Population Displacement vs. Sea Level Rise', 'Sea Level Rise (mm)',
    #             'Population Displacement'])

    # pop_displacement_points is a list with one point
    # this check is to ensure that due to errors in regression, the population displacement is never negative
    if pop_displacement_points[0] < 0:
        return 0.0
    else:
        return pop_displacement_points[0]


def land_loss_national_stats(filepath_land_loss: str, sea_level_rise: float) -> List[float]:
    """
    Return a list of predicted national land-loss percentages in the same order of countries as in land_loss.csv.
    sea_level_rise should be done by doing (sea_level_prediction()[-1] - sea_level_prediction()[0])
    land_loss path: 'Project Datasets/land_loss.csv'
    """
    # TODO: shift the data processing OUTSIDE the function to reduce overhead
    land_loss_data = process_land_loss(filepath_land_loss)

    national_land_loss = []
    for country_code in land_loss_data:
        national_land_loss.append(land_loss_prediction(filepath_land_loss, sea_level_rise, country_code))

    return national_land_loss


def pop_displacement_national_stats(filepath_pop_displacement: str, sea_level_rise: float) -> List[float]:
    """
    Return a list of predicted national population displacement percentages in the same
    order of countries as in pop_displacement.csv.
    sea_level_rise should be done by doing (sea_level_prediction()[-1] - sea_level_prediction()[0])
    pop_displacement path: 'Project Datasets/slr-impacts_nov2010-_1_.csv'
    """
    # TODO: shift the data processing OUTSIDE the function to reduce overhead
    pop_displacement_data = process_land_loss(filepath_pop_displacement)

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
    """
    fig = px.scatter(x=x_existing, y=y_existing, opacity=0.8)

    fig.add_traces(go.Scatter(x=x_future, y=y_future, name='Regression'))
    fig.update_layout(title=graph_titles[0], xaxis_title=graph_titles[1], yaxis_title=graph_titles[2])

    fig.show()
