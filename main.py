"""CSC110 Fall 2020: Final Project Submission

Module Description
==================
This module contains the culmination of all other modules of the project.
Running this module allows the user to make use of the system weve developed
to analayze, extrapolate and display the data for our chosen question.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
involved with CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Jason Wang, Kevin Wang, Samraj Aneja and Abdus Shaikh.
"""
from tkinter import Label, Button, Entry, Tk
import animation
import maps
import prediction


PATH_SEA_LEVEL = 'Project Datasets/csiro_recons_gmsl_yr_2015_csv.csv'
PATH_CO2 = 'Project Datasets/annual-co2-emissions-per-country_1.csv'
PATH_LAND_LOSS = 'Project Datasets/land_loss.csv'
PATH_POP_DISPLACEMENT = 'Project Datasets/pop_displacement.csv'
PATH_COUNTRY_TO_CODE = 'Project Datasets/Country_to_Code.csv'


window = Tk()
window.geometry("360x300")
error_message = Label(window, text="Invalid Input")


# Functions for Buttons
def start_function() -> None:
    """
    This function corresponds to the first start button that appears to the user that will output
    the sea level rise interactive animated graph. On the call of this function, we will also show
    the rest of the options to the user including the land loss map and the population displaced.
    Function notifies user for invalid inputs.
    """
    year_input = int(year.get())
    co2_input = float(co2.get())
    total_co2 = (year_input - 2013) * co2_input
    if year_input <= 2013 or co2_input < 1:
        error_message.grid(row=5, column=0, columnspan=2)
        second_instructions.grid_forget()
        land_loss_prompt.grid_forget()
        land_loss_button.grid_forget()
        pop_displaced_prompt.grid_forget()
        pop_displaced_button.grid_forget()

    else:
        error_message.grid_forget()

        # displays a graph and animation of sea-level rise
        sea_level_points = prediction.sea_level_prediction(PATH_SEA_LEVEL, PATH_CO2, total_co2, True, year_input - 2013)
        animation.display_animated_graph(sea_level_points)

        second_instructions.grid(row=5, column=0, columnspan=2)

        land_loss_prompt.grid(row=6, column=0)
        land_loss_button.grid(row=6, column=1)

        pop_displaced_prompt.grid(row=7, column=0)
        pop_displaced_button.grid(row=7, column=1)


def land_loss_func() -> None:
    """
    This function corresponds to the land loss button that will output the land loss map.
    """
    year_input = int(year.get())
    co2_input = float(co2.get())
    total_co2 = (year_input - 2013) * co2_input

    sea_level_points = prediction.sea_level_prediction(PATH_SEA_LEVEL, PATH_CO2, total_co2, False, year_input - 2013)
    sea_level_rise = sea_level_points[-1] - sea_level_points[0]

    land_loss_points = prediction.land_loss_national_stats(PATH_LAND_LOSS, sea_level_rise)
    maps.display_map(land_loss_points, 'Land Lost', PATH_COUNTRY_TO_CODE)


def pop_displaced_func() -> None:
    """
    This function corresponds to the population displaces button that will output the population displacement map.
    """
    year_input = int(year.get())
    co2_input = float(co2.get())
    total_co2 = (year_input - 2013) * co2_input

    sea_level_points = prediction.sea_level_prediction(PATH_SEA_LEVEL, PATH_CO2, total_co2, False, year_input - 2013)
    sea_level_rise = sea_level_points[-1] - sea_level_points[0]

    pop_displacement_points = prediction.pop_displacement_national_stats(PATH_POP_DISPLACEMENT, sea_level_rise)
    maps.display_map(pop_displacement_points, 'Population Displaced', PATH_COUNTRY_TO_CODE)


# Assigning elements
window.title("CSC110 Final Project")

greeting = Label(window, text='Welcome to our CSC110 Final Project!')
instructions = Label(window, text="To get started, enter a year after 2013 "
                                  "\n and a co2 emissions per year in metric tonnes greater than 1"
                                  "\n (note that the co2 emissions in 2013 was 35k).")
year_prompt = Label(window, text="Input Year")
year = Entry(window)
co2_prompt = Label(window, text="Input Co2/year")
co2 = Entry(window)
start_button = Button(window, text="Start", padx=50, command=start_function)
second_instructions = Label(window, text="\n The following buttons will open choropleth maps"
                                         "\n representing the land loss % and population"
                                         "\n displacement % of various developing countries.\n")
land_loss_prompt = Label(window, text="Land Loss")
land_loss_button = Button(window, text="Show Map", command=land_loss_func, padx=25)
pop_displaced_prompt = Label(window, text="Population Displacement")
pop_displaced_button = Button(window, text="Show Map", command=pop_displaced_func, padx=25)

# Displaying the previously assigned elements
greeting.grid(row=0, column=0, columnspan=2)
instructions.grid(row=1, column=0, columnspan=2)
year_prompt.grid(row=2, column=0)
year.grid(row=2, column=1)
co2_prompt.grid(row=3, column=0)
co2.grid(row=3, column=1)
start_button.grid(row=4, column=0, columnspan=2)

window.mainloop()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'animation', 'prediction', 'maps'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
