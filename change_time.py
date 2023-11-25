from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar

# Classes

class TimeOption(ttk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global root

        self.title_var = StringVar
        self.title_entry = ttk.Entry(self).grid(column=0, row=0, columnspan=3, pady=10)

        calendar = Calendar(self, year=2023, month=11, day=24).grid(column=0, row=1, rowspan=2)
        
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
        self.change_time = ttk.Button(self, text="Change Time", command=self.change_time
                                      ).grid(column=4, row=2, columnspan=1)

    def change_time(self):
        print()
        print("change")

# Functions

# Reset Time Function
def reset_time():
    print("reset")

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

if __name__ == "__main__":
    main()