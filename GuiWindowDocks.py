""" Standard imports """

"""
    Author: Shameer Sathar
    Description: Provide Gui Interface.
"""

import numpy as np
from multiprocessing import Process
# Main GUI support
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import *
import cPickle as pickle

# Locally-developed modules
from TrainingData import TrainingData
from ARFFcsvReader import ARFFcsvReader
from WekaInterface import WekaInterface
from FeatureAnalyser import FeatureAnalyser
from ClassifySlowWavesScikit import ClassifySlowWavesScikit
import config_global as cg

class GuiWindowDocks:
    def __init__(self):
        """
        Initialise the properties of the GUI. This part of the code sets the docks, sizes
        :return: NULL
        """
        self.app = QtGui.QApplication([])
        self.win = QtGui.QMainWindow()
        area = DockArea()
        self.d_control = Dock("Dock Controls", size=(50, 200))
        self.d_plot = Dock("Dock Plots", size=(500, 200))
        self.d_train = Dock("Training Signal", size=(500, 50))
        area.addDock(self.d_control, 'left')
        area.addDock(self.d_plot, 'right')
        area.addDock(self.d_train, 'bottom', self.d_plot)
        self.win.setCentralWidget(area)
        self.win.resize(1500, 800)
        self.win.setWindowTitle('GUI Training')
        self.addDockWidgetsControl()
        self.curves_left = []
        self.curves_right = []
        self.curve_bottom = []
        self.addDockWidgetsPlots()
        self.setCrosshair()
        self.setRectRegionROI()
        self.elec = []
        self.data = []
        self.trainingData = TrainingData()
        self.saveBtn_events.clicked.connect(lambda: self.analyse_data())
        self.saveBtn_nonEvents.clicked.connect(lambda: self.add_non_events())
        self.undoBtn.clicked.connect(lambda: self.undo())
        self.analyseBtn.clicked.connect(lambda: self.process_data())
        self.readPredictedVal.clicked.connect(lambda: self.read_predicted())
        self.analyseInternal.clicked.connect(lambda: self.analyse_internal())
        self.save_trained_data.clicked.connect(lambda: self.save_trained())
        self.load_trained_data.clicked.connect(lambda: self.load_trained())

        self.win.show()

    def addDockWidgetsControl(self):
        w1 = pg.LayoutWidget()
        label = QtGui.QLabel('Usage info')
        self.saveBtn_events = QtGui.QPushButton('Save As Events')
        self.saveBtn_nonEvents = QtGui.QPushButton('Save As Non-Events')
        self.undoBtn = QtGui.QPushButton('Undo')
        self.analyseBtn = QtGui.QPushButton('Analyse')
        self.readPredictedVal = QtGui.QPushButton('Read Weka CSV')
        self.analyseInternal = QtGui.QPushButton('SciKit Analyse')
        self.save_trained_data = QtGui.QPushButton('Save Training')
        self.load_trained_data = QtGui.QPushButton('Load Training')
        w1.addWidget(label, row=0, col=0)
        w1.addWidget(self.saveBtn_events, row=1, col=0)
        w1.addWidget(self.saveBtn_nonEvents, row=1, col=1)
        w1.addWidget(self.undoBtn, row=2, col=0)
        w1.addWidget(self.analyseBtn, row=3, col=0)
        w1.addWidget(self.readPredictedVal, row=4,col=0)
        w1.addWidget(self.analyseInternal, row=5, col=0)
        w1.addWidget(self.save_trained_data, row=6, col=0)
        w1.addWidget(self.load_trained_data, row=6, col=1)
        self.d_control.addWidget(w1, row=1, colspan=2)


    def addDockWidgetsPlots(self):
        self.w1 = pg.PlotWidget(title="Plots of the slow-wave data")
        self.w2 = pg.PlotWidget(title="Plots of zoomed-in slow-wave data")
        self.w3 = pg.PlotWidget(title="Selected Data for Training")
        c = pg.PlotCurveItem(pen=pg.mkPen('r', width=2))
        c_event = pg.PlotCurveItem(pen=pg.mkPen('y', width=2))
        self.curve_bottom.append(c)
        self.curve_bottom.append(c_event)
        self.w3.addItem(c)
        self.w3.addItem(c_event)
        nPlots =256
        for i in range(nPlots):
            c1 = pg.PlotCurveItem(pen=(i, nPlots*1.3))
            c1.setPos(0, i * 20)
            self.curves_left.append(c1)
            self.w1.addItem(c1)
            self.w1.setYRange(0, 900)
            self.w1.setXRange(0, 3000)

            c2 = pg.PlotCurveItem(pen=(i, nPlots*1.3))
            c2.setPos(0, i * 20)
            self.curves_right.append(c2)
            self.w2.addItem(c2)
        self.s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        self.s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        self.w1.addItem(self.s1)
        self.w2.addItem(self.s2)
        self.d_plot.addWidget(self.w1, row=0, col=0)
        self.d_plot.addWidget(self.w2, row=0, col=1)
        self.d_train.addWidget(self.w3, row=0, col=0)
        self.proxy = pg.SignalProxy(self.w2.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.w2.scene().sigMouseClicked.connect(self.onClick)
        self.w2.sigXRangeChanged.connect(self.updateRegion)
        self.w2.sigYRangeChanged.connect(self.updateRegion)

    def setCrosshair(self):
        """
        Cross hair definition and initiation
        """
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.w2.addItem(self.vLine, ignoreBounds=True)
        self.w2.addItem(self.hLine, ignoreBounds=True)

    def setRectRegionROI(self):
        '''
        Rectangular selection region
        '''
        self.rect = pg.RectROI([300, 300], [1500, 100], pen=pg.mkPen(color='y', width=2))
        self.w1.addItem(self.rect)
        self.rect.sigRegionChanged.connect(self.updatePlot)


    def setCurveItem(self, nPlots, nSamples):
        for i in range(nPlots):
            c1 = pg.PlotCurveItem(pen=(i, nPlots*1.3))
            self.w1.addItem(c1)
            c1.setPos(0, i * 20)
            self.curves_left.append(c1)
            self.w1.setYRange(0, 900)
            self.w1.setXRange(0, 3000)
            self.w1.resize(600, 900)

            c2 = pg.PlotCurveItem(pen=(i, nPlots*1.3))
            self.w2.addItem(c2)
            c2.setPos(0, i * 20)
            self.curves_right.append(c2)
            self.w2.showGrid(x=True, y=True)
            self.w2.resize(600, 900)
        self.updatePlot()

    def setData(self, data, nPlots, nSize):
        self.data = data
        self.trainingData.setData(data)
        self.setCurveItem(nPlots, nSize)
        for i in range(nPlots):
            self.curves_left[i].setData(data[i])
            self.curves_right[i].setData(data[i])

    def updatePlot(self):
        xpos = self.rect.pos()[0]
        ypos = self.rect.pos()[1]
        width = self.rect.size()[0]
        height = self.rect.size()[1]
        self.w2.setXRange(xpos, xpos+width, padding=0)
        self.w2.setYRange(ypos, ypos+height, padding=0)

    def updateRegion(self):
        xpos = self.w2.getViewBox().viewRange()[0][0]
        ypos = self.w2.getViewBox().viewRange()[1][0]
        self.rect.setPos([xpos, ypos], update=False)

    def mouseMoved(self, evt):
        pos = evt[0]
        vb = self.w2.plotItem.vb
        if self.w2.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def onClick(self, evt):
        pos = evt.scenePos()
        vb = self.w2.plotItem.vb
        if self.w2.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            self.elec.append([int(round(mousePoint.y()/20)), int(round(mousePoint.x()))])
            self.trainingData.addRegion([int(round(mousePoint.y()/20)), int(round(mousePoint.x()))])

    """
    The binding functions for different gui command buttons.
    """
    def analyse_data(self):
        self.trainingData.add_events()
        self.curve_bottom[0].setData(self.trainingData.plotDat.flatten()[0:self.trainingData.plotLength])
        self.curve_bottom[1].setData(self.trainingData.plotEvent.flatten()[0:self.trainingData.plotLength])
        self.w3.setXRange(0, self.trainingData.plotLength, padding=0)
        self.w3.setYRange(-10, 10, padding=0)

    def add_non_events(self):
        self.trainingData.add_non_events()
        self.curve_bottom[0].setData(self.trainingData.plotDat.flatten()[0:self.trainingData.plotLength])
        self.curve_bottom[1].setData(self.trainingData.plotEvent.flatten()[0:self.trainingData.plotLength])
        self.w3.setXRange(0, self.trainingData.plotLength, padding=0)
        self.w3.setYRange(-10, 10, padding=0)

    def undo(self):
        self.trainingData.undo()
        self.curve_bottom[0].setData(self.trainingData.plotDat.flatten()[0:self.trainingData.plotLength])
        self.curve_bottom[1].setData(self.trainingData.plotEvent.flatten()[0:self.trainingData.plotLength])
        self.w3.setXRange(0, self.trainingData.plotLength, padding=0)
        self.w3.setYRange(-10, 10, padding=0)

    def read_predicted(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open ARFF WEKA generated output file')
        if filename == u'':
            return
        test = ARFFcsvReader(filename)
        prediction = np.asarray(test.get_prediction())
        diff = np.diff(prediction)
        linear_at = np.array(np.where(diff == 1))
        pos = []
        length = len(self.data[1])
        for val in linear_at.transpose():
            pos.append([int(val/length), int(val % length)])
        pos_np = np.asarray(pos).transpose()

        self.s1.addPoints(x=pos_np[1], y=(pos_np[0] * 20))
        self.s2.addPoints(x=pos_np[1], y=(pos_np[0] * 20))

    def process_data(self):

        test_data = np.reshape(self.data, -1)
        data = self.trainingData.plotDat[0][0:self.trainingData.plotLength]
        events = self.trainingData.plotEvent[0][0:self.trainingData.plotLength]/5
        Process(target=self.process_thread, args=(data, events)).start()
        Process(target=self.process_thread, args=[test_data]).start()

    def process_thread(self, data, event=None):
        training_analyser = FeatureAnalyser()
        # FeatureAnalyser requires the 1d data to be passed as array of an array
        training_features = training_analyser.process_data([data])
        if event is None:
            output_name = cg.test_file_name
        else:
            output_name = cg.training_file_name
        weka_write = WekaInterface(training_features, output_name)
        weka_write.arff_write(event)

    def analyse_internal(self):
        self.s1.clear()
        self.s2.clear()
        # Deal with training data
        data = self.trainingData.plotDat[0][0:self.trainingData.plotLength]
        events = self.trainingData.plotEvent[0][0:self.trainingData.plotLength]/5
        training_analyser = FeatureAnalyser()
        training_features_training = training_analyser.process_data([data])

        # FeatureAnalyser requires the 1d data to be passed as array of an array
        test_data_analyser = FeatureAnalyser()
        # FeatureAnalyser requires the 1d data to be passed as array of an array
        test_data_features = test_data_analyser.process_data([test_data])
        classifier = ClassifySlowWavesScikit()
        prediction = classifier.classify_data(training_features_training, events, test_data_features)
        diff = np.diff(prediction)
        linear_at_uncorrected = np.array(np.where(diff == 1))
        rows, cols = linear_at_uncorrected.shape
        to_remove_index = []
        for i in range(cols - 1):
            if linear_at_uncorrected[0][i + 1] - linear_at_uncorrected[0][i] < 60:
                to_remove_index.append(i + 1)
        linear_at = np.delete(linear_at_uncorrected, to_remove_index)

        pos = []
        length = len(self.data[0])
        sync_events = []

        ''' Check for sync events'''
        for val in linear_at.transpose():
            sync_events.append(int(val % length))
        remove_sync_point = set([x for x in sync_events if sync_events.count(x) > 1])

        ''' Remove the sync events from the actual array'''
        for val in linear_at.transpose():
            if int(val % length) not in remove_sync_point:
                pos.append([int(val/length), int(val % length)])

        pos_np = np.asarray(pos).transpose()
        if pos_np.size is 0:
            print "No events detected"
            return
        self.s1.addPoints(x=pos_np[1], y=(pos_np[0] * 20))
        self.s2.addPoints(x=pos_np[1], y=(pos_np[0] * 20))

    def save_trained(self):
        with open(cg.trained_file, 'wb') as output:
            pickle.dump(self.trainingData, output, pickle.HIGHEST_PROTOCOL)

    def load_trained(self):
        self.trainingData = np.load(cg.get_trained_file())
        self.curve_bottom[0].setData(self.trainingData.plotDat.flatten()[0:self.trainingData.plotLength])
        self.curve_bottom[1].setData(self.trainingData.plotEvent.flatten()[0:self.trainingData.plotLength])
        self.w3.setXRange(0, self.trainingData.plotLength, padding=0)
        self.w3.setYRange(-10, 10, padding=0)

