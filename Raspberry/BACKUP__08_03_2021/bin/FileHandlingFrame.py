# ========================================================================
# Title:        FileHandlingFrame
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  A frame to display all file handling elements
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================

# ==[ Import ]============================================================
import tkinter as Tk
from tkinter import ttk

# ==[ Constants ]=========================================================
FHANDLING_FRAME_BG_COLOR = "PaleVioletRed1"

# ==[ Class definition ]==================================================
class FileHandlingFrame(Tk.LabelFrame):

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
        self.configure(relief="solid", bd=1, background=FHANDLING_FRAME_BG_COLOR)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1, uniform="x")
        pass

    def create_widgets(self):
        # Create ui components
        self.importButton = ttk.Button(master=self, text="Import", command=self.importButtonClicked)
        self.exportButton = ttk.Button(master=self, text="Export", command=self.exportButtonClicked)
        self.createHeatmapButton = ttk.Button(master=self, text="Create Heatmap", command=self.createHeatmapButtonClicked)
        self.heatmapConfigurationButton = ttk.Button(master=self, text="s", command=self.heatmapConfigurationButtonClicked)
        self.currentFileLabel = ttk.Label(master=self, text="Current", background=FHANDLING_FRAME_BG_COLOR)

        # TODO: Continue here: Design is still not very nice

    	# grid components
        self.importButton.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.exportButton.grid(row=0, column=4, columnspan=4, sticky="ew")
        self.currentFileLabel.grid(row=1, column=0, columnspan=8, sticky="w")
        self.createHeatmapButton.grid(row=2, column=0, columnspan=7, sticky="ew")
        self.heatmapConfigurationButton.grid(row=2, column=7, columnspan=1, sticky="ew")
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
        pass

    def exportButtonClicked(self):
        print("exportButtonClicked()")
        pass

    def createHeatmapButtonClicked(self):
        print("createHeatmapButtonClicked()")
        pass

    def heatmapConfigurationButtonClicked(self):
        print("heatmapConfigurationButtonClicked()")
        pass