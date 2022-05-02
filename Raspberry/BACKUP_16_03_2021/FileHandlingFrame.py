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
from exceptions import *
from Heatmapper import *
from systemAttributes import *
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
        self.initialize_members()
        self.create_widgets()
        self.initialize_widgets()
        self.refresh_widgets()
        pass

    def configure_self(self):
        self.configure(relief="solid", bd=1, background=FileHandlingFrame.FHANDLING_FRAME_BG_COLOR)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform="x")
        pass

    def create_widgets(self):
        # Create ui components
        self.importButton = ttk.Button(master=self, text="Import", command=self.importButtonClicked)
        self.exportButton = ttk.Button(master=self, text="Export", command=self.exportButtonClicked)
        
        self.currentFileLabel = ttk.Label(master=self, text="Current file:", background=FileHandlingFrame.FHANDLING_FRAME_BG_COLOR)
        self.networkDropdown = ttk.OptionMenu(self, self.networkVarList, command=self.getNetworkDropdownState)
        self.networkDropdown["menu"].config(bg=FileHandlingFrame.FHANDLING_FRAME_BG_COLOR)
        self.networkDropdownMenu = self.networkDropdown["menu"]

        self.createHeatmapButton = ttk.Button(master=self, text="Create Heatmap", command=self.createHeatmapButtonClicked)
        self.heatmapSettingsButton = ttk.Button(master=self, text="Settings", command=self.heatmapSettingsButtonClicked)
        self.resetButton = ttk.Button(master=self, text="Reset", command=self.resetButtonClicked)

    	# grid components
        self.importButton.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.exportButton.grid(row=0, column=4, columnspan=4, sticky="ew")

        self.currentFileLabel.grid(row=1, column=0, columnspan=4, sticky="w")
        self.networkDropdown.grid(row=1, column=4, columnspan=4, sticky="ew")

        self.createHeatmapButton.grid(row=2, column=0, columnspan=6, sticky="ew")
        self.heatmapSettingsButton.grid(row=2, column=6, columnspan=1, sticky="ew")
        self.resetButton.grid(row=2, column=7, columnspan=1, sticky="ew")
        pass

    def initialize_members(self):
        self.networkVarList = Tk.StringVar(self)
        self.networkDropdownMenu = None
        pass 

    def initialize_widgets(self):
        # initialize widget states
        pass

    def refresh_widgets(self):
        # Set current file label to currently opened file
        if ((self.master.workingFile == "") or (self.master.workingFile is None)):
            self.currentFileLabel['text'] = ("No valid file loaded")
        else:            
            self.currentFileLabel['text'] = ("Loaded file:\t" + os.path.basename(self.master.workingFile))

        if (self.master.workingDataSeries is None):
            tmpLabel = "No data series set"
            self.networkDropdownMenu.delete(0, "end")
            self.networkDropdownMenu.add_command(label=tmpLabel,
                                                command=lambda value=tmpLabel:
                                                    self.networkVarList.set(value))
            self.networkVarList.set(tmpLabel)
            return

        self.networkDropdownMenu.delete(0, "end")
        for foundNetwork in self.master.workingDataSeries.networks:
            self.networkDropdownMenu.add_command(label=foundNetwork.ssid, 
                                                command=lambda value=foundNetwork.ssid:
                                                    self.networkVarList.set(value))
            self.networkVarList.set(foundNetwork.ssid)            
            
        pass

    # --< Generic initializer >-------------------------------------------
    # ...

    # --< Button actions >------------------------------------------------
    def importButtonClicked(self):
        print("importButtonClicked()")
        try:
            self.importData()
            self.refresh_widgets()
        except Exception as ex:
            self.evaluateException(ex)
        
    def exportButtonClicked(self):
        print("exportButtonClicked()")
        try:
            self.exportData()
            self.refresh_widgets()
        except Exception as ex:
            self.evaluateException(ex)

    def createHeatmapButtonClicked(self):
        print("createHeatmapButtonClicked()")
        print("-> Starting heatmapTest protected")
        
        # --< Check for safety >------------------------------------------
        if (self.master.workingDataSeries is None):
            mb.showerror(master=self.master, title="No data series available", message="No data series is available for heatmap creation.")
            return 
        if not (type(self.master.workingDataSeries) == DataSeries):
            mb.showerror(master=self.master, title="No data series available", message="The data series seems to be corrupted. Try to fix on your own ¯\_(ツ)_/¯")
            return
        # --< Fetch settings >--------------------------------------------
        hm_config = HeatmapConfig()
        # hm_config.selectedNetwork = self.networkDropdownState()
        hm_config.showOnlyMap = False
        hm_config.selectedNetwork = self.networkVarList.get()

        # --< Create heatmap >--------------------------------------------
        self.heatmapTest(self.master.workingDataSeries, hm_config)

        pass

    def heatmapSettingsButtonClicked(self):
        print("heatmapConfigurationButtonClicked()")
        # print("-> Starting heatmapTest unprotected")
        # self.heatmapTest(None, None)

        pass

    def resetButtonClicked(self):
        self.master.workingDataSeries = None
        self.master.workingFile = ""
        self.refresh_widgets()
        pass

    # --< Methods >-------------------------------------------------------
    def evaluateException(self, exception):
        opzioni = type(exception)

        if opzioni == DataSeriesIsNullException:
            tmpmsg4 = "No data series is loaded and thus can't be export.\nPlease import or acquire a data series before exporting it."
            mb.showerror(master=self.master, title="No data series available", message=tmpmsg4)
        elif opzioni == DataSeriesIsNotOfTypeDataSeriesException:
            tmpmsg5 = "The data series seems to have been corrupted (is not of type DataSeries).\nPlease try again or restart the program."
            mb.showerror(master=self.master, title="Dataseries is corrupted", message=tmpmsg5)
        elif opzioni == NoDataSeriesExistentException:
            raise exception
        elif opzioni == CouldntExportException:
            tmpmsg6 = ("Wasn't able to export to " + "\"" + str(os.path.basename(self.destinationFile)) + "\".\nPlease try again.")
            mb.showerror(master=self.master, title="Couldnt export to file", message=tmpmsg6)
        elif opzioni == CouldntPickleException:
            tmpmsg7 = ("Wasn't able to pickle \"" + str(self.master.workingDataSeries.name) + "\" to \"" + str(os.path.basename(self.destinationFile)) + "\".\nPlease try again.")
            mb.showerror(master=self.master, title="Couldnt export to file", message=tmpmsg7)
        elif opzioni == CouldntUnPickleException:
            tmpmsg3 = ("Wasn't able to load object of " + "\"" + str(os.path.basename(self.master.workingFile)) + "\".\nPlease try again.")
            mb.showerror(master=self.master, title="Couldn't load object", message=tmpmsg3)
        elif opzioni == FileNonExistentException:
            tmpmsg1 = ("File " + "\"" + str(os.path.basename(self.master.workingFile)) + "\" does not exist.")
            mb.showerror(master=self.master, title="File non-existent", message=tmpmsg1)
        elif opzioni == FileNonExistentException:
            tmpmsg2 = ("File " + "\"" + str(os.path.basename(self.master.workingFile)) + "\" is not a valid file type (must be \"" + PICKLE_FILE_EXTENSION + "\").")
            mb.showerror(master=self.master, title="File not valid", message=tmpmsg2)
        elif opzioni == CouldntOpenFileException:
            mb.showwarning(master=self.master, title="Something went wong ...", message="Something went wrong while trying to open/access the specified file.\nPlease try again.")
        else:
            raise exception

    def importData(self):
        
        try:
            tmp_extensions = ("*." + PICKLE_FILE_EXTENSION)
            self.master.workingFile = fd.askopenfilename(initialdir =   "/", 
                                                        title   =   "Please select antenna data", 
                                                        filetypes   =   [("Antenna data files", tmp_extensions)]
                                                        )
        except Exception:
            raise CouldntOpenFileException("")
        
        # Check whether a file was selected
        if(self.master.workingFile == ""):
            # mb.showinfo(master=self.master, title="No file selected", message="No file selected.")
            return

        # Check whether it exists
        if(not os.path.isfile(self.master.workingFile)):
            self.master.workingFile = ""
            raise FileNonExistentException("")

        # Check whether it's a *.(PICKLE_FILE_EXTENSION) file (usually *.a24)
        if(not self.master.workingFile.endswith(PICKLE_FILE_EXTENSION)):
            self.master.workingFile = ""
            raise FileNotValidException("")

        # Try to unpickle file
        try:
            self.master.workingDataSeries = DataSeries.unpickle(self.master.workingFile)
        except Exception:
            self.master.workingFile = ""
            raise CouldntUnPickleException("")

        # Show success of import
        succMsg = "Successfully imported \"" + str(self.master.workingDataSeries.name) + "\" from \"" + str(os.path.basename(self.master.workingFile)) + "\"."
        mb.showinfo(master=self.master, title="Successful import", message=succMsg)

        pass

    def exportData(self):
        # Check whether workingDataSeries is not null
        if (self.master.workingDataSeries is None):
            raise DataSeriesIsNullException("")

        # Check whether workingDataSeries is of type DataSeries
        if not (type(self.master.workingDataSeries) is DataSeries):
            raise DataSeriesIsNotOfTypeDataSeriesException("")

        # Choose file
        try:
            dext = ("." + PICKLE_FILE_EXTENSION)
            self.destinationFile = fd.asksaveasfilename(initialdir="/",
                                title="Export data series",
                                defaultextension=dext
            )
        except Exception:
            raise CouldntExportException("")

        try:
            self.master.workingDataSeries.pickle(self.destinationFile)
        except Exception:
            raise CouldntPickleException("")
        
        succMsg2 = "Successfully exported \"" + str(self.master.workingDataSeries.name) + "\" to \"" + str(os.path.basename(self.destinationFile)) + "\"."
        mb.showinfo(master=self.master, title="Successful export", message=succMsg2)

        pass

    def getNetworkDropdownState(self, value):
        self.networkDropdownState = value
        print(self.networkDropdownState)

    def changeLockState(self, locked):
        if locked:
            self.networkDropdown.state(['disabled'])
            self.importButton.state(['disabled'])
            self.exportButton.state(['disabled'])
            self.createHeatmapButton.state(['disabled'])
            self.heatmapSettingsButton.state(['disabled'])
            self.resetButton.state(['disabled'])
        elif not locked:
            self.networkDropdown.state(['!disabled'])
            self.importButton.state(['!disabled'])
            self.exportButton.state(['!disabled'])
            self.createHeatmapButton.state(['!disabled'])
            self.heatmapSettingsButton.state(['!disabled'])
            self.resetButton.state(['!disabled'])
        else:
            raise Exception("Failing to (un)lock FileHandlingFrame")
        return

    def heatmapTest(self, dataseries, hm_config):
        h = Heatmapper(self, dataseries, hm_config)
        h.create()


        