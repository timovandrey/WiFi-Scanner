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
import sys
import os
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# ==[ Custom imports ]====================================================
# import MainApplication as main
from dataSeries import DataSeries
from systemAttributes import *

# ==[ Class definition ]==================================================
class Heatmapper:

    # ==[ Constants ]=====================================================
    # ...

    # --< Initialization >------------------------------------------------
    # Constructor
    def __init__(self, master, dataSeries, hm_config, *args, **kwargs):
        self.workingDataSeries = dataSeries
        self.master = master
        self.hm_config = hm_config
        self.configure_self()
        self.initialize_members()
        pass

    def configure_self(self):
        pass

    def initialize_members(self):
        pass

    def create(self):


        # tmpYawSteps = (YAW_MOTOR_UPPER_LIMIT_IN_STEPS - YAW_MOTOR_LOWER_LIMIT_IN_STEPS)
        # tmpPitchSteps = (PITCH_MOTOR_UPPER_LIMIT_IN_STEPS - PITCH_MOTOR_LOWER_LIMIT_IN_STEPS)

        # ATTRIBUTES OF HEATMAP -------------------------------------
        cbar_kws_var = {'label': 'Signal strength (in dBm)'}
        # END OF ATTRIBUTES -----------------------------------------

        # Check how to get the index of the selected network
        networkIndex = self.workingDataSeries.networks.index(self.hm_config.selectedNetwork)
        # TODO: CONT here: Error: "The element is not in the list" -> \x00 is in the list as a value, filter somehow?

        data = self.workingDataSeries.networks[networkIndex].dataPoints
        try:
            hm = sb.heatmap(data, cmap="YlOrBr", cbar_kws=cbar_kws_var)
            plt.title(self.hm_config.selectedNetwork)
            plt.xlabel("Yaw (in °)")
            plt.ylabel("Pitch (in °)")
            plt.show()
        except Exception:
            print("heatmap failure")
            sys.exit()

        pass

    @staticmethod
    def showExamplePlot():
        data = [[1,0,0,0],[1,0,4.5,0],[1,0,0,0],[1,0,0,0]]
        hm = sb.heatmap(data)
        plt.show()
        pass

    @staticmethod
    def test():
        cbar_kws_var = {'label': 'Signal strength (in dBm)'}
        # cmap_var = "YlOrBr"
        cmap_var = "mako"

        # TODO: Change aspect ratio heatmap
        # TODO: Fix axis label ticks (make them beautiful)

        data = np.random.rand(90, 360)
        
        yTicks = Heatmapper.createTicks(data, num_ticks=int(len(data)/5))
        xTicks = Heatmapper.createTicks(data[0], num_ticks=int(len(data[0])/10))
        yTickLabels = Heatmapper.createTickLabels(data, yTicks)
        xTickLabels = Heatmapper.createTickLabels(data[0], xTicks)

        try:
            hm = sb.heatmap(data, cmap=cmap_var, cbar_kws=cbar_kws_var, yticklabels=yTickLabels, xticklabels=xTickLabels)
            hm.set_yticks(yTicks)
            hm.set_xticks(xTicks)

            plt.title("test()")
            plt.xlabel("Yaw (in °)")
            plt.ylabel("Pitch (in °)")
            
            fig = plt.gcf()

            plt.show()
        except Exception as ex:
            print("heatmap failure:\n{0}".format(ex))
            sys.exit()

    @staticmethod
    def createTicks(_list, num_ticks):
        ticks = np.linspace(0, len(_list) - 1, num_ticks, dtype=np.int64)
        return ticks

    @staticmethod
    def createTickLabels(_list, ticks_list):
        ticklabels = [_list[idx] for idx in ticks_list]
        return ticklabels

if __name__ == "__main__":
    Heatmapper.test()
    pass

        