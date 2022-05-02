from dataSeries import DataSeries
from dataAquisitionApplication import SIMULATED_X_STEPS as penx
from dataAquisitionApplication import SIMULATED_Y_STEPS as penys

print(DataSeries.getEstimatedScanTimeInMinutes(penx, penys))