import tensorflow as tf
import numpy as np
import scipy
import reader
import model

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("mode",         "train",            "train")
tf.app.flags.DEFINE_string("data_dir",     "tabelog_final_s",  "dir")
tf.app.flags.DEFINE_float("learning_rate", 0.01,              "Learning rate.")
tf.app.flags.DEFINE_integer("loop_num",    10,                 "Number of train.")
tf.app.flags.DEFINE_integer("batch_size",  100,                "batch.")
tf.app.flags.DEFINE_integer("steps",       105,               "max_step")
tf.app.flags.DEFINE_integer("vocab_size",  98,                "vocaburary")
tf.app.flags.DEFINE_integer("hidden_size", 128,                "hidden")
tf.app.flags.DEFINE_integer("out_size",    3,                  "out")

def assert_x_row(row):
  print(row.shape)
  assert type(row) == np.ndarray
  assert row.shape[0] == FLAGS.batch_size
  assert row.shape[1]  > FLAGS.steps
  assert row.shape[2] == FLAGS.vocab_size

def assert_y_row(row):
  print(row.shape)
  assert type(row) == np.ndarray
  assert row.shape[0] == FLAGS.batch_size
  assert row.shape[1]  > FLAGS.steps
  assert row.shape[2] == FLAGS.out_size

def assert_all_data(allx, ally, allz):
  assert type(allx) == np.ndarray
  assert type(ally) == np.ndarray
  assert type(allz) == np.ndarray
  batch_num = allx.shape[0]
  assert batch_num > 10
  assert batch_num == len(ally)
  assert batch_num == len(allz)
  assert_x_row(allx)
  assert_y_row(ally)

def main(argv=None):
  xdata, ydata, zdata, ids, vocabrary = reader.load_master_data(FLAGS.data_dir)

  allx, ally, allz = reader.load_train_data(ids, xdata, ydata, zdata, FLAGS.batch_size)
  assert_all_data(allx, ally, allz)

  train_x_data, test_x_data, train_y_data, test_y_data = reader.split_data(allx, ally)
  print(train_x_data.shape)
  print(test_x_data.shape)
  print(train_y_data.shape)
  print(test_y_data.shape)
  print("Over")
  1 / 0

  x, y = model.placeholders()

  pred, loss, initial_state, final_state = model.RNN(x, y, FLAGS.steps / FLAGS.batch_size)

  optimizer = model.optimizer(loss)
  accuracy  = model.accuracy(pred, y)

  with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    for step in range(FLAGS.loop_num):
      batch_x = train_data[step]['x']
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
