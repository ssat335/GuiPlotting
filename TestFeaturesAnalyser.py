"""
    Author: Shameer Sathar
"""

import unittest
from FeatureAnalyser import FeatureAnalyser
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

class TestFeaturesAnalyser(unittest.TestCase):
    def test(self):
        test_data = sio.loadmat('/people/ssat335/PycharmProjects/GuiPlotting/data/training_data_test.mat')
        #print test_data['vect']
        data = np.asarray(test_data['vect'])
        #print data.transpose().shape
        analyser = FeatureAnalyser()
        data = analyser.process_data(data.transpose())
        (rows, cols) = data.shape
        for i in [0,32]:
            plt.figure(i)
            plt.plot(data[i][:])
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.figure(51)
        plt.plot(data[31][:])
        plt.show()
        plt.close()
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

