import ctypes
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import sys
from _datetime import datetime
import requests

# Classes

class TimeOption(ttk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global root

        self.title_var = StringVar()
        self.title_entry = ttk.Entry(self).grid(column=0, row=0, columnspan=3, pady=10)

        self.date_var = StringVar()
        self.date_var.set("23/11/2023")
        self.calendar = Calendar(self, textvariable=self.date_var,
                                 date_pattern="dd/mm/y").grid(column=0, row=1, rowspan=2)
        
        # Hour
        self.hour_label = ttk.Label(self, text="Hour").grid(column=1, row=1, sticky="s")
        self.hour_var = StringVar()
        self.hour_var.set("00")
        self.hour = ttk.Spinbox(self, from_=00, to=23, increment=1, textvariable=self.hour_var, width = 2,
                                format="%02.0f", wrap=True).grid(column=1, row=2, sticky="n")
        
        # Min
        self.min_label = ttk.Label(self, text="Min").grid(column=2, row=1, sticky="s")
        self.min_var = StringVar()
        self.min_var.set("00")
        self.min = ttk.Spinbox(self, from_=00, to=59, increment=1, textvariable=self.min_var, width = 2,
                               format="%02.0f", wrap=True).grid(column=2, row=2, sticky="n")
        self.min_var.set("00")
        
        # Sec
        self.sec_label = ttk.Label(self, text="Sec").grid(column=3, row=1, sticky="s")
        self.sec_var = StringVar()
        self.sec_var.set("00")
        self.sec = ttk.Spinbox(self, from_=00, to=59, increment=1, textvariable=self.sec_var, width = 2,
                               format="%02.0f", wrap=True).grid(column=3, row=2, sticky="n")
        self.sec_var.set("00")

        # Button
        self.change_time = ttk.Button(self, text="Change Time", command=self.change_time_to_chosen
                                      ).grid(column=4, row=2, columnspan=1)

    def change_time_to_chosen(self):
        date = self.date_var.get().split("/")
        time_tuple = (int(date[2]), # Year
                      int(date[1]), # Month
                      int(date[0]), # Day
                      int(self.hour_var.get()) , # Hour
                      int(self.min_var.get()), # Minute
                      int(self.sec_var.get()), # Second
                      0 # Milisecond
        )

        print("change")
        print(time_tuple)
        win_change_time(time_tuple)
        print(self.hour_var.get(), self.min_var.get(), self.sec_var.get(), self.date_var.get())

# Functions

def win_change_time(time_tuple):
    import win32api
    dayOfWeek = datetime(*time_tuple).isocalendar()[2]
    new_time = time_tuple[:2] + (dayOfWeek,) + time_tuple[2:]
    win32api.SetSystemTime(*new_time)

# Reset Time Function
def reset_time():
    timeapi = requests.get("http://worldtimeapi.org/api/timezone/Etc/GMT")
    tuple_info = timeapi.json()['datetime']
    year = int(tuple_info[0:4])
    month = int(tuple_info[5:7])
    day = int(tuple_info[8:10])
    hour = int(tuple_info[11:13])
    minute = int(tuple_info[14:16])
    second= int(tuple_info[17:19])
    millisecond = 0
    api_tuple = (year,month,day,hour,minute,second,millisecond)
    win_change_time(api_tuple)
    print("reset")
    print(year,month,day,hour,minute,second,millisecond)

# Main

def main():

    global root
    root = Tk()
    root.title("Change The Time and Date")

    # Styles
    global style
    style = ttk.Style()
    style.theme_use("clam")

    mainframe = ttk.Frame(root, padding="3 3 12 12").grid(column=0, row=0, sticky="nwes")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    time1 = TimeOption(mainframe, padding="12 12 12 12").grid(row=0, column=0)
    time2 = TimeOption(mainframe, padding="12 12 12 12").grid(row=0, column=1)
    time3 = TimeOption(mainframe, padding="12 12 12 12").grid(row=1, column=0)
    time4 = TimeOption(mainframe, padding="12 12 12 12").grid(row=1, column=1)

    reset = ttk.Button(mainframe, text="Reset Time and Date (Requires internet)", command=reset_time
                       ).grid(row=3, column=0, columnspan=3)

    root.mainloop()

def root_access():
    """
    Function to check if the current user has root access or administrative privileges.

    Returns:
    - bool:
        True if the user has root access or administrative privileges, False otherwise.
    """

    # Checking the operating system to determine the appropriate command to check for root access.
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        # On Linux and macOS, we can use the os.geteuid() function to check for root access.
        return os.geteuid() == 0
    elif sys.platform == 'win32':
        # On Windows, we can use the ctypes library to check for administrative privileges.
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except ImportError:
            # If ctypes is not available, we cannot determine root access.
            return False
    else:
        # If the operating system is not supported, we cannot determine root access.
        return False

if __name__ == "__main__":
    if root_access():
        main()
    else:
        messagebox.showwarning(message="You need admin rights to change the time")