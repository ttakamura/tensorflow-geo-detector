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
tf.app.flags.DEFINE_integer("vocab_size",  4230,                "vocaburary")
tf.app.flags.DEFINE_integer("hidden_size", 128,                "hidden")
tf.app.flags.DEFINE_integer("out_size",    3,                  "out")

def assert_x_row(row):
  print(type(row))
  print(len(row))
  assert type(row) == np.ndarray
  assert row.shape[0] == FLAGS.steps
  assert row.shape[1] == FLAGS.vocab_size

def assert_y_row(row):
  assert type(row) == np.ndarray
  assert row.shape[0] == FLAGS.steps
  assert row.shape[1] == FLAGS.out_size

def assert_all_data(allx, ally, allz):
  batch_num = len(allx)
  assert type(allx) == list
  assert type(ally) == list
  assert type(allz) == list
  assert batch_num > 10
  assert batch_num == len(ally)
  assert batch_num == len(allz)
  assert_x_row(allx[0])
  assert_x_row(allx[10])
  assert_y_row(ally[0])
  assert_y_row(ally[10])

def main(argv=None):
  xdata, ydata, zdata, ids, vocabrary = reader.load_master_data(FLAGS.data_dir)
  assert type(xdata) == list
  assert type(ydata) == list
  assert type(zdata) == list
  assert len(xdata) == len(ydata)
  assert len(xdata) == len(zdata)

  allx, ally, allz = reader.load_train_data(ids, xdata, ydata, zdata, FLAGS.batch_size)
  assert_all_data(allx, ally, allz)

  train_data, test_data = reader.split_data(all_data)

  print(train_data)
  print(test_data)
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
