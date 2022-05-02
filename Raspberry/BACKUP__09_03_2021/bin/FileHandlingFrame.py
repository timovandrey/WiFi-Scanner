# ========================================================================
# Title:        FileHandlingFrame
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  A frame to display all file handling elements
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================

# ==[ System imports ]====================================================
import os
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter as Tk
from tkinter import ttk
# ==[ Custom imports ]====================================================
import MainApplication as main
from dataSeries import DataSeries


# ==[ Class definition ]==================================================
class FileHandlingFrame(Tk.LabelFrame):

    # ==[ Constants ]=====================================================
    FHANDLING_FRAME_BG_COLOR = "PaleVioletRed1"

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, container, *args, **kwargs):
        Tk.LabelFrame.__init__(self, container, *args, **kwargs)
        self.configure_self()
        self.create_widgets()
        self.initialize_members()
        self.initialize_widgets()
        pass

    def configure_self(self):
        self.configure(relief="solid", bd=1, background=FileHandlingFrame.FHANDLING_FRAME_BG_COLOR)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform="x")
        pass

    def create_widgets(self):
        # Create ui components
        self.importButton = ttk.Button(master=self, text="Import", command=self.importButtonClicked)
        self.exportButton = ttk.Button(master=self, text="Export", command=self.exportButtonClicked)
        self.createHeatmapButton = ttk.Button(master=self, text="Create Heatmap", command=self.createHeatmapButtonClicked)
        self.heatmapSettingsButton = ttk.Button(master=self, text="Settings", command=self.heatmapSettingsButtonClicked)
        self.currentFileLabel = ttk.Label(master=self, text="Current file:", background=FileHandlingFrame.FHANDLING_FRAME_BG_COLOR)
    	
        # TODO: Continue here: Design is still not very nice

    	# grid components
        self.importButton.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.exportButton.grid(row=0, column=4, columnspan=4, sticky="ew")
        self.currentFileLabel.grid(row=1, column=0, columnspan=8, sticky="w")
        self.createHeatmapButton.grid(row=2, column=0, columnspan=7, sticky="ew")
        self.heatmapSettingsButton.grid(row=2, column=7, columnspan=1, sticky="ew")
        pass

    def initialize_members(self):
        # initialize members
        pass 

    def initialize_widgets(self):
        # initialize widget states
        pass

    # --< Generic initializer >-------------------------------------------
    # ...

    # --< Button actions >------------------------------------------------
    def importButtonClicked(self):
        print("importButtonClicked()")

        try:
            tmp_extensions = ("*." + main.PICKLE_FILE_EXTENSION)
            self.master.workingFile = fd.askopenfilename(initialdir =   "/", 
                                                        title   =   "Please select antenna data", 
                                                        filetypes   =   [("Antenna data files", tmp_extensions)]
                                                        )
        except Exception:
            mb.showwarning(master=self.master, title="Something went wong ...", message="Something went wrong while trying to open/access the specified file.\nPlease try again.")
            return
        
        # Check whether a file was selected
        if(self.master.workingFile == ""):
            # mb.showinfo(master=self.master, title="No file selected", message="No file selected.")
            return

        # Check whether it exists
        if(not os.path.isfile(self.master.workingFile)):
            tmpmsg1 = ("File " + "\"" + str(os.path.basename(self.master.workingFile)) + "\" does not exist.")
            mb.showerror(master=self.master, title="File non-existent", message=tmpmsg1)
            self.master.workingFile = ""
            return

        # Check whether it's a *.(PICKLE_FILE_EXTENSION) file (usually *.a24)
        if(not self.master.workingFile.endswith(main.PICKLE_FILE_EXTENSION)):
            tmpmsg2 = ("File " + "\"" + str(os.path.basename(self.master.workingFile)) + "\" is not a valid file type (must be \"" + main.PICKLE_FILE_EXTENSION + "\").")
            mb.showerror(master=self.master, title="File not valid", message=tmpmsg2)
            self.master.workingFile = ""
            return

        # Try to unpickle file
        try:
            self.master.workingDataSeries = DataSeries.unpickle(self.master.workingFile)
        except Exception:
            tmpmsg3 = ("Wasn't able to load object of " + "\"" + str(os.path.basename(self.master.workingFile)) + "\".\nPlease try again.")
            mb.showerror(master=self.master, title="Couldn't load object", message=tmpmsg3)
            self.master.workingFile = ""
            return

        self.currentFileLabel['text'] = ("Loaded file:\t" + os.path.basename(self.master.workingFile))

        succMsg = "Successfully imported \"" + str(self.master.workingDataSeries.name) + "\" from \"" + str(os.path.basename(self.master.workingFile)) + "\"."
        mb.showinfo(master=self.master, title="Successful import", message=succMsg)

        pass

    def exportButtonClicked(self):
        print("exportButtonClicked()")

        # Check whether workingDataSeries is not null
        if (self.master.workingDataSeries is None):
            tmpmsg4 = "No data series is loaded and thus can't be export.\nPlease import or acquire a data series before exporting it."
            mb.showerror(master=self.master, title="No data series available", message=tmpmsg4)
            return

        # Check whether workingDataSeries is of type DataSeries
        if not (type(self.master.workingDataSeries) is DataSeries):
            tmpmsg5 = "The data series seems to have been corrupted (is not of type DataSeries).\nPlease try again or restart the program."
            mb.showerror(master=self.master, title="Dataseries is corrupted", message=tmpmsg5)
            return

        # Choose file
        try:
            dext = ("." + main.PICKLE_FILE_EXTENSION)
            destinationFile = fd.asksaveasfilename(initialdir="/",
                                title="Export data series",
                                defaultextension=dext
            )
        except Exception:
            tmpmsg6 = ("Wasn't able to export to " + "\"" + str(os.path.basename(destinationFile)) + "\".\nPlease try again.")
            mb.showerror(master=self.master, title="Couldnt export to file", message=tmpmsg6)
            return

        try:
            self.master.workingDataSeries.pickle(destinationFile)
        except Exception:
            tmpmsg7 = ("Wasn't able to pickle \"" + str(self.master.workingDataSeries.name) + "\" to \"" + str(os.path.basename(destinationFile)) + "\".\nPlease try again.")
            mb.showerror(master=self.master, title="Couldnt export to file", message=tmpmsg7)
            return
        
        succMsg2 = "Successfully exported \"" + str(self.master.workingDataSeries.name) + "\" to \"" + str(os.path.basename(destinationFile)) + "\"."
        mb.showinfo(master=self.master, title="Successful import", message=succMsg2)

        pass

    def createHeatmapButtonClicked(self):
        print("createHeatmapButtonClicked()")
        pass

    def heatmapSettingsButtonClicked(self):
        print("heatmapConfigurationButtonClicked()")
        pass