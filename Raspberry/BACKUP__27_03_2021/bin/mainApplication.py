# ====================================================================
# Title:        MainApplication
# Author:       Jonas Buuck, Timo Vandrey
# Date:         06.03.2021
# Description:  Main application to control antenna and dat aqcuisition
#
# --< LOG >-----
# 06.03.2021 -> class created by Timo
# ========================================================================
#
# ==[ System imports ]====================================================
import tkinter as Tk
from tkinter import ttk
# ==[ Custom imports ]====================================================
import fileHandlingFrame as fhf
import antennaConfigurationFrame as aConfig
import antennaControlFrame as aControl
import antennaStateFrame as aState

# ==[ Class definition ]==================================================
class MainApplication(Tk.Frame):

    # ==[ Constants ]=====================================================
    PICKLE_FILE_EXTENSION = "a24"   # TODO: Move to DataSeries

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, master, *args, **kwargs):    
        Tk.Frame.__init__(self, master, *args, **kwargs)
        self.configure_main_style()
        self.configure_mainframe()
        self.initialize_members()
        self.create_widgets()
        pass

    # Configure the overarching style of application
    def configure_main_style(self):
        # s = ttk.Style("My.TFrame", =("Helvetiva", 12))
        pass

    # Configure mainframe
    def configure_mainframe(self):
        self.pack()
        pass

    # GUI creation
    def create_widgets(self):
        self.create_section_fileHandling()
        self.create_section_antennaConfiguration()
        self.create_section_antennaControl()
        self.create_sectiom_antennaState()
        pass

    # --< Individual section creation >-----------------------------------
    def create_section_fileHandling(self):
        self.fileHandlingSection = fhf.FileHandlingFrame(container=self, text="File handling")
        # self.fileHandlingSection.grid(row=0, column=0, sticky="nw")
        self.fileHandlingSection.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        pass
    def create_section_antennaConfiguration(self):
        self.antennaConfigurationSection = aConfig.AntennaConfigurationFrame(container=self, text="Antenna configuration")
        # self.antennaConfigurationSection.grid(row=0, column=1, sticky="ne")
        self.antennaConfigurationSection.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        pass
    def create_section_antennaControl(self):
        self.antennaControlSection = aControl.AntennaControlFrame(container=self, text="Antenna control")
        # self.antennaControlSection.grid(row=1, column=1, sticky="se")
        self.antennaControlSection.pack(side="bottom", fill="both", expand=True, padx=2, pady=2)
        pass
    def create_sectiom_antennaState(self):
        self.antennaStateSection = aState.AntennaStateFrame(container=self, text="Antenna state")
        # self.antennaStateSection.grid(row=1, column=0, sticky="sw")
        self.antennaStateSection.pack(side="right", fill="both", expand=True, padx=2, pady=2)
        pass

    # --< Member initialization >-----------------------------------------
    def initialize_members(self):
        self.workingFile = ""
        self.workingDataSeries = None
        self.toFillDataSeries = None
        self.antennaConfig = None
        self.progressBarVar = Tk.IntVar()
        self.progressBarVar.set(0)
        self.progressBarMaxVar = Tk.IntVar()
        self.progressBarMaxVar.set(0)

        #self.heatmapConfig
        pass

    # --< Controls actions >----------------------------------------------
    # ... 

# ==[ Main application start configuration ]==============================
def create_application_root():
    root = Tk.Tk()
    # -- Configuring root frame -----
    # root.state('zoomed')
    root.resizable(width=False, height=False)
    root.title("Antenna Control Center")
    # -- configuration end ----------
    return root

# ==[ Start of main application ]=========================================
if __name__ == "__main__":
    application = MainApplication(master=create_application_root())
    application.mainloop()
    pass

