# ========================================================================
# Title:        AntennaStateFrame
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  A frame to display all antenna state elements
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================

# ==[ System imports ]====================================================
import tkinter as Tk
from tkinter import ttk
# ==[ Custom imports ]====================================================
from IndicatorLight import IndicatorLight

# ==[ Class definition ]==================================================
class AntennaStateFrame(Tk.LabelFrame):

    # ==[ Constants ]=====================================================
    STATE_FRAME_BG_COLOR = "tomato"
    
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
        self.configure(relief="solid", bd=1, background=AntennaStateFrame.STATE_FRAME_BG_COLOR)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=3)
        pass

    def create_widgets(self):
        
        self.runningStateIndicatorLight = IndicatorLight(master=self, bg=AntennaStateFrame.STATE_FRAME_BG_COLOR, indicatorColor="lightblue")
        self.runningStateIndicatorLabel = ttk.Label(master=self, background=AntennaStateFrame.STATE_FRAME_BG_COLOR, text="Running ...")
        
        self.errorStateIndicatorLight = IndicatorLight(master=self, bg=AntennaStateFrame.STATE_FRAME_BG_COLOR, indicatorColor="green")
        self.errorStateIndicatorLabel = ttk.Label(master=self, background=AntennaStateFrame.STATE_FRAME_BG_COLOR, text="No error(s)")

        self.progressBarLabel = ttk.Label(master=self, background=AntennaStateFrame.STATE_FRAME_BG_COLOR, text="Progress:", font=("helvetica 9 underline"))
        self.progressBar = ttk.Progressbar(master=self, orient="horizontal", length=(self.winfo_width() - 2), mode="determinate")
        
        # grid components
        self.runningStateIndicatorLight.grid(row=0, column=0)
        self.runningStateIndicatorLabel.grid(row=0, column=1, columnspan=2, padx=2)
        
        self.errorStateIndicatorLight.grid(row=1, column=0)
        self.errorStateIndicatorLabel.grid(row=1, column=1, columnspan=2, padx=2)

        self.progressBarLabel.grid(row=2, column=0, columnspan=3, sticky="w")
        self.progressBar.grid(row=3, column=0, columnspan=3, sticky="ew", padx=4, pady=4)

        pass

    def initialize_members(self):
        # initialize members
        pass 

    def initialize_widgets(self):
        # initialize widget states
        pass

    # --< Generic initializer >-------------------------------------------
    # ...