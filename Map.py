"""CSC110 Fall 2020: Map

Module Description
==================
This module contains the code to create and display the 3D world maps that show how
much land is lost or how much population is displaced for each respective country

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Wang, Kevin Wang, Samraj Aneja and Abdus Shaikh.
"""


import plotly.graph_objects as go
import pandas as pd
from typing import List


def display_map(points: List[float], title: str, filepath: str) -> None:
    """
    Function to display a 3d world map that shows how much land is lost or how much population is displayed
    for each respective country

    Preconditions:
        - len(points) != 0
    """
    df = pd.read_csv(filepath)
    df['POINTS'] = points
    fig = go.Figure(data=go.Choropleth(
        locations=df['CODE'],
        z=df['POINTS'],
        text=df['COUNTRY'],
        colorscale='Reds',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_ticksuffix='%',
        colorbar_title='Percentage of<br>' + title,
    ))

    fig.update_layout(
        title_text='% Of ' + title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='orthographic'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='#',
            showarrow=False
        )]
    )

    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['plotly', 'pandas', 'typing'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
