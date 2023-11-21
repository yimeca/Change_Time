from tkinter import *
from tkinter import ttk

# Classes

class DateOption(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        button = ttk.Button(self, text="Press me", command=self.calculate)
        button.grid(column=0, row=0, sticky=(N, W, E, S))

    def calculate(self):
        pass

# Main

def main():

    root = Tk()
    root.title("Change The Time and Date")

    mainframe = ttk.Frame(root, padding="3 3 12 12").grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    time1 = DateOption(root, padding="3 3 12 12").grid(column=0, row=0, sticky=(N, W, E, S))

    root.mainloop()

if __name__ == "__main__":
    main()