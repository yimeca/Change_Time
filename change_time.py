import re
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, SpinTimePickerModern, SpinTimePickerOld, constants

# Classes

class DateOption(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global root

        # Day
        increase_day = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=0, row=0)
        self.validate_day_wrapper = (root.register(self.validate_day), "%P", "%V")
        self.day_var = StringVar()
        self.day_var.set("0")
        day_entry = ttk.Entry(self, textvariable=self.day_var, validate="all",
                               validatecommand=self.validate_day_wrapper).grid(column=0, row=1)
        decrease_day = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=0, row=2)

        # Month
        increase_month = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=1, row=0)
        self.validate_month_wrapper = (root.register(self.validate_month), "%P", "%V")
        self.month_var = StringVar()
        self.month_var.set("0")
        month_entry = ttk.Entry(self, textvariable=self.month_var, validate="all",
                               validatecommand=self.validate_month_wrapper).grid(column=1, row=1)
        decrease_month = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=1, row=2)


#        # Increase Buttons
#        increase_day = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=0, row=0)
#        increase_month = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=1, row=0)
#        increase_year = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=2, row=0)
#        
#        increase_hour = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=3, row=0)
#        increase_minute = ttk.Button(self, style="ChangeTime.TButton", text="↑").grid(column=4, row=0)
#
#        # Entry
#        global root
#        self.validate_wrapper = (root.register(self.validate), "%P", "%V")
#        self.time_var = StringVar()
#        self.time_var.set("00/00/0000 00:00")
#        date_entry = ttk.Entry(self, textvariable=self.time_var, validate="all",
#                               validatecommand=self.validate_wrapper).grid(column=0, row=1, columnspan=5)
#        
#        # Decrease Buttons
#        decrease_day = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=0, row=2)
#        decrease_month = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=1, row=2)
#        decrease_year = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=2, row=2)
#        
#        increase_hour = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=3, row=2)
#        increase_minute = ttk.Button(self, style="ChangeTime.TButton", text="↓").grid(column=4, row=2)
#
#
#        button = ttk.Button(self, text="Press me", command=self.calculate)
#        button.grid(column=0, row=6, sticky=(N, W, E, S))
    
    def validate_day(self, newval, op):
        if op == "key":
            print(newval)
            if (re.match("^[0-9]*$", newval) is not None and  len(newval) <= 2 and
                int(newval) <= 31):
                return True
        return True
    
    def validate_month(self, newval, op):
        if op == "key":
            print(newval)
        return True

    def calculate(self):
        pass

class TimeOption(ttk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global root

        self.title_var = StringVar
        self.title_entry = ttk.Entry(self).grid(column=0, row=0, columnspan=3, )

        calendar = Calendar(self, year=2023, month=11, day=24).grid(column=0, row=1, rowspan=2)
        
        # Hour
        self.hour_label = ttk.Label(self, text="Hour").grid(column=1, row=2)
        self.hour_var = StringVar()
        self.hour_var.set("00")
        self.hour = ttk.Spinbox(self, from_=00, to=23, increment=1, textvariable=self.hour_var, width = 2, format="%02.0f"
                                ).grid(column=1, row=2)
        
        # Min
        self.min_label = ttk.Label(self, text="Min").grid(column=2, row=1)
        self.min_var = StringVar()
        self.min_var.set("00")
        self.min = ttk.Spinbox(self, from_=00, to=59, increment=1, textvariable=self.min_var, width = 2, format="%02.0f"
                               ).grid(column=2, row=2)
        self.min_var.set("00")

        # Button
        self.change_time = ttk.Button(self, text="Change Time").grid(column=3, row=1, columnspan=2)


# Main

def main():

    global root
    root = Tk()
    root.title("Change The Time and Date")

    # Styles
    global style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("ChangeTime.TButton", width=2)
    style.configure("Increase.ChangeTime.TButton", text="↑")
    style.configure("Decrease.ChangeTime.TButton", text="↓")

    mainframe = ttk.Frame(root, padding="3 3 12 12").grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    time1 = TimeOption(mainframe, padding="12 12 12 12").grid(row=0, column=0)
    time2 = TimeOption(mainframe, padding="12 12 12 12").grid(row=0, column=1)
    time3 = TimeOption(mainframe, padding="12 12 12 12").grid(row=1, column=0)
    time4 = TimeOption(mainframe, padding="12 12 12 12").grid(row=1, column=1)

#    seperator = ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=3, column=0, columnspan=3)
#    reset_frame = ttk.LabelFrame(mainframe, padding="120 120 120 120").grid(row=3, column=0, columnspan=3, sticky=(N, W, E, S))
    reset = ttk.Button(mainframe, text="Reset Time and Date (Requires internet)").grid(row=3, column=0, columnspan=3)

#    time1 = DateOption(root, padding="3 3 12 12").grid(column=0, row=0, sticky=(N, W, E, S))
#    time2 = DateOption(root, padding="3 3 12 12").grid(column=0, row=1, sticky=(N, W, E, S))
#    time3 = DateOption(root, padding="3 3 12 12").grid(column=0, row=2, sticky=(N, W, E, S))

#    cal1 = Calendar(root, year=2020, month=5, day=22).grid(column=0, row=0)
#    tim1 = AnalogPicker(root).grid(column=1, row=0)
#    tim2 = SpinTimePickerModern(root, orient=constants.HORIZONTAL).grid(column=0, row=0)
#    cal2 = Calendar(root, selectmode="day", year=2020, month=5, day=22).grid(column=0, row=1)
#    cal3 = Calendar(root, selectmode="day", year=2020, month=5, day=22).grid(column=0, row=2)
#    cal4 = Calendar(root, selectmode="day", year=2020, month=5, day=22).grid(column=0, row=3)

    root.mainloop()

if __name__ == "__main__":
    main()