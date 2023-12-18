import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import sys
from datetime import datetime
import requests

# Classes

class TimeOption(ttk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global root

        self.title_var = StringVar()
        self.title_entry = ttk.Entry(self, textvariable=self.title_var).grid(column=0, row=0, columnspan=3, pady=10)

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
        
        self.reset_time_option = ttk.Button(self, text="Now",
                                                      command=self.reset_time_option
                                                      ).grid(column=4, row=2, sticky="n", columnspan=1)

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

    def reset_time_option(self):
        global time_zone_var
        try:
            timeapi = requests.get(f"http://worldtimeapi.org/api/timezone/{time_zone_var.get()}")
        except Exception:
            messagebox.showwarning(message="You need internet for this")
        else:
            tuple_info = timeapi.json()['datetime']

            year = int(tuple_info[0:4])
            month = int(tuple_info[5:7])
            day = int(tuple_info[8:10])
            hour = tuple_info[11:13]
            minute = tuple_info[14:16]
            second= tuple_info[17:19]

            date = f"{day}/{month}/{year}"
            
            self.date_var.set(date)
            # Hour
            self.hour_var.set(f"{hour:.2}")
            # Minute
            self.min_var.set(f"{minute:.2}")
            # Second
            self.sec_var.set(f"{second:.2}")
            # Title
            self.title_var.set("")
    
    def __str__(self):
        
        date = self.date_var.get()#.split("/")
        time_tuple = (self.date_var.get(),
                      #f"{date[2]:.4}", # Year
                      #f"{date[1]:.2}", # Month
                      #f"{date[0]:.2}", # Day
                      f"{self.hour_var.get():.2}" , # Hour
                      f"{self.min_var.get():.2}", # Minute
                      f"{self.sec_var.get():.2}", # Second
                      self.title_var.get(), # Title
        )
        time_str = ""
        for time_number in time_tuple:
            time_str += time_number
        return time_str

# Functions

def win_change_time(time_tuple):
    import win32api
    dayOfWeek = datetime(*time_tuple).isocalendar()[2]
    new_time = time_tuple[:2] + (dayOfWeek,) + time_tuple[2:]
    win32api.SetSystemTime(*new_time)

# Reset Time Function
def reset_time():
    global time_zone_var
    try:
        timeapi = requests.get(f"http://worldtimeapi.org/api/timezone/{time_zone_var.get()}")
    except Exception:
        messagebox.showwarning(message="You need internet for this")
    else:
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

# On close

def on_close():
    global time1, time2, time3, time4, time_zone_var
#    save_list = []
    save_str = ""
    for time_option in [time1, time2, time3, time4]:
        save_str += (time_option.__str__() + "\n")
    save_str += time_zone_var.get() + "\n"
    print(save_str)
    with open("change_time_defaults.txt", "w") as defaults_file:
        defaults_file.write(save_str)

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Main

def main():

    global root
    root = Tk()
    root.title("Change The Time and Date")

    # Styles
    global style
    style = ttk.Style()
    style.theme_use("clam")

    # On close

    root.protocol("WM_DELETE_WINDOW", on_close)


    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky="nwes")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    global time1, time2, time3, time4, time_zone_var
    time1 = TimeOption(mainframe, padding="12 12 12 12")
    time1.grid(row=0, column=0)
    time2 = TimeOption(mainframe, padding="12 12 12 12")
    time2.grid(row=0, column=1)
    time3 = TimeOption(mainframe, padding="12 12 12 12")
    time3.grid(row=1, column=0)
    time4 = TimeOption(mainframe, padding="12 12 12 12")
    time4.grid(row=1, column=1)

    reset = ttk.Button(mainframe, text="Reset Time and Date (Requires internet)", command=reset_time
                       ).grid(row=3, column=0, columnspan=1)
    
    list_of_time_zones = ['Africa/Abidjan', 'Africa/Algiers', 'Africa/Bissau', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/El_Aaiun', 'Africa/Johannesburg', 'Africa/Juba', 'Africa/Khartoum', 'Africa/Lagos', 'Africa/Maputo', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Sao_Tome', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Asuncion', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Cayenne', 'America/Chicago', 'America/Chihuahua', 'America/Ciudad_Juarez', 'America/Costa_Rica', 'America/Cuiaba', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Fort_Nelson', 'America/Fortaleza', 'America/Glace_Bay', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/New_York', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Sitka', 'America/St_Johns', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Tijuana', 'America/Toronto', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/Troll', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuching', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Riyadh', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faroe', 'Atlantic/Madeira', 'Atlantic/South_Georgia', 'Atlantic/Stanley', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'CET', 'CST6CDT', 'EET', 'EST', 'EST5EDT', 'Etc/GMT', 'Etc/GMT+1', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7', 'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT-1', 'Etc/GMT-10', 'Etc/GMT-11', 'Etc/GMT-12', 'Etc/GMT-13', 'Etc/GMT-14', 'Etc/GMT-2', 'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9', 'Etc/UTC', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Chisinau', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Helsinki', 'Europe/Istanbul', 'Europe/Kaliningrad', 'Europe/Kirov', 'Europe/Kyiv', 'Europe/Lisbon', 'Europe/London', 'Europe/Madrid', 'Europe/Malta', 'Europe/Minsk', 'Europe/Moscow', 'Europe/Paris', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Sofia', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Ulyanovsk', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zurich', 'HST', 'Indian/Chagos', 'Indian/Maldives', 'Indian/Mauritius', 'MET', 'MST', 'MST7MDT', 'PST8PDT', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Kanton', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Marquesas', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'WET']
    time_zone_var = StringVar()
    time_zone_var.set("Etc/GMT")
    time_zone_combo_box = ttk.Combobox(mainframe, textvariable=time_zone_var,
                                            values=list_of_time_zones, state="readonly")
#    time_zone_combo_box.current(time_zone_combo_box.current())
#    time_zone_combo_box.set
    time_zone_combo_box.grid(row=3, column=1, columnspan=1)
#    time_zone_combo_box.bind('<<ComboboxSelected>>', lambda e: time_zone_var.set(
#        time_zone_var.get()))
    time_zone_combo_box.bind('<<ComboboxSelected>>', lambda e: time_zone_combo_box.selection_clear())
    
    # Set time from defaults

    try:
        with open("change_time_defaults.txt", "r") as defaults_file:
#            defaults_str = defaults_file.read()
            defaults_list = defaults_file.readlines()
    except FileNotFoundError:
        pass
    else:
        print("defaults_list")
        print(defaults_list)
#        print(defaults_str[2:44])
#        print(defaults_str[48:90])
#        print(defaults_str[94:136])
#        print(defaults_str[140:182])
#        print("hi")
#        defaults_list = [defaults_str[2:18], defaults_str[24:40], defaults_str[46:62], defaults_str[68:84]]
#        print(defaults_list)
#        print("hi")

        times_list = [time1, time2, time3, time4]

        for i, time_option, time_string in zip(range(4), times_list, defaults_list):
            print(i, time_option, time_string)
#            # Year
#            print(time_string[4:8])
 #           # Month
 #           print(time_string[2:4])
 #           # Day
 #           print(time_string[0:2])
            # Date
            print(time_string[0:10])
            time_option.date_var.set(time_string[0:10])
            # Hour
            print(time_string[10:12])
            time_option.hour_var.set(time_string[10:12])
            # Minute
            print(time_string[12:14])
            time_option.min_var.set(time_string[12:14])
            # Second
            print(time_string[14:16])
            time_option.sec_var.set(time_string[14:16])
#            time_option.hour_var.set(defaults_list[2:3])
            # Title
            print(time_string[16:-2])
            time_option.title_var.set(time_string[16:-1])
        
        time_zone_var.set(defaults_list[4][:-1]) # Get rid of the new line with [:-1]

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