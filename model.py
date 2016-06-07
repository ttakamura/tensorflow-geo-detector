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
    x = tf.placeholder("float", [None, FLAGS.steps, FLAGS.vocab_size], name='X')
    y = tf.placeholder("float", [None, FLAGS.steps, FLAGS.out_size], name='Y')
  return x, y

def optimizer(loss):
  with tf.variable_scope('optimize') as scope:
    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(loss)
  return optimizer

def accuracy(pred, y):
  with tf.variable_scope('evaluate') as scope:
    correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
    accuracy     = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
  return accuracy

def RNN(x, y):
  x, y = reshape(x, y)

  with tf.variable_scope('lstm1') as scope:
    lstm_cell = rnn_cell.BasicLSTMCell(FLAGS.hidden_size, forget_bias=1.0)
    outputs, states = rnn.rnn(lstm_cell, x, dtype=tf.float32)

  print('x', x[0])
  print('y', y[0])
  print('out', outputs[0])

  with tf.variable_scope('output') as scope:
    W_out = weight_variable([FLAGS.hidden_size, FLAGS.out_size])
    b_out = bias_variable([FLAGS.out_size])
    pred  = list()
    loss  = list()
    for i in range(len(outputs)):
      pred.append( tf.matmul(outputs[i], W_out) + b_out )
      loss.append( tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred[i], y[i])) )

  return pred, loss

# ------- reshaping -----------------------------------

def assert_shape(x,y):
  xshape = x.get_shape()
  xshape[0].assert_is_compatible_with(FLAGS.batch_size)
  xshape[1].assert_is_compatible_with(FLAGS.steps)
  xshape[2].assert_is_compatible_with(FLAGS.vocab_size)

  yshape = y.get_shape()
  yshape[0].assert_is_compatible_with(FLAGS.batch_size)
  yshape[1].assert_is_compatible_with(FLAGS.steps)
  yshape[2].assert_is_compatible_with(FLAGS.out_size)

def assert_reshaped_x(x):
  assert len(x) == FLAGS.steps
  xshape = x[0].get_shape()
  xshape[0].assert_is_compatible_with(FLAGS.batch_size)
  xshape[1].assert_is_compatible_with(FLAGS.vocab_size)

def assert_reshaped_y(y):
  assert len(y) == FLAGS.steps
  yshape = y[0].get_shape()
  yshape[0].assert_is_compatible_with(FLAGS.batch_size)
  yshape[1].assert_is_compatible_with(FLAGS.out_size)

def reshape(x, y):
  assert_shape(x, y)

  # Permuting => (steps, batch_size, vocab_size)
  # Reshaping => (steps * batch_size, vocab_size)
  # Split     => list of 'steps' tensors of shape (batch_size, vocab_size)
  x = tf.transpose(x, [1, 0, 2])
  x = tf.reshape(x, [-1, FLAGS.vocab_size])
  x = tf.split(0, FLAGS.steps, x)
  assert_reshaped_x(x)

  # Permuting => (steps, batch_size, out_size)
  # Reshaping => (steps * batch_size, out_size)
  # Split     => list of 'steps' tensors of shape (batch_size, vocab_size)
  y = tf.transpose(y, [1, 0, 2])
  y = tf.reshape(y, [-1, FLAGS.out_size])
  y = tf.split(0, FLAGS.steps, y)
  assert_reshaped_y(y)

  return x, y
