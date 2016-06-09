import chainer
# # from chainer import computational_graph
from chainer import cuda
from chainer import Chain
from chainer import Variable
import chainer.links as L
import chainer.functions as F
from chainer import optimizers
from chainer import serializers

import numpy as np
import scipy
import reader
import model
import gc

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

    def __call__(self, x, t):
        loss   = 0.0
        outseq = list()
        for i in range(x.shape[1]):
            z    = x[:,i,:]
            h0   = self.embed(z)
            h1   = self.l1(F.dropout(h0, train=self.train))
            h2   = self.l2(F.dropout(h1, train=self.train))
            y    = self.l3(F.dropout(h2, train=self.train))
            if t != None:
                zt   = t[:,i]
                loss += F.softmax_cross_entropy(y, zt)
            outseq.append(y)
        return loss, outseq

vocab_size = 98
n_units    = 64
out_size   = 3
batch_size = 20
steps      = 30
use_gpu    = True

rnn = RNNLM(vocab_size, n_units, out_size)
optimizer = optimizers.SGD()
optimizer.setup(rnn)

if use_gpu:
    # cuda.get_device(args.gpu).use()
    rnn.to_gpu()
    xp = cuda.cupy
else:
    xp = np

def model():
  return rnn

def train(x, t):
  x = Variable(cuda.to_gpu(x))
  t = Variable(cuda.to_gpu(t))
  optimizer.zero_grads()
  loss, outputs = rnn(x, t)
  loss.backward()
  optimizer.update()
  return loss

def train_for(i, train_z_data, train_y_data):
  x = train_z_data[i]
  t = train_y_data[i].argmax(2).astype(xp.int32)
  loss = train(x, t)
  print("data %d, loss %f" % (i, loss.data))
  return loss

def main():
  xdata, ydata, zdata, ids, vocabrary = reader.load_master_data('tabelog_final_s')

  allx, ally, allz = reader.load_train_data(ids, xdata, ydata, zdata, batch_size, steps, vocab_size, out_size)

  train_x_data, test_x_data, train_y_data, test_y_data, train_z_data, test_z_data = reader.split_data(allx, ally, allz)

  for epoch in range(20):
    print('epoch %d' % epoch)

    for i in range(len(train_z_data)):
      loss = train_for(i, train_z_data, train_y_data)
      if i % 10 == 0:
          gc.collect()

      # accuracy(test_x_data, test_y_data)
      if i % 50 == 0:
        # Save the model and the optimizer
        print('epoch done')
        print('save the model')
        serializers.save_npz(('data/chainer_%d_%d.model' % (epoch, i)), rnn)
        print('save the optimizer')
        serializers.save_npz(('data/chainer_%d_%d.state' % (epoch, i)), optimizer)

        import tensorflow as tf
        import numpy as np

        FLAGS = tf.app.flags.FLAGS
        tf.app.flags.DEFINE_string('mode', 'train', 'train or console')

if __name__ == '__main__':
  main()
