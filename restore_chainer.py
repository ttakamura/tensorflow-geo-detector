import chainer
from chainer import serializers
from IPython import embed

import cmain
import sys

model    = cmain.model()
npy_file = sys.argv[1]
serializers.load_npz(npy_file, model)

xdata, ydata, zdata, ids, vocabrary = reader.load_master_data('tabelog_final_s')
allx, ally, allz = reader.load_train_data(ids, xdata, ydata, zdata, batch_size, steps, vocab_size, out_size)
train_x_data, test_x_data, train_y_data, test_y_data, train_z_data, test_z_data = reader.split_data(allx, ally, allz)

embed()
