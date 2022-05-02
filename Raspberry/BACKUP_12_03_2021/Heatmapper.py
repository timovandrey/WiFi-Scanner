# ========================================================================
# Title:        Heatmapper
# Author:       Jonas Buuck, Timo Vandrey
# Date:         09.03.2021
# Description:  A class to create heatmaps
#
# --< LOG >-----
# 09.03.2021 -> class created by Timo
# ========================================================================

# ==[ System imports ]====================================================
import os
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# ==[ Custom imports ]====================================================
import MainApplication as main
from dataSeries import DataSeries

# ==[ Class definition ]==================================================
class Heatmapper:

    # ==[ Constants ]=====================================================
    # ...

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, dataSeries, hm_config, *args, **kwargs):
        self.workingDataSeries = dataSeries

        self.configure_self()
        self.initialize_members()
        pass

    def configure_self(self):
        pass

    def initialize_members(self):
        pass

    def test(self):

        data = self.workingDataSeries.networks[0].dataPoints
        hm = sb.heatmap(data)
        plt.show()

        pass

    @staticmethod
    def showExamplePlot():
        data = [[1,0,0,0],[1,0,4.5,0],[1,0,0,0],[1,0,0,0]]
        hm = sb.heatmap(data)
        plt.show()
        pass