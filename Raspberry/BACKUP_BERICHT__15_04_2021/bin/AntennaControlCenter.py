# ====================================================================
# Title:        AntennaControlCenter
# Author:       Jonas Buuck, Timo Vandrey
# Date:         27.03.2021
# Description:  Start the main (GUI) application to control the antenna
#               (mainApplication.py -> MainApplication(...))
#
# --< LOG >-----
# 27.03.2021 - File created by Timo
# ========================================================================
#
# ==[ System imports ]====================================================
import tkinter as Tk
from tkinter import ttk
# ==[ Custom imports ]====================================================
from mainApplication import *

# ==[ Main application start configuration ]==============================
def create_application_root():
    root = Tk.Tk()
    root.resizable(width=False, height=False)
    root.title("Antenna Control Center")
    return root

# ==[ Start of main application ]=========================================
if __name__ == "__main__":
    application = MainApplication(master=create_application_root())
    application.mainloop()