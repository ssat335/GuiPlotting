"""
    Author: Shameer Sathar
    Description: Deal with training data.
"""

import numpy as np


class TrainingData:

    def __init__(self):
        self.data = []
        self.regions = []
        self.plotLength = 0
        self.prev_length = 0
        """
        Initialise the array with long length.
        """
        self.plotDat = np.zeros([1, 200000], dtype=float)
        self.plotEvent = np.zeros([1, 200000], dtype=int)

    def setData(self, data):
        self.data = np.array(data)

    def addRegion(self, region):
        self.regions.append(region)

    def add_events(self):
        i = 0
        while i <= (len(self.regions) - 3):
            elec = self.regions[i][0]
            init_pos = self.regions[i][1]
            mid_pos = self.regions[i+1][1]
            end_pos = self.regions[i+2][1]
            length = end_pos-init_pos
            self.plotDat[0][self.plotLength:self.plotLength+length] = self.data[elec][init_pos:end_pos] + \
                self.plotDat[0][self.plotLength - 1] - self.data[elec][init_pos]
            self.plotEvent[0][self.plotLength + mid_pos - init_pos:self.plotLength+end_pos-init_pos] = 5
            self.plotLength = self.plotLength+length
            i += 3
            self.prev_length = length
        self.clearRegion()

    def add_non_events(self):
        i = 0
        while i <= (len(self.regions) - 2):
            elec = self.regions[i][0]
            init_pos = self.regions[i][1]
            end_pos = self.regions[i+1][1]
            length = end_pos-init_pos
            self.plotDat[0][self.plotLength:self.plotLength+length] = self.data[elec][init_pos:end_pos] + \
                self.plotDat[0][self.plotLength - 1] - self.data[elec][init_pos]
            self.plotLength = self.plotLength+length
            i += 2
            self.prev_length = length
        self.clearRegion()

    def undo(self):
        self.plotLength -= self.prev_length
        self.plotDat[0][self.plotLength:self.plotLength+self.prev_length] = 0
        self.plotEvent[0][self.plotLength:self.plotLength+self.prev_length] = 0
        self.prev_length = 0

    def clearRegion(self):
        del self.regions[:]


