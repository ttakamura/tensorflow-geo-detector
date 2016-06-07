import tensorflow as tf
import numpy as np
from tensorflow.models.rnn import rnn, rnn_cell

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("mode",         "train",            "train")
tf.app.flags.DEFINE_string("data_dir",     "tabelog_final_s",  "dir")
tf.app.flags.DEFINE_float("learning_rate", 0.001,              "Learning rate.")
tf.app.flags.DEFINE_integer("loop_num",    64,                 "Number of train.")
tf.app.flags.DEFINE_integer("batch_size",  1,                  "batch.")
tf.app.flags.DEFINE_integer("data_num",    100,                "Data of all.")
tf.app.flags.DEFINE_integer("steps",       1000,               "max_step")
tf.app.flags.DEFINE_integer("vocab_size",  100,                "vocaburary")
tf.app.flags.DEFINE_integer("hidden_size", 128,                "hidden")
tf.app.flags.DEFINE_integer("out_size",    3,                  "out")

def RNN(x, y):
  # Define weights
  weights = {
    'hidden': tf.Variable(tf.random_normal([FLAGS.vocab_size, FLAGS.hidden_size])),
    'out': tf.Variable(tf.random_normal([FLAGS.hidden_size, FLAGS.out_size]))
  }
  biases = {
    'hidden': tf.Variable(tf.random_normal([FLAGS.hidden_size])),
    'out': tf.Variable(tf.random_normal([FLAGS.out_size]))
  }

  # Prepare data shape to match `rnn` function requirements
  # Current data input shape: (batch_size, n_steps, n_input)
  # Permuting batch_size and n_steps
  x = tf.transpose(x, [1, 0, 2])

  # Reshaping to (n_steps*batch_size, n_input)
  x = tf.reshape(x, [-1, FLAGS.vocab_size])

  # Split to get a list of 'n_steps' tensors of shape (batch_size, n_hidden)
  # This input shape is required by `rnn` function
  x = tf.split(0, FLAGS.steps, x)

  # Define a lstm cell with tensorflow
  lstm_cell = rnn_cell.BasicLSTMCell(FLAGS.hidden_size, forget_bias=1.0)

  # Get lstm cell output
  outputs, states = rnn.rnn(lstm_cell, x, dtype=tf.float32)

  # Linear activation, using rnn inner loop last output
  pred = tf.matmul(outputs[-1], weights['out']) + biases['out']

  # Define loss and optimizer
  cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))

  return pred, loss

def load_train_data(step, ids):
  # TODO
  # i = step /
  hash = ids[step][1]
  return np.load("%s/np/%s.npy" % (FLAGS.data_dir, hash))

def main(argv=None):
  ids, vocabrary = np.load("%s/np/main.np.npy" % FLAGS.data_dir)
  np.random.shuffle(ids)

  # tf Graph input
  x = tf.placeholder("float", [None, FLAGS.steps, FLAGS.vocab_size])
  y = tf.placeholder("float", [None, FLAGS.steps, FLAGS.out_size])

  pred, loss = RNN(x, y)
  optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(loss)

  # Evaluate model
  correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
  accuracy     = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

  # Initializing the variables
  init = tf.initialize_all_variables()

  # Launch the graph
  with tf.Session() as sess:
    sess.run(init)

    # Keep training until reach max iterations
    for step in range(FLAGS.loop_num):
      batch_x, batch_y, batch_z = load_train_data(step, ids)
      batch_x = batch_x.reshape((FLAGS.batch_size, FLAGS.steps, FLAGS.vocab_size))
      sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})

      if step > 0:
        acc  = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
        loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
        print("step %d , acc %f" % (step, acc))

      ## Calculate accuracy for 128 mnist test images
      #test_len = 128
      #test_data = mnist.test.images[:test_len].reshape((-1, n_steps, n_input))
      #test_label = mnist.test.labels[:test_len]
      #print "Testing Accuracy:", \
      #  sess.run(accuracy, feed_dict={x: test_data, y: test_label})

if __name__ == '__main__':
  tf.app.run()
