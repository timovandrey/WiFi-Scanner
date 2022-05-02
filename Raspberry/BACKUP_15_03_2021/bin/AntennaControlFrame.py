# ========================================================================
# Title:        AntennaControlFrame
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  A frame to display all antenna controlling elements
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================

# ==[ Import ]============================================================
import tkinter as Tk
from tkinter import ttk
from dataSeries import DataSeries

# ==[ Class definition ]==================================================
class AntennaControlFrame(Tk.LabelFrame):

    # ==[ Constants ]=====================================================
    CONTROL_FRAME_BG_COLOR = "lightblue"

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
        self.configure(relief="solid", bd=1, background=AntennaControlFrame.CONTROL_FRAME_BG_COLOR)
        pass

    def create_widgets(self):
        # create ui components
        self.startPauseButton = ttk.Button(master=self, text="Start", command=self.startPauseButtonClicked)
        self.defaultPositionButton = ttk.Button(master=self, text="Back to default", command=self.defaultPositionButtonClicked)
        self.stopButton = ttk.Button(master=self, text="Stop", command=self.stopButtonClicked)
        # grid components
        self.startPauseButton.grid(row=0, column=0)
        self.defaultPositionButton.grid(row=0, column=1)
        self.stopButton.grid(row=1, column=0, columnspan=2, sticky="ew")
        pass

    def initialize_members(self):
        pass 

    def initialize_widgets(self):
        pass

    # --< Button actions >------------------------------------------------
    def startPauseButtonClicked(self):
        print("startPauseButtonClicked()")

        if (not (self.master.workingDataSeries is None)):
            MsgBox = Tk.messagebox.askquestion('Warning! Existing data! (。・・)ノ',
                                                'Are you sure you want to continue?\nThere is existing data loaded in the program\nand it will be overwritten and potentially lost\nif you continue.',icon = 'warning')
            if MsgBox == 'no':
                return
        
        self.master.workingDataSeries = self.master.toFillDataSeries
        self.master.fileHandlingSection.refresh_widgets()

        pass

    def stopButtonClicked(self):
        print("stopButtonClicked()")

        # Muss das? 
        # self.master.fileHandlingSection.refresh_widgets()
        pass

    def defaultPositionButtonClicked(self):
        print("defaultPositionButtonClicked()")

        # Muss das? 
        # TODO: Reset?
        # self.master.fileHandlingSection.refresh_widgets()

        pass