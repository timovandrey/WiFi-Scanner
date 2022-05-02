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

# ==[ Class definition ]==================================================
class AntennaConfigurationFrame(Tk.LabelFrame):

    # ==[ Constants ]=====================================================
    CONFIG_FRAME_BG_COLOR = "lightgreen"
    iStepSizeYawDg = 0.36   
    iStepSizePitchDg = 0.36   
    iMaxYawPossible = 180
    iMinYawPossible = 0
    iMaxPitchPossible = +45
    iMinPitchPossible = -45

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, container, *args, **kwargs):
        Tk.LabelFrame.__init__(self, container, *args, **kwargs)
        self.configure_self()
        self.create_widgets()
        self.initialize_members()
        self.initialize_widgets()

    def configure_self(self):
        self.configure(relief="solid", bd=1, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.grid_columnconfigure(index=(0, 2, 4), weight=1)
        self.grid_columnconfigure(index=(1, 3), weight=2)
        pass

    def create_widgets(self):
        # --< Create GUI components >-------------------------------------
        self.seperator1 = ttk.Separator(self, orient="horizontal")
        self.seperator2 = ttk.Separator(self, orient="horizontal")
        self.seperator3 = ttk.Separator(self, orient="horizontal")
        self.seperator4 = ttk.Separator(self, orient="horizontal")

        # pitch
        self.pitchLabel = ttk.Label(master=self, text="Pitch:", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 9 underline")
        pitchConstraintsText = ("[" + str(AntennaConfigurationFrame.iMinPitchPossible) + "," + str(AntennaConfigurationFrame.iMaxPitchPossible) + "]")
        self.pitchConstraintsLabel = ttk.Label(master=self, text=pitchConstraintsText, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 7 normal")

        self.pitchFromLabel = ttk.Label(master=self, text="From", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchToLabel = ttk.Label(master=self, text="° to",background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchFromEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchToEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchDegLabel = ttk.Label(master=self, text="°", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)

        # yaw
        self.yawLabel = ttk.Label(master=self, text="Yaw:", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 9 underline")
        yawConstraintsText = ("[" + str(AntennaConfigurationFrame.iMinYawPossible) + "," + str(AntennaConfigurationFrame.iMaxYawPossible) + "]")
        self.yawConstraintsLabel = ttk.Label(master=self, text=yawConstraintsText, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 7 normal")

        self.yawFromLabel = ttk.Label(master=self, text="From", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.yawToLabel = ttk.Label(master=self, text="° to", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.yawFromEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.yawToEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.yawDegLabel = ttk.Label(master=self, text="°", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)

        # stepsize pitch    
        self.stepsizePitchLabel = ttk.Label(master=self, text="Step size (Pitch):", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.stepsizePitchMultiplierEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.stepsizePitchConstLabel = ttk.Label(master=self, text=("* " + str(AntennaConfigurationFrame.iStepSizePitchDg) + "°"), background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR) # TODO: Replace with SysAttr
        
        # stepsize yaw     
        self.stepsizeYawLabel = ttk.Label(master=self, text="Step size (Yaw):", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.stepsizeYawMultiplierEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)        
        self.stepsizeYawConstLabel = ttk.Label(master=self, text=("* " + str(AntennaConfigurationFrame.iStepSizeYawDg) + "°"), background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR) # TODO: Replace with SysAttr

        # apply, reset
        self.resetButton = ttk.Button(master=self, text="Reset", command=self.resetButtonClicked)
        self.applyButton = ttk.Button(master=self, text="Apply", command=self.applyButtonClicked)

        # --< Grid all GUI components >-----------------------------------
        # pitch
        self.pitchLabel.grid(row=0, column=0, sticky="w")
        self.pitchConstraintsLabel.grid(row=0, column=1, sticky="ew", columnspan=4)
        self.pitchFromLabel.grid(row=1, column=0, sticky="w")
        self.pitchFromEntryField.grid(row=1, column=1, padx=4)
        self.pitchToLabel.grid(row=1, column=2)
        self.pitchToEntryField.grid(row=1, column=3, padx=4)
        self.pitchDegLabel.grid(row=1, column=4, ipadx=2)

        # seperator 1 ---
        self.seperator1.grid(row=2, column=0, columnspan=5, sticky="ew", pady=4)

        # yaw
        self.yawLabel.grid(row=3, column=0, sticky="w")
        self.yawConstraintsLabel.grid(row=3, column=1, sticky="ew", columnspan=4)
        self.yawFromLabel.grid(row=4, column=0, sticky="w")
        self.yawFromEntryField.grid(row=4, column=1, padx=4)
        self.yawToLabel.grid(row=4, column=2)
        self.yawToEntryField.grid(row=4, column=3, padx=4)
        self.yawDegLabel.grid(row=4, column=4, ipadx=2)

        # seperator 2 ---
        self.seperator2.grid(row=5, column=0, columnspan=5, sticky="ew", pady=4)

        # stepsize pitch
        self.stepsizePitchLabel.grid(row=6, column=0, sticky="ew")
        self.stepsizePitchMultiplierEntryField.grid(row=6, column=1) 
        self.stepsizePitchConstLabel.grid(row=6, column=2, ipadx=2)

        # seperator 3 ---
        self.seperator3.grid(row=7, column=0, columnspan=5, sticky="ew", pady=4)

        # stepsize yaw     
        self.stepsizeYawLabel.grid(row=8, column=0, sticky="ew")
        self.stepsizeYawMultiplierEntryField.grid(row=8, column=1) 
        self.stepsizeYawConstLabel.grid(row=8, column=2, ipadx=2)

        # seperator 4 ---
        self.seperator4.grid(row=9, column=0, columnspan=5, sticky="ew", pady=4)

        # buttons (apply, reset)
        self.resetButton.grid(row=10, column=0, columnspan=2, sticky="ew")
        self.applyButton.grid(row=10, column=2, columnspan=4, sticky="ew")

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