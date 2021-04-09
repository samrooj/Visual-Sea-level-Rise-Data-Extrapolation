"""
Copyright Info
"""

from typing import Dict, List

import csv
import datetime


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
    Return a mapping from a year to that year's total co2 emissions.
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


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'numpy', 'plotly', 'sklearn',
                          'Animation', 'GUI', 'prediction', 'Map'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
