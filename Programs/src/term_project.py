"""!
@file lab4.py
Runs a pair of controlled motor responses from a step input and plots the results.
This program allows for the user to input a pair of desired angular distances and Kps.
With these values, the microcontroller will produce two step responses for the position of the motor using an encoder and proportional controller.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Spluttflob (original)
@date   2023-12-24 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import tkinter
import serial
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def restart_device():
    """!
    
    """
    # States COM device (May vary with different computers)
    com_port = 'COM5'
    
    # Tries to open the defined serial port and run data, and if it can not, will print error
    try:
        serial_port = serial.Serial(com_port, baudrate=115200, timeout=1)
    except serial.SerialException as error:
        print(f"could not open serial port '{com_port}': {error}")
    else:     
        # Writes (Ctrl-B, Ctrl-C, Ctrl-D) to reset the serial port and rerun main on microcontroller
        serial_port.write(b'\x02')
        serial_port.write(b'\x03')
        serial_port.write(b'\x04')
        
        # Closes the serial port
        serial_port.close()      


def tk_matplot(restart_device):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title('Run the program!')
    tk_root.geometry('100x100')

    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: restart_device())
    button_run.pack(side='top')

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(restart_device)


