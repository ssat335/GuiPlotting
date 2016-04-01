from ARFFcsvReader import ARFFcsvReader
import numpy as np

test = ARFFcsvReader('data/results_data.arff')
prediction = np.asarray(test.get_prediction())
diff = np.diff(prediction)
linear_at = np.array(np.where(diff == 1))
print type(linear_at)
print linear_at.shape
pos = []
for val in linear_at.transpose():
    pos.append([int(val/9001), int(val % 9001)])
    print int(val/9001), int(val % 9001)
#print np.where(diff == 1)
print prediction.size
print len(pos)
print pos[25][0]