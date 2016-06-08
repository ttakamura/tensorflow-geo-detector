import tensorflow as tf
import numpy as np
from tensorflow.models.rnn import rnn, rnn_cell

FLAGS = tf.app.flags.FLAGS

def weight_variable(shape, wd=None):
  initial = tf.truncated_normal(shape, stddev=0.01)
  w = tf.Variable(initial, name='W')
  if wd is not None:
    weight_decay = tf.mul(tf.nn.l2_loss(w), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
  return w

def bias_variable(shape):
  initial = tf.constant(0.0, shape=shape)
  return tf.Variable(initial, name='b')

def placeholders():
  with tf.variable_scope('placeholder') as scope:
    x = tf.placeholder(np.float32, [None, FLAGS.steps, FLAGS.vocab_size], name='X')
    y = tf.placeholder(np.float32, [None, FLAGS.steps, FLAGS.out_size],   name='Y')
  return x, y

def optimizer(loss):
  with tf.variable_scope('optimize') as scope:
    total_loss = tf.add_n(loss, name='total_loss')
    adam       = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate)
    optimizer  = adam.minimize(total_loss)
  return optimizer

def accuracy(pred, y):
  with tf.variable_scope('evaluate') as scope:
    correct_pred = list()
    for i in range(len(pred)):
      ptop = tf.argmax(pred[i],1)
      ytop = tf.argmax(y[i],1)
      eql  = tf.equal(ptop, ytop)
      correct_pred.append(eql)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
  return accuracy

def LSTM(x, y):
  x, y  = reshape(x, y, 1)
  W_out = weight_variable([FLAGS.hidden_size, FLAGS.out_size])
  b_out = bias_variable([FLAGS.out_size])
  predictions = list()
  cost_all    = list()
  with tf.variable_scope('lstm1') as scope:
    lstm_cell = rnn_cell.BasicLSTMCell(FLAGS.hidden_size, forget_bias=1.0)
    outputs, states = rnn.rnn(lstm_cell, x, dtype=tf.float32)
    #
    # print(len(outputs))
    # for i in range(len(outputs)):
    #   print(outputs[i].get_shape()) => (?, 128)
    #
    for i in range(len(outputs)):
      output    = outputs[i]
      pred      = tf.matmul(output, W_out) + b_out
      current_y = y[i]

      # tensorflow.python.pywrap_tensorflow.StatusNotOK:
      # Invalid argument: logits and labels must be same size:
      # logits_size=[9800,3]
      # labels_size=[100,3]

      gg = pred.reshape(98, FLAGS.batch_size, FLAGS.out_size)

      # I don't know これでうまくいく？
      loss = tf.nn.softmax_cross_entropy_with_logits(gg[0], current_y)

      cost = tf.reduce_mean(loss)
      cost_all.append(cost)
      predictions.append(pred)
  return predictions, cost_all

# ------- reshaping -----------------------------------
def assert_reshaped_x(x, vocab_size):
  assert len(x) == FLAGS.steps
  xshape = x[0].get_shape()
  xshape[0].assert_is_compatible_with(FLAGS.batch_size)
  xshape[1].assert_is_compatible_with(vocab_size)

def assert_reshaped_y(y):
  assert len(y) == FLAGS.steps
  yshape = y[0].get_shape()
  yshape[0].assert_is_compatible_with(FLAGS.batch_size)
  yshape[1].assert_is_compatible_with(FLAGS.out_size)

def reshape(x, y, vocab_size):
  # assert_shape(x, y)
  # Permuting => (steps, batch_size, vocab_size)
  # Reshaping => (steps * batch_size, vocab_size)
  # Split     => list of 'steps' tensors of shape (batch_size, vocab_size)
  x = tf.transpose(x, [1, 0, 2])
  x = tf.reshape(x, [-1, vocab_size])
  x = tf.split(0, FLAGS.steps, x)
  assert_reshaped_x(x, vocab_size)

  # Permuting => (steps, batch_size, out_size)
  # Reshaping => (steps * batch_size, out_size)
  # Split     => list of 'steps' tensors of shape (batch_size, vocab_size)
  y = tf.transpose(y, [1, 0, 2])
  y = tf.reshape(y, [-1, FLAGS.out_size])
  y = tf.split(0, FLAGS.steps, y)
  assert_reshaped_y(y)
  return x, y

#def assert_shape(x,y):
#  xshape = x.get_shape()
#  xshape[0].assert_is_compatible_with(FLAGS.batch_size)
#  xshape[1].assert_is_compatible_with(FLAGS.steps)
#  xshape[2].assert_is_compatible_with(FLAGS.vocab_size)
#
#  yshape = y.get_shape()
#  yshape[0].assert_is_compatible_with(FLAGS.batch_size)
#  yshape[1].assert_is_compatible_with(FLAGS.steps)
#  yshape[2].assert_is_compatible_with(FLAGS.out_size)
