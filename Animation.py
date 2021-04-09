"""CSC110 Fall 2020: Animation

Module Description
==================
This module contains the code to create and display the animated bar
graph shown when the start button is clicked in the main program.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Wang, Kevin Wang, Samraj Aneja and Abdus Shaikh.
"""


import plotly.express as px
import pandas as pd
import datetime
from typing import List


def display_animated_graph(sea_level_points: List[float]) -> None:
    """"
    Function to display an animated bar graph to represent the rising sea level

    Preconditions:
        - len(sea_level_points) > 0
    """

    total_years = [datetime.date(2013, 1, 1).year + (1 + i) for i in range(0, len(sea_level_points))]
    location = ['World'] * len(sea_level_points)
    data_dict = {"Location": location, "Year": total_years, "Sea Level (mm)": sea_level_points}
    df = pd.DataFrame(data_dict)
    fig = px.bar(df, x='Location', y='Sea Level (mm)', color='Location',
                 animation_frame='Year', animation_group='Location', range_y=[0, max(sea_level_points)])
    fig.show()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['plotly.express', 'pandas', 'datetime', 'typing'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
