# ==[ Import ]============================================================
import tkinter as Tk
from tkinter import ttk

# ==[ Class definition ]==================================================
class FileHandlingFrame(Tk.LabelFrame):

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, container, *args, **kwargs):
        Tk.LabelFrame.__init__(self, container, *args, **kwargs)
        self.configure_self()
        self.create_widgets()
        pass

    def configure_self(self):
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform="x")
        self.pack()
        pass

    def create_widgets(self):
        # Create ui components
        self.importButton = ttk.Button(master=self, text="Import")
        self.exportButton = ttk.Button(master=self, text="Export")
        self.currentLabel = ttk.Label(master=self, text="Current")
        self.createButton = ttk.Button(master=self, text="Create")
        self.configurationButton = ttk.Button(master=self, text="s")

    	# Grid components
        self.importButton.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.exportButton.grid(row=0, column=4, columnspan=4, sticky="ew")
        self.currentLabel.grid(row=1, column=0, columnspan=8, sticky="w")
        self.createButton.grid(row=2, column=0, columnspan=7, sticky="ew")
        self.configurationButton.grid(row=2, column=7, columnspan=1, sticky="ew")
        pass

# ==[ Start of main application ]=========================================
if __name__ == "__main__":
    root = Tk.Tk()
    root.resizable(width=False, height=False)
    root.title("MWE")
    mainframe = Tk.Frame(master=root)
    mainframe.pack()
    application = FileHandlingFrame(container=mainframe)
    application.mainloop()