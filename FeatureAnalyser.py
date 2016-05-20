from scipy.signal import savgol_filter
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

class FeatureAnalyser:

    def __init__(self):
        self.data = []
        self.len = 0
        self.features = []

    def process_data(self, plot):
        """
        The features for the data is created. The plot should in in 1 x #samples size.
        :param plot: Input values to be processed for generating features
        :return: features in #features X #sample size
        """
        print plot
        self.data = np.asarray(plot)
        print self.data.shape
        temp, self.len = self.data.shape
        print self.len
        '''Obtain the features'''
        self.features = np.zeros([33, self.len], dtype=float)
        self.features[0, :] = self.data
        self.features[1, :] = self.apply_diff(self.data)
        for i in range(1, 4, 1):
            self.features[i + 1, :] = gaussian_filter1d(self.data, 6 * pow(2, (i-1)))
        for i in range(1, 4, 1):
            self.features[i + 4, :] = self.apply_diff(self.features[i, :])
        for i in range(1, 4, 1):
            self.features[i + 5, :] = self.shift_signals(self.data, -90*i)
        for i in range(1, 4, 1):
            self.features[i + 10, :] = self.shift_signals(self.data, 90*i)
        for i in range(1, 19, 1):
            self.features[i + 13, :] = gaussian_filter1d(self.features[int((i-1)/3) + 7, :], 6 * pow(2, ((i - 1) % 3)))
        self.features[32, :] = np.square(self.features[1, :])
        return self.features

    def apply_diff(self, data):
        return np.append(np.diff(data, n=1), 0)

    def shift_signals(self, data, shift_period):
        if shift_period > 0:
            pre_temp = np.ones([1, shift_period], dtype=float) * data[0][1]
            return np.append(pre_temp, data[0][0:self.len-shift_period])
        elif shift_period < 0:
            shift_period *= -1
            pre_temp = np.ones([1, shift_period], dtype=float) * data[0][self.len-1]
            return np.append(data[0][shift_period:], pre_temp)
        else:
            return data


