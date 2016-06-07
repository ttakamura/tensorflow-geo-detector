import tensorflow as tf
import numpy as np
import reader
import model

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("mode",         "train",            "train")
tf.app.flags.DEFINE_string("data_dir",     "tabelog_final_s",  "dir")
tf.app.flags.DEFINE_float("learning_rate", 0.001,              "Learning rate.")
tf.app.flags.DEFINE_integer("loop_num",    64,                 "Number of train.")
tf.app.flags.DEFINE_integer("batch_size",  100,                "batch.")
tf.app.flags.DEFINE_integer("steps",       1000,               "max_step")
tf.app.flags.DEFINE_integer("vocab_size",  100,                "vocaburary")
tf.app.flags.DEFINE_integer("hidden_size", 128,                "hidden")
tf.app.flags.DEFINE_integer("out_size",    3,                  "out")

def main(argv=None):
  ids, vocabrary = reader.load_master_data(FLAGS.data_dir)

  x, y = model.placeholders()

  pred, loss, initial_state, final_state = model.RNN(x, y, FLAGS.steps / FLAGS.batch_size)

  optimizer = model.optimizer(loss)
  accuracy  = model.accuracy(pred, y)

  with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    train_data, test_data = reader.load_train_data(ids, FLAGS.data_dir, FLAGS.batch_size)
    print(train_data)
    print(test_data)
    1 / 0

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
