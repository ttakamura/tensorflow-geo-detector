import numpy as np

import chainer
# # from chainer import computational_graph
from chainer import cuda
from chainer import Chain
import chainer.links as L
from chainer import optimizers
from chainer import serializers

import numpy as np
import scipy
import reader
import model

class RNNLM(chainer.Chain):
    def __init__(self, n_vocab, n_units, n_out, train=True):
        super(RNNLM, self).__init__(
            embed=L.EmbedID(n_vocab, n_units),
            l1=L.LSTM(n_units, n_units),
            l2=L.LSTM(n_units, n_units),
            l3=L.Linear(n_units, n_out),
        )
        self.train = train

    def reset_state(self):
        self.l1.reset_state()
        self.l2.reset_state()

    def __call__(self, x):
        h0 = self.embed(x)
        h1 = self.l1(F.dropout(h0, train=self.train))
        h2 = self.l2(F.dropout(h1, train=self.train))
        y = self.l3(F.dropout(h2, train=self.train))
        return y

vocab_size = 10000
n_units    = 128
out_size   = 3
batch_size = 100

rnn = RNNLM(vocab_size, n_units, out_size)
model = L.Classifier(rnn)
optimizer = optimizers.SGD()
optimizer.setup(model)

model.zerograds()

xdata, ydata, zdata, ids, vocabrary = reader.load_master_data('tabelog_final_s')

allx, ally, allz = reader.load_train_data(ids, xdata, ydata, zdata, batch_size)

train_x_data, test_x_data, train_y_data, test_y_data, train_z_data, test_z_data = reader.split_data(allx, ally, allz)

for epoch in range(20):
  print('epoch %d' % epoch)
  for i in range(len(train_x_data)):
    x = Variable(train_z_data[i])
    t = Variable(train_y_data[i])
    optimizer.update(model, x, t)
