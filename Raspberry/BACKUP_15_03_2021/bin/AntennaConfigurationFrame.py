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
from systemAttributes import *
from dataSeries import DataSeries
import tkinter.messagebox as mb
from datetime import datetime

# ==[ Class definition ]==================================================
class AntennaConfigurationFrame(Tk.LabelFrame):

    # ==[ Constants ]=====================================================
    CONFIG_FRAME_BG_COLOR = "lightgreen"

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
        pitchConstraintsText = ("[" + str(PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE) + "," + str(PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE) + "]")
        self.pitchConstraintsLabel = ttk.Label(master=self, text=pitchConstraintsText, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 7 normal")

        self.pitchFromLabel = ttk.Label(master=self, text="From", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchToLabel = ttk.Label(master=self, text="° to",background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchFromEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchToEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.pitchDegLabel = ttk.Label(master=self, text="°", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)

        # yaw
        self.yawLabel = ttk.Label(master=self, text="Yaw:", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 9 underline")
        yawConstraintsText = ("[" + str(YAW_MOTOR_LOWER_LIMIT_IN_DEGREE) + "," + str(YAW_MOTOR_UPPER_LIMIT_IN_DEGREE) + "]")
        self.yawConstraintsLabel = ttk.Label(master=self, text=yawConstraintsText, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 7 normal")

        self.yawToScanLabel = ttk.Label(master=self, text="Scan arc:", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.yawToScanEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.yawDegLabel = ttk.Label(master=self, text="°", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)

        # name
        self.nameLabel = ttk.Label(master=self, text="Name of data series:", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, font="helvetica 9 underline")
        self.nameLabelEntryField = ttk.Entry(master=self, text="", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)

        SPINBOX_WIDTH = 10
        # stepsize pitch  
        self.stepsizePitchLabel = ttk.Label(master=self, text="Step size (Pitch):", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.stepsizePitchMultiplierSpinbox = ttk.Spinbox(master=self, from_=1, to=5, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, width=SPINBOX_WIDTH)
        self.stepsizePitchConstLabel = ttk.Label(master=self, text=("* " + str(PITCH_MOTOR_STEP_SIZE_IN_DEGREE) + "°"), background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR) # TODO: Replace with SysAttr
        
        # stepsize yaw     
        self.stepsizeYawLabel = ttk.Label(master=self, text="Step size (Yaw):", background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR)
        self.stepsizeYawMultiplierSpinbox = ttk.Spinbox(master=self, from_=1, to=5, background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR, width=SPINBOX_WIDTH)
        self.stepsizeYawConstLabel = ttk.Label(master=self, text=("* " + str(YAW_MOTOR_STEP_SIZE_IN_DEGREE) + "°"), background=AntennaConfigurationFrame.CONFIG_FRAME_BG_COLOR) # TODO: Replace with SysAttr

        # apply, reset
        self.resetButton = ttk.Button(master=self, text="Reset", command=self.resetButtonClicked)
        self.applyButton = ttk.Button(master=self, text="Apply", command=self.applyButtonClicked)

        # --< Grid all GUI components >-----------------------------------
        # pitch
        self.pitchLabel.grid(row=0, column=0, sticky="w")
        self.pitchConstraintsLabel.grid(row=0, column=1, sticky="ew", columnspan=4)
        self.pitchFromLabel.grid(row=1, column=0, sticky="w")
        self.pitchFromEntryField.grid(row=1, column=1, padx=4)
        self.pitchToLabel.grid(row=1, column=2, sticky="w")
        self.pitchToEntryField.grid(row=1, column=3, padx=4)
        self.pitchDegLabel.grid(row=1, column=4, ipadx=2)

        # seperator 1 ---
        self.seperator1.grid(row=2, column=0, columnspan=5, sticky="ew", pady=4)

        # yaw
        self.yawLabel.grid(row=3, column=0, sticky="w")
        self.yawConstraintsLabel.grid(row=3, column=1, sticky="ew", columnspan=4)
        self.yawToScanLabel.grid(row=4, column=0, sticky="w")
        self.yawToScanEntryField.grid(row=4, column=1, padx=4)
        self.yawDegLabel.grid(row=4, column=2, sticky="w")

        self.nameLabel.grid(row=3, column=3, columnspan=2, sticky="w")
        self.nameLabelEntryField.grid(row=4, column=3, columnspan=2, sticky="ew", padx=4)

        # seperator 2 ---
        self.seperator2.grid(row=5, column=0, columnspan=5, sticky="ew", pady=4)

        # stepsize pitch
        self.stepsizePitchLabel.grid(row=6, column=0, sticky="ew")
        self.stepsizePitchMultiplierSpinbox.grid(row=6, column=1, sticky="e") 
        self.stepsizePitchConstLabel.grid(row=6, column=2, ipadx=2)

        # seperator 3 ---
        self.seperator3.grid(row=7, column=0, columnspan=5, sticky="ew", pady=4)

        # stepsize yaw     
        self.stepsizeYawLabel.grid(row=8, column=0, sticky="ew")
        self.stepsizeYawMultiplierSpinbox.grid(row=8, column=1, sticky="e") 
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

        self.pitchFromEntryField.delete(0, "end")
        self.pitchFromEntryField.insert(0, PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE)
        self.pitchToEntryField.delete(0, "end")
        self.pitchToEntryField.insert(0, PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE)

        self.yawToScanEntryField.delete(0, "end")
        self.yawToScanEntryField.insert(0, YAW_MOTOR_LOWER_LIMIT_IN_DEGREE)

        self.stepsizePitchMultiplierSpinbox.delete(0,"end")
        self.stepsizePitchMultiplierSpinbox.insert(0, PITCH_MOTOR_MIN_STEP_MULIPLIER)
        self.stepsizeYawMultiplierSpinbox.delete(0,"end")
        self.stepsizeYawMultiplierSpinbox.insert(0, YAW_MOTOR_MIN_STEP_MULIPLIER)

        self.nameLabelEntryField.delete(0, "end")
        self.nameLabelEntryField.insert(0, "[None]")

        pass

    # --< Generic initializer >-------------------------------------------
    # ...

    # --< Button actions >------------------------------------------------
    def resetButtonClicked(self):
        print("resetButtonClicked()")
        self.initialize_widgets()
        self.master.toFillDataSeries = None
        pass

    def applyButtonClicked(self):
        print("applyButtonClicked()")

        # --< Range limit checks >----------------------------------------
        # Check lower pitch limit
        tmp_pitch_motor_lower_limit_in_degree = int(float(self.pitchFromEntryField.get()))
        if (tmp_pitch_motor_lower_limit_in_degree < PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE):
            pitch_lower_limit_in_degree_message = "Lower end of the pitch interval is invalid. Please make sure it is in the allowed interval."
            mb.showerror(master=self.master, 
                        title="Invalid value", 
                        message=pitch_lower_limit_in_degree_message
                        )
            return

        # Check upper pitch limit
        tmp_pitch_motor_upper_limit_in_degree = int(float(self.pitchToEntryField.get()))
        if (tmp_pitch_motor_upper_limit_in_degree > PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE):
            pitch_upper_limit_in_degree_message = "Upper end of the pitch interval is invalid. Please make sure it is in the allowed interval."
            mb.showerror(master=self.master, 
                        title="Invalid value", 
                        message=pitch_upper_limit_in_degree_message
                        )
            return
        
        # Check yaw range
        tmp_yaw_to_scan_in_degree = int(float(self.yawToScanEntryField.get()))
        if ((tmp_yaw_to_scan_in_degree > YAW_MOTOR_UPPER_LIMIT_IN_DEGREE) or 
            (tmp_yaw_to_scan_in_degree < YAW_MOTOR_LOWER_LIMIT_IN_DEGREE)):
            tmp_yaw_to_scan_in_degree_message = "Yaw range to scan invalid. Please make sure the range of the yaw is in the allowed interval."
            mb.showerror(master=self.master, 
                        title="Invalid value", 
                        message=tmp_yaw_to_scan_in_degree_message
                        )
            return        

        # --< Step multiplier check >-------------------------------------
        # Check pitch motor step multiplier
        tmp_pitch_motor_step_multipler = int(float(self.stepsizePitchMultiplierSpinbox.get()))
        if ((tmp_pitch_motor_step_multipler > PITCH_MOTOR_MAX_STEP_MULIPLIER) or 
            (tmp_pitch_motor_step_multipler < PITCH_MOTOR_MIN_STEP_MULIPLIER)):
            tmp_pitch_motor_step_multipler_message = "Pitch step multiplier invalid.\nPlease make sure the multiplier is a whole number (integer) and in the allowed interval."
            mb.showerror(master=self.master, 
                        title="Invalid value", 
                        message=tmp_pitch_motor_step_multipler_message
                        )
            return       
        
        # Check yaw motor step multiplier
        tmp_yaw_motor_step_multiplier = int(float(self.stepsizeYawMultiplierSpinbox.get()))
        if ((tmp_yaw_motor_step_multiplier > YAW_MOTOR_MAX_STEP_MULIPLIER) or 
            (tmp_yaw_motor_step_multiplier < YAW_MOTOR_MIN_STEP_MULIPLIER)):
            tmp_yaw_motor_step_multiplier_message = "Yaw step multiplier invalid.\nPlease make sure the multiplier is a whole number (integer) and in the allowed interval."
            mb.showerror(master=self.master, 
                        title="Invalid value", 
                        message=tmp_yaw_motor_step_multiplier_message
                        )
            return       
        
        # Get dataseries name and create entry field
        tmp_dataseries_name = self.nameLabelEntryField.get()
        if ((tmp_dataseries_name == "[None]") or (tmp_dataseries_name == "")):
            tmp_dataseries_name = "DataSeries_" + datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

        # Create DataSeries to work with
        self.master.toFillDataSeries = DataSeries(tmp_dataseries_name,
                                                    tmp_pitch_motor_lower_limit_in_degree, 
                                                    tmp_pitch_motor_upper_limit_in_degree,
                                                    tmp_yaw_to_scan_in_degree,
                                                    tmp_pitch_motor_step_multipler,
                                                    tmp_yaw_motor_step_multiplier)

        # Give feedback "settings applied" or something
        mb.showinfo(master=self.master, 
                        title="Settings applied successfully", 
                        message="Settings have been successfully applied.\n(o゜▽゜)o☆"
                        )

        pass

    # --< Methods >-------------------------------------------------------
    # ...
