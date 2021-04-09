from tkinter import *

window = Tk()
window.geometry("225x325")


# Functions for Buttons
def start_function():
    """"
    This function corresponds to the first start button that appears to the user that will output
    the sea level rise interactive animated graph. On the call of this function, we will also show
    the rest of the options to the user including the land loss map and the population displaced.
    """
    year_input = year.get()
    co2_input = co2.get()
    # Insert function that shows the graph using inputs assigned above
    land_loss_prompt.grid(row=6, column=0)
    land_loss_button.grid(row=6, column=1)
    pop_displaced_prompt.grid(row=7, column=0)
    pop_displaced_button.grid(row=7, column=1)
    second_instructions.grid(row=5, column=0, columnspan=2)


def land_loss_func():
    """"
    This function corresponds to the land loss button that will output the land loss map.
    """
    year_input = year.get()
    co2_input = co2.get()
    # Insert function that shows the graph using inputs assigned above


def pop_displaced_func():
    """"
    This function corresponds to the population displaces button that will output the population displacement map.
    """
    year_input = year.get()
    co2_input = co2.get()
    # Insert function that shows the graph using inputs assigned above


# Assigning elements
window.title("CSC110 Final Project")
greeting = Label(window, text='Welcome to our CSC110 Final Project')
instructions = Label(window, text="Insert Instructions "
                                  "\n (some restrictions on what year"
                                  "\n guidelines on what co2 emissions"
                                  "\n they might want to put) \n")
year_prompt = Label(window, text="Input Year")
year = Entry(window)
co2_prompt = Label(window, text="Input Co2/year")
co2 = Entry(window)
start_button = Button(window, text="Start", padx=50, command=start_function)
second_instructions = Label(window, text="\n Insert Second Instructions "
                                         "\n this will be very short "
                                         "\n if you want to see this click this\n")
land_loss_prompt = Label(window, text="Land Loss")
land_loss_button = Button(window, text="Show Map", command="land_loss_func", padx=25)
pop_displaced_prompt = Label(window, text="Pop Displaced")
pop_displaced_button = Button(window, text="Show Map", command="pop_displaced_func", padx=25)

# Displaying the previously assigned elements
greeting.grid(row=0, column=0, columnspan=2)
instructions.grid(row=1, column=0, columnspan=2)
year_prompt.grid(row=2, column=0)
year.grid(row=2, column=1)
co2_prompt.grid(row=3, column=0)
co2.grid(row=3, column=1)
start_button.grid(row=4, column=0, columnspan=2)


window.mainloop()
