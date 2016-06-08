import numpy as np

def load_train_data(ids, xdata, ydata, zdata, batch_size):
  xdata = np.array(xdata)
  ydata = np.array(ydata)
  zdata = np.array(zdata)
  # TODO
  # np.random.shuffle(ids)
  return xdata, ydata, zdata

def split_data(allx, ally):
  data_num     = len(allx)
  train_num    = int(data_num * 0.7)
  test_num     = int(data_num * 1.0)
  train_x_data = list()
  test_x_data  = list()
  train_y_data = list()
  test_y_data  = list()

  for xrow in allx[0:train_num]:
    train_x_data.append(xrow)

  for xrow in allx[train_num:test_num]:
    test_x_data.append(xrow)

  for yrow in ally[0:train_num]:
    train_y_data.append(yrow)

  for yrow in ally[train_num:test_num]:
    test_y_data.append(yrow)

  return train_x_data, test_x_data, train_y_data, test_y_data

def load_master_data(data_dir):
  x, y, z, ids, vocabrary = np.load("%s/np/main.np.npy" % data_dir)
  np.random.shuffle(ids)
  return x, y, z, ids, vocabrary

# def load_doc_data(hash, data_dir):
#   if type(hash) == bytes:
#     hash = hash.decode('utf-8')
#   x, y, z = np.load("%s/np/%s.npy" % (data_dir, hash))
#   return x, y, z
