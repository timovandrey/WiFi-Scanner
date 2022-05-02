# ========================================================================
# Title:        AntennaStatusIndicator
# Author:       Jonas Buuck, Timo Vandrey
# Date:         07.03.2021
# Description:  Mini custom widget with "led-light" and text
#
# --< LOG >-----
# 07.03.2021 -> class created by Timo
# ========================================================================

# ==[ Import ]============================================================
import tkinter as Tk
from tkinter import ttk

# ==[ Constants ]=========================================================
SELF_SIZE_XY = 20
REQ_SIZE_XY = 14

# ==[ Class definition ]==================================================
class IndicatorLight(Tk.Canvas):
    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, indicatorColor, *args, **kwargs):
        Tk.Canvas.__init__(self, *args, **kwargs)
        self.indicatorColor = indicatorColor
        self.configure_self()
        self.create_widgets()
        self.initialize_members()
        self.initialize_widgets()

    def configure_self(self):
        self.configure(height=SELF_SIZE_XY, width=SELF_SIZE_XY, bd=-2, relief=None)
        self.grid()
        pass

    def create_widgets(self):
        self.redraw_light(self.indicatorColor)
        pass

    def initialize_members(self):
        pass

    def initialize_widgets(self):
        pass

    def redraw_light(self, color):
        tmp_pos = ((SELF_SIZE_XY - REQ_SIZE_XY)/2.0)
        # tmp_pos = ((SELF_SIZE_XY - REQ_SIZE_XY))
        self.oval_light_id = self.create_oval(tmp_pos, tmp_pos, 
                            (self.winfo_reqwidth() - tmp_pos),
                            (self.winfo_reqheight() - tmp_pos), 
                            fill=(color), 
                            outline=("black"), 
                            state="disabled")
        pass

    # --< Use this to change the color of the indicator!!! >--------------
    def changeColor(self, newColor):
        self.delete(self.oval_light_id)
        self.redraw_light(newColor)        
        pass
