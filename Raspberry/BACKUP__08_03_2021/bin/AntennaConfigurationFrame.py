# ========================================================================
# Title:        AntennaConfigurationFrame
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  A frame to display all antenna configuration elements
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================

# ==[ Import ]============================================================
import tkinter as Tk
from tkinter import ttk

# ==[ Constants ]=========================================================
CONFIG_FRAME_BG_COLOR = "lightgreen"

# ==[ Class definition ]==================================================
class AntennaConfigurationFrame(Tk.LabelFrame):

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, container, *args, **kwargs):
        Tk.LabelFrame.__init__(self, container, *args, **kwargs)
        self.configure_self()
        self.create_widgets()
        self.initialize_members()
        self.initialize_widgets()

    def configure_self(self):
        self.configure(relief="solid", bd=1, background=CONFIG_FRAME_BG_COLOR)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        pass

    def create_widgets(self):
        # --< Create GUI components >-------------------------------------
        self.pitchYawSeperator = ttk.Separator(self, orient="horizontal")
        self.yawButtonSeperator = ttk.Separator(self, orient="horizontal")

        # pitch
        self.pitchLabel = ttk.Label(master=self, text="Pitch:", background=CONFIG_FRAME_BG_COLOR, font="helvetica 9 underline")
        self.pitchFromLabel = ttk.Label(master=self, text="From", background=CONFIG_FRAME_BG_COLOR)
        self.pitchToLabel = ttk.Label(master=self, text="to",background=CONFIG_FRAME_BG_COLOR)
        self.pitchFromEntryField = ttk.Entry(master=self, text="", background=CONFIG_FRAME_BG_COLOR)
        self.pitchToEntryField = ttk.Entry(master=self, text="", background=CONFIG_FRAME_BG_COLOR)

        # yaw
        self.yawLabel = ttk.Label(master=self, text="Yaw:", background=CONFIG_FRAME_BG_COLOR, font="helvetica 9 underline")
        self.yawFromLabel = ttk.Label(master=self, text="From", background=CONFIG_FRAME_BG_COLOR)
        self.yawToLabel = ttk.Label(master=self, text="to", background=CONFIG_FRAME_BG_COLOR)
        self.yawFromEntryField = ttk.Entry(master=self, text="", background=CONFIG_FRAME_BG_COLOR)
        self.yawToEntryField = ttk.Entry(master=self, text="", background=CONFIG_FRAME_BG_COLOR)

        # apply, reset
        self.resetButton = ttk.Button(master=self, text="Reset", command=self.resetButtonClicked)
        self.applyButton = ttk.Button(master=self, text="Apply", command=self.applyButtonClicked)

        # --< Grid all GUI components >-----------------------------------
        # pitch
        self.pitchLabel.grid(row=0, column=0, columnspan=4, sticky="w")
        self.pitchFromLabel.grid(row=1, column=0)
        self.pitchToLabel.grid(row=1, column=2)
        self.pitchFromEntryField.grid(row=1, column=1, padx=4)
        self.pitchToEntryField.grid(row=1, column=3, padx=4)

        # seperator 1
        self.pitchYawSeperator.grid(row=2, column=0, columnspan=4, sticky="ew", pady=4)

        # yaw
        self.yawLabel.grid(row=3, column=0, columnspan=4, sticky="w")
        self.yawFromLabel.grid(row=4, column=0)
        self.yawToLabel.grid(row=4, column=2)
        self.yawFromEntryField.grid(row=4, column=1, padx=4)
        self.yawToEntryField.grid(row=4, column=3, padx=4)

        # seperator 2
        self.yawButtonSeperator.grid(row=5, column=0, columnspan=4, sticky="ew", pady=4)

        # buttons (apply, reset)
        self.resetButton.grid(row=6, column=0, columnspan=2, sticky="ew")
        self.applyButton.grid(row=6, column=2, columnspan=2, sticky="ew")

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
    def resetButtonClicked(self):
        print("resetButtonClicked()")
        pass

    def applyButtonClicked(self):
        print("applyButtonClicked()")
        pass