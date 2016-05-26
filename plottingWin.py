#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Author: Shameer Sathar
    Description: GUI for training and plotting the activation times.
"""

from pyqtgraph.Qt import QtGui, QtCore
from GuiWindowDocks import GuiWindowDocks
import numpy as np
import scipy.io as sio
import config_global as cg

#data = 'data/exp3_A-H-256channels_recording_Elec_data_only'
data = 'data/exp7_A-H-256_pacing_recording_17s_period_Elec_data_only'
mat_contents = sio.loadmat(data)

cg.set_data_file_name((data.rsplit('/', 1)[1]))
cg.set_test_file_name(str(cg.loaded_data_file) + str('_test.arff'))
cg.set_training_file_name(str(cg.loaded_data_file) + str('_training.arff'))

vals = np.array(mat_contents['bdfdat'])
print len(vals[1, :])
# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    gui = GuiWindowDocks()
    """
    Create data here and add to the curve
    """
    gui.setData(vals[44:52, 0:9001]/100,  8, 9000)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
