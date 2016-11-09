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

"""
Gastric data pacing
"""
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig68/exp7_A-H-256_pacing_recording_17s_period_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig68/exp6_A-H-256_pacing_recording_15s_period_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig68/exp5_A-H-256_pacing_recording_13s_period_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig68/exp4_A-H-256_pacing_recording_Elec_dat.mat'
data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig71/bdf/pig71_exp7_pcb_A_H_aydinStimbdf_Elec_data.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig51/pig51_exp10_3g3_E32_Elec_data.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/pacing/pig51/pig51_exp11_3g3_E32_Elec_data.mat'

"""
Gastric data normal
"""
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig68/exp3_A-H-256channels_recording_Elec_data.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig41/pig41exp2_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig37/pig37exp1_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig34/pig34exp1_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig32/pig32exp1_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig32/pig32exp2_Elec_dat.mat'
#data = '/media/hpc/codes/python-spider-projects/GuiPlotting/01092016_data/normal/pig32/pig32exp3_Elec_dat.mat'
"""
Cardiac data
"""
mat_contents = sio.loadmat(data)

cg.set_data_file_name((data.rsplit('/', 1)[1]))
cg.set_test_file_name(str(cg.loaded_data_file) + str('_test.arff'))
cg.set_training_file_name(str(cg.loaded_data_file) + str('_training.arff'))
cg.set_trained_file(str(cg.loaded_data_file) + str('_trained.dat'))

vals = np.array(mat_contents['bdfdat'])
#vals = np.array(mat_contents['mark_cardiac'])

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    gui = GuiWindowDocks()
    """
    Create data here and add to the curve
    """
    gui.setData(vals[0:12, 0:15001]/100, 10, 15000)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
