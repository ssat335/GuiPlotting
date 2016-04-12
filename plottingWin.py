#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI for training and plotting the activation times.
"""

from pyqtgraph.Qt import QtGui, QtCore
from GuiWindowDocks import GuiWindowDocks
import numpy as np
import scipy.io as sio

#mat_contents = sio.loadmat('data/exp3_A-H-256channels_recording_Elec_data_only')
mat_contents = sio.loadmat('data/exp7_A-H-256_pacing_recording_17s_period_Elec_data_only')
vals = np.array(mat_contents['bdfdat'])

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    gui = GuiWindowDocks()
    """
    Create data here and add to the curve
    """
    gui.setData(vals[33:65, 0:9001]/100, 32, 9000)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
