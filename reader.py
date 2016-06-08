import numpy as np

def load_train_data(ids, xdata, ydata, zdata, batch_size):
  xdata = np.array(xdata)
  ydata = np.array(ydata)
  zdata = np.array(zdata).astype(np.int32)
  # TODO
  # np.random.shuffle(ids)
  return xdata, ydata, zdata

def split_data(allx, ally, allz):
  data_num     = len(allx)
  train_num    = int(data_num * 0.7)
  test_num     = int(data_num * 1.0)
  train_x_data = list()
  test_x_data  = list()
  train_y_data = list()
  test_y_data  = list()
  train_z_data = list()
  test_z_data  = list()

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
