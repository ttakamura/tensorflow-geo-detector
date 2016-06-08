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
    total_loss = tf.add_n(loss, name='total_loss')
    adam       = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate)
    optimizer  = adam.minimize(total_loss)
  return optimizer

def accuracy(pred, y):
  with tf.variable_scope('evaluate') as scope:
    correct_pred = list()
    for i in range(len(pred)):
      correct_pred.append(tf.equal(tf.argmax(pred[i],1), tf.argmax(y[i],1)))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
  return accuracy

def RNN(x, y, steps):
  x, y = reshape(x, y)

  with tf.variable_scope('lstm1') as scope:
    lstm_cell = rnn_cell.BasicLSTMCell(FLAGS.hidden_size, forget_bias=1.0)
    state     = tf.zeros([ FLAGS.batch_size, lstm_cell.state_size ])
    W_out     = weight_variable([FLAGS.hidden_size, FLAGS.out_size])
    b_out     = bias_variable([FLAGS.out_size])
    loss      = 0.0
    initial_state = state

    with tf.variable_scope("RNN"):
      for time_step in range(steps):
        if time_step > 0: tf.get_variable_scope().reuse_variables()
        output, state = lstm_cell(x[time_step], state)

        with tf.variable_scope('output_%s' % time_step) as scope:
          output = tf.matmul(output, W_out) + b_out
          loss  += tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, y[time_step]))
          outputs.append(output)

    final_state = state

  print('x', x[0])
  print('y', y[0])
  print('out', outputs[0])
  print('pred', pred[0])
  print('loss', loss)

  return pred, loss, initial_state, final_state

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
