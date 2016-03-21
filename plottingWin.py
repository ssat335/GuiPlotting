#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI for training and plotting the activation times.
"""

from pyqtgraph.Qt import QtGui, QtCore
from GuiWindowTraining import GuiWindowTraining
import numpy as np
import scipy.io as sio

mat_contents = sio.loadmat('exp7_A-H-256_pacing_recording_17s_period_Elec_data_only')
vals = np.array(mat_contents['bdfdat']);

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    junk = GuiWindowTraining()
    """
    Create data here and add to the curve
    """
    print vals.shape
    data = vals
    junk.setData(data[0:256, 0:9001]/100, 256, 9000)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
