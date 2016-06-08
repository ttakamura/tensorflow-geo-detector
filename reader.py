import numpy as np

def long_sequence_to_batch(sequence, batch_size):
  x_data  = list()
  x_batch = list()
  for i in range(sequence.shape[0]):
    if len(x_batch) == batch_size:
      x_data.append(x_batch)
      x_batch = list()
    x_batch.append(sequence[i,:])
  x_data.append(x_batch)
  return x_data

def load_train_data(ids, xdata, ydata, zdata, batch_size):
  np.random.shuffle(ids)
  data_num = len(ids)
  x_data   = list()
  y_data   = list()
  z_data   = list()
  for i in range(len(xdata)):
    x = xdata[i]
    y = ydata[i]
    z = zdata[i]
    x_data += long_sequence_to_batch(x, batch_size)
    y_data += long_sequence_to_batch(y, batch_size)
    z_data += long_sequence_to_batch(z, batch_size)
  return x_data, y_data, z_data

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
