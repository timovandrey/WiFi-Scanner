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
from time import *
# ==[ Custom imports ]====================================================
from indicatorLight import IndicatorLight
from antennaFiniteStateMachine import *

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
        
        self.stateIndicatorLight = IndicatorLight(master=self, bg=AntennaStateFrame.STATE_FRAME_BG_COLOR, indicatorColor="gray60")
        self.stateIndicatorLabel = ttk.Label(master=self, background=AntennaStateFrame.STATE_FRAME_BG_COLOR, text="No information available yet")
        
        self.progressLabel = ttk.Label(master=self, background=AntennaStateFrame.STATE_FRAME_BG_COLOR, text="0 / 0")

        self.progressBarLabel = ttk.Label(master=self, background=AntennaStateFrame.STATE_FRAME_BG_COLOR, text="Progress:", font=("helvetica 9 underline"))
        self.progressBar = ttk.Progressbar(master=self, 
                                            orient="horizontal", 
                                            length=(self.winfo_width() - 2), 
                                            mode="determinate", 
                                            variable=self.master.progressBarVar
                                            )
        
        # grid components
        self.stateIndicatorLight.grid(row=0, column=0)
        self.stateIndicatorLabel.grid(row=0, column=1, columnspan=2, padx=2)
        
        self.progressBarLabel.grid(row=1, column=0, columnspan=3, sticky="w")
        self.progressLabel.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.progressBar.grid(row=3, column=0, columnspan=3, sticky="ew", padx=4, pady=4)

        pass

    def initialize_members(self):
        self.stateIndicatorText = "Waiting..."
        self.stateIndicatorTextNext = "Waiting..."
        pass 

    def initialize_widgets(self):
        # initialize widget states
        pass

    # --< Methods >-------------------------------------------------------
    def update_progress_label(self):
        eta = self.master.EtaVarInSec.get()
        eta_string = strftime("%H:%M:%S", gmtime(eta))
        txt = (str(self.master.progressBarVar.get()) + " / " + str(self.master.progressBarMaxVar.get()) + " ( ~ " + eta_string + " left)")
        self.progressLabel['text'] = txt

    def change_state_indicator(self):
        if(not (self.master.antennaControlSection.stateMachine == None)):

            self.stateIndicatorText = self.stateIndicatorTextNext
            self.stateIndicatorLabel['text'] = self.stateIndicatorText
            self.stateIndicatorTextNext = self.master.antennaControlSection.stateMachine.IStatusMessage

            if(self.master.antennaControlSection.stateMachine.IStatusMessage == AntennaFiniteStateMachine.STATUS_MESSAGE_IDLE):
                self.stateIndicatorLight.changeColor("red")
            elif(self.master.antennaControlSection.stateMachine.IStatusMessage == AntennaFiniteStateMachine.STATUS_MESSAGE_COLLECTING_DATA):
                self.stateIndicatorLight.changeColor("DarkOliveGreen1")    
            elif(self.master.antennaControlSection.stateMachine.IStatusMessage == AntennaFiniteStateMachine.STATUS_MESSAGE_MOVING_MOTORS):
                self.stateIndicatorLight.changeColor("DarkOliveGreen3")
            elif(self.master.antennaControlSection.stateMachine.IStatusMessage == AntennaFiniteStateMachine.STATUS_MESSAGE_IDLE):
                self.stateIndicatorLight.changeColor("blue")                                