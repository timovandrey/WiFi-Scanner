# ========================================================================
# Title:        AntennaControlFrame
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  A frame to display all antenna controlling elements
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================

# ==[ System imports ]====================================================
import tkinter as Tk
from tkinter import ttk
from dataSeries import DataSeries
from time import sleep
import threading as t
import tkinter.messagebox as mb
# ==[ Custom imports ]====================================================
from antennaFiniteStateMachine import AntennaState
from antennaFiniteStateMachine import AntennaFiniteStateMachine
from log import LOG

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
        self.stopButton = ttk.Button(master=self, text="Stop", command=self.stopButtonClicked)
        self.sep1 = ttk.Separator(master=self)
        self.helpAboutButton = ttk.Button(master=self, text="Help / About", command=self.helpAboutButtonClicked)
        # pack components
        self.startPauseButton.pack(expand=True, fill=Tk.BOTH, anchor="c")
        self.stopButton.pack(expand=True, fill=Tk.BOTH, anchor="c")
        self.sep1.pack(expand=True, fill=Tk.BOTH, anchor="c")
        self.helpAboutButton.pack(expand=True, fill=Tk.BOTH, anchor="c")
        return

    def initialize_members(self):
        self.stateMachineThread = t.Thread(target=self.advanceStateMachine, daemon=True)
        self.pauseStateMachine = True
        self.stopStateMachine = True
        self.stateMachineStarted = False
        self.stateMachineProgressEnd = 0

        # self.debugCounter = 0
        return

    def initialize_widgets(self):
        self.updateStopButton()
        return

    # --< Button actions >------------------------------------------------
    def startPauseButtonClicked(self):
        # TODO: What to do when "finished"?
        
        self.evaluateStartPauseButtonFaces()
        self.updateStopButton()

        if not self.stateMachineStarted:

            # If the toFillDataSeries is none, it means there is no container to fill. 
            # So just take the values that are in the AntennaConfigurationFrame's entry fields already
            if self.master.toFillDataSeries is None:
                self.master.antennaStateSection.applyButtonClicked()

            if (not (self.master.workingDataSeries is None)):
                MsgBox = Tk.messagebox.askquestion('Warning! Existing data! (。・・)ノ',
                                                    'Are you sure you want to continue?\nThere is existing data loaded in the program\nand it will be overwritten and potentially lost\nif you continue.',icon = 'warning')
                if MsgBox == 'no':
                    return

            # Set working data series 
            self.master.workingDataSeries = self.master.toFillDataSeries
            self.master.fileHandlingSection.refresh_widgets()

            # set max progress of statemachine
            self.master.progressBarMaxVar.set(abs(self.master.workingDataSeries.stepsToScanPitch) * abs(self.master.workingDataSeries.stepsToScanYaw))
            self.master.antennaStateSection.progressBar['maximum'] = self.master.progressBarMaxVar.get()
            self.master.progressBarVar.set(0)

            # setup stateMachine
            self.stateMachine = AntennaFiniteStateMachine()
            self.stateMachine.IDataSeries = self.master.workingDataSeries
            self.stateMachine.IStartScan = True
        
            # setup stateMachine control variables.
            self.stateMachineStarted = True
            self.stopStateMachine = False
            self.pauseStateMachine = False
            # setup and start stateMachine thread
            self.stateMachineThread = t.Thread(target=self.advanceStateMachine, daemon=True)
            self.stateMachineThread.start()
        return

    def stopButtonClicked(self):
        self.stopStateMachine = True
        self.stateMachineStarted = False
        
        self.startPauseButton['text'] = "Start"
        self.updateStopButton()

        self.master.fileHandlingSection.refresh_widgets()

        # self.debugCounter = 0
        return

    def helpAboutButtonClicked(self):
        mb.showinfo(master=self.master, title="Help not available yet", message="No help available yet, sorry. (˘･_･˘)")
        return

    # --< Methods >-------------------------------------------------------
    def advanceStateMachine(self):
        while(not self.stopStateMachine):
            try:
                if not self.pauseStateMachine:
                    pass
                    #self.stateMachine.run()    ############################################################???
                    # self.debugCounter += 100

            except Exception as ekzepzioni:
                LOG("Couldn't advance stateMachine! Stopping machine...\n" + str(ekzepzioni.message))
                self.stopStateMachine = True
            finally:
                self.updateGuiComponents()
        return

    def evaluateStartPauseButtonFaces(self):
        if self.pauseStateMachine == True:
            self.pauseStateMachine = False
            self.startPauseButton['text'] = "Pause"
        elif self.pauseStateMachine == False:
            self.pauseStateMachine = True
            self.startPauseButton['text'] = 'Start'

    def updateStopButton(self):
        if not self.stopStateMachine:
            self.stopButton.state(['!disabled'])
        else:
            self.stopButton.state(['disabled'])
        return

    def updateGuiComponents(self):
        self.updateStopButton()

        # Dis-/Enable all components of file handling and settings while its running
        locking = self.stateMachineStarted and (not self.stopStateMachine)
        self.master.fileHandlingSection.changeLockState(locking)
        self.master.antennaConfigurationSection.changeLockState(locking)

        # Change progress bar
        # self.master.progressBarVar.set(self.debugCounter)       # set to stateMachine.IProgress
        self.master.progressBarVar.set(self.stateMachine.ICurrentProgress + 1) ############################################################???
        # Change color and text of state indicator
        self.master.antennaStateSection.update_progress_label() ############################################################???
        self.master.antennaStateSection.change_state_indicator(self.stateMachine.state) # set to stateMachine.(currentstate, welche var das auch immer sein mag...)

        

