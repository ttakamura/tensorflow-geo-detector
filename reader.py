import numpy as np

def load_train_data(ids, xdata, ydata, zdata, batch_size):
  xdata = np.array(xdata)
  ydata = np.array(ydata)
  zdata = np.array(zdata)
  # TODO
  # np.random.shuffle(ids)
  return xdata, ydata, zdata

def split_data(data):
  data_num   = len(data)
  train_num  = int(data_num * 0.7)
  test_num   = int(data_num * 1.0)
  train_data = list()
  test_data  = list()

  for row in data[0:train_num]:
    train_data.append(row)

  for row in data[train_num:test_num]:
    test_data.append(row)

  return train_data, test_data

def load_master_data(data_dir):
  x, y, z, ids, vocabrary = np.load("%s/np/main.np.npy" % data_dir)
  np.random.shuffle(ids)
  return x, y, z, ids, vocabrary

# def load_doc_data(hash, data_dir):
#   if type(hash) == bytes:
#     hash = hash.decode('utf-8')
#   x, y, z = np.load("%s/np/%s.npy" % (data_dir, hash))
#   return x, y, z
