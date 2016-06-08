import numpy as np

def load_train_data(ids, xdata, ydata, zdata, batch_size):
  xdata = np.array(xdata)
  ydata = np.array(ydata)
  zdata = np.array(zdata).astype(np.int32)
  return xdata, ydata, zdata

def split_data(allx, ally, allz):
  batch_num = allx.shape[0]
  train_num = int(batch_num * 0.7) * FLAGS.batch_size
  test_num  = int(batch_num * 1.0) * FLAGS.batch_size
  print('train_num', train_num)
  print('test_num', test_num)
  # TODO: random shuffle

  allx = allx.reshape(-1, FLAGS.vocab_size)
  ally = ally.reshape(-1, FLAGS.out_size)
  allz = allz.reshape(-1, 1)

  train_x_data = allx[0:train_num]
  test_x_data  = allx[train_num:test_num]

  train_y_data = ally[0:train_num]
  test_y_data  = ally[train_num:test_num]

  train_z_data = allz[0:train_num]
  test_z_data  = allz[train_num:test_num]

  return train_x_data, test_x_data, train_y_data, test_y_data, train_z_data, test_z_data

def load_master_data(data_dir):
  x, y, z, ids, vocabrary = np.load("%s/np/main.np.npy" % data_dir)
  np.random.shuffle(ids)
  return x, y, z, ids, vocabrary

# def load_doc_data(hash, data_dir):
#   if type(hash) == bytes:
#     hash = hash.decode('utf-8')
#   x, y, z = np.load("%s/np/%s.npy" % (data_dir, hash))
#   return x, y, z
