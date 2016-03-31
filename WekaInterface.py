import arff
import numpy as np


class WekaInterface:
    def __init__(self, data, file_name='test_data.arff'):
        self.data = np.transpose(data)
        self.file_name = file_name
        self.arff_write()

    def arff_write(self, event=[]):
        ''' Write ARFF object file as required by analyser GUI.
        :param event: a list of event denotions. Empty implies it is a testing data.
        :return: null.
        '''
        attributes = []
        (rows, cols) = np.shape(self.data)
        if np.array(event).size == 0:
            hcat = np.empty((rows, 1))
            hcat.fill(np.NAN)
            ndarray = np.asarray(np.hstack((self.data, hcat)))
        else:
            #hcat_event = np.transpose(np.array(event))
            hcat_event = np.empty((len(event), 1))
            hcat_event[:, 0] = np.transpose(np.array(event))
            ndarray = np.asarray(np.hstack((self.data, hcat_event)))
        for i in range(0, cols, 1):
            attributes.append(('attribute' + str(i), 'NUMERIC'))
        attributes.append(('event', ['TRUE', 'FALSE']))
        vals = []
        for i in range(0, rows, 1):
            vals.append(ndarray[i, :])
        obj = {
            'description': 'Training set',
            'relation': 'Training',
            'attributes': attributes,
            'data': vals
        }

        ''' Write to file here'''
        f = open(self.file_name, 'wb')
        arff.dump(obj, f)
        f.close()