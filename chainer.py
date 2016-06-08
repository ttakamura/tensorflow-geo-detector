import numpy as np

import chainer
# from chainer import computational_graph
from chainer import cuda
import chainer.links as L
from chainer import optimizers
from chainer import serializers

import numpy as np
import scipy
import reader
import model

class RNN(Chain):
    def __init__(self):
        super(RNN, self).__init__(
            embed=L.EmbedID(1000, 100),  # word embedding
            mid=L.LSTM(100, 50),  # the first LSTM layer
            out=L.Linear(50, 1000),  # the feed-forward output layer
        )

    def reset_state(self):
        self.mid.reset_state()

    def __call__(self, cur_word):
        # Given the current word ID, predict the next word.
        x = self.embed(cur_word)
        h = self.mid(x)
        y = self.out(h)
        return y

rnn = RNN()
model = L.Classifier(rnn)
optimizer = optimizers.SGD()
optimizer.setup(model)

model.zerograds()

xdata, ydata, zdata, ids, vocabrary = reader.load_master_data(FLAGS.data_dir)

allx, ally, allz = reader.load_train_data(ids, xdata, ydata, zdata, FLAGS.batch_size)

train_x_data, test_x_data, train_y_data, test_y_data, train_z_data, test_z_data = reader.split_data(allx, ally, allz)

for epoch in range(20):
  print('epoch %d' % epoch)
  for i in range(len(train_x_data)):
    x = Variable(train_z_data[i])
    t = Variable(train_y_data[i])
    optimizer.update(model, x, t)
