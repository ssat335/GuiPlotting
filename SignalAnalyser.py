from scipy import signal
import numpy as np
from scipy.ndimage.filters import gaussian_filter

class SignalAnalyser:

    def __init__(self):
        self.data = []
        self.event = []
        self.len = 0
        self.features = []

    def process_data(self, plot, event_info, length):
        self.data = plot[0:length]
        print len(plot)
        self.event = event_info[0:length]
        self.len = length
        '''Obtain the features'''
        self.features = np.zeros([31, self.len], dtype=float)

        self.features[0, :] = self.apply_diff(self.data)
        for i in range(1, 4, 1):
            self.features[i, :] = gaussian_filter(self.data, 6 * pow(2, (i-1)))
        for i in range(1, 4, 1):
            self.features[i+3, :] = self.apply_diff(self.features[i, :])
        for i in range(1, 4, 1):
            self.features[i+6, :] = self.shift_signals(self.data, -90*i)
        for i in range(1, 4, 1):
            self.features[i+9, :] = self.shift_signals(self.data, 90*i)
        print 'test'
        for i in range(1, 19, 1):
            self.features[i+12, :] = gaussian_filter(self.features[int((i-1)/3) + 7, :],  6 * pow(2, ((i -1) % 3)))

    def apply_diff(self, data):
        return np.append(np.diff(data, n=1, axis=0), 0)

    def shift_signals(self, data, shift_period):
        if shift_period > 0:
            pre_temp = np.ones([1, shift_period], dtype=float) * data[0:1]
            return np.append(pre_temp, data[0:len(data)-shift_period])
        elif shift_period < 0:
            shift_period *= -1
            pre_temp = np.ones([1, shift_period], dtype=float) * data[len(data)-1]
            return np.append(data[shift_period:], pre_temp)
        else:
            return data


