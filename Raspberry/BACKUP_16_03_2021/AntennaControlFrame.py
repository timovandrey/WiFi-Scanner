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
from time import sleep
# from antennaFiniteStateMachine import AntennaFiniteStateMachine 
import threading as t
from Heatmapper import Heatmapper

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
        self.stateMachineThread = t.Thread(target=self.advanceStateMachine, daemon=True)
        self.pauseStateMachine = True
        self.stopStateMachine = True
        self.stateMachineStarted = False

        self.debugCounter = 0
        pass

    def create_widgets(self):
        # create ui components
        self.startPauseButton = ttk.Button(master=self, text="Start", command=self.startPauseButtonClicked)
        self.stopButton = ttk.Button(master=self, text="Stop", command=self.stopButtonClicked)
        self.sep1 = ttk.Separator(master=self)
        self.helpAboutButton = ttk.Button(master=self, text="Help / About", command=self.helpAboutButtonClicked)
        # grid components
        # self.startPauseButton.grid(row=0, column=0, columnspan=1, sticky="ew")
        # self.stopButton.grid(row=1, column=0, columnspan=2, sticky="ew")
        # self.sep1.grid(row=2, column=0, columnspan=2, sticky="ew")
        # self.helpAboutButton.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.startPauseButton.pack(expand=True, fill=Tk.BOTH, anchor="c")
        self.stopButton.pack(expand=True, fill=Tk.BOTH, anchor="c")
        self.sep1.pack(expand=True, fill=Tk.BOTH, anchor="c")
        self.helpAboutButton.pack(expand=True, fill=Tk.BOTH, anchor="c")

        pass

    def initialize_members(self):
        pass 

    def initialize_widgets(self):
        self.updateStopButton()
        pass

    # --< Button actions >------------------------------------------------
    def startPauseButtonClicked(self):
        print("startPauseButtonClicked()")

        self.evaluateStartPauseButtonFaces()
        self.updateStopButton()

        if not self.stateMachineStarted:
            print("starting state machine thread")

            if (not (self.master.workingDataSeries is None)):
                MsgBox = Tk.messagebox.askquestion('Warning! Existing data! (。・・)ノ',
                                                    'Are you sure you want to continue?\nThere is existing data loaded in the program\nand it will be overwritten and potentially lost\nif you continue.',icon = 'warning')
                if MsgBox == 'no':
                    return


            self.master.workingDataSeries = self.master.toFillDataSeries
            self.master.fileHandlingSection.refresh_widgets()

            # self.stateMachine = AntennaFiniteStateMachine()
            # self.stateMachine.IDataSeries = self.master.workingDataSeries
            # self.stateMachine.IStartScan = True
        
            self.stateMachineStarted = True
            self.stopStateMachine = False
            self.pauseStateMachine = False
            self.stateMachineThread = t.Thread(target=self.advanceStateMachine, daemon=True)
            self.stateMachineThread.start()

        pass

    def stopButtonClicked(self):
        print("stopButtonClicked()")

        self.stopStateMachine = True
        self.stateMachineStarted = False
        
        self.startPauseButton['text'] = "Start"
        self.updateStopButton()


        self.debugCounter = 0

        # TODO: Delete data?

        # Muss das? 
        # self.master.fileHandlingSection.refresh_widgets()
        pass

    def helpAboutButtonClicked(self):
        print("helpAboutButtonClicked()")        
        Heatmapper.test()
        pass

    # --< Methods >-------------------------------------------------------
    def advanceStateMachine(self):
        print("advanceStateMachine()")

        while(not self.stopStateMachine):
            try:
                if self.pauseStateMachine:
                    print(f"State machine paused ({self.debugCounter})")
                else:
                    print(f"State machine running ({self.debugCounter})")
                    #self.stateMachine.run()
                self.debugCounter += 1
                sleep(0.5)
            except Exception as excep:
                print("advanceStateMachine() failed!\n" + excep.message)
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
        print("self.pauseStateMachine is now:\t" + str(self.pauseStateMachine))

    # TODO: When state machine is finished, self.master.workingDataSeries = self.master.toFillDataSeries !!!

    def updateStopButton(self):
        if not self.stopStateMachine:
            self.stopButton.state(['!disabled'])
        else:
            self.stopButton.state(['disabled'])
        return

    def updateGuiComponents(self):
        print("updateGuiComponents()")
        self.updateStopButton()

        # Dis-/Enable all components of file handling and settings while its running
        locking = self.stateMachineStarted and (not self.stopStateMachine)
        self.master.fileHandlingSection.changeLockState(locking)
        self.master.antennaConfigurationSection.changeLockState(locking)

        # TODO: Change color and text of state indicator
        # TODO: Change progress bar
        

