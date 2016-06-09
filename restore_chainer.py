import chainer
from chainer import serializers
from IPython import embed

import cmain
import sys
import reader

model    = cmain.model()
npy_file = sys.argv[1]
serializers.load_npz(npy_file, model)

vocab_size = 98
n_units    = 64
out_size   = 3
batch_size = 20
steps      = 30
use_gpu    = True

xdata, ydata, zdata, ids, vocabrary = reader.load_master_data('tabelog_final_s')
allx, ally, allz                    = reader.load_train_data(ids, xdata, ydata, zdata, batch_size, steps, vocab_size, out_size)
train_x_data, test_x_data, train_y_data, test_y_data, train_z_data, test_z_data = reader.split_data(allx, ally, allz)

embed()
