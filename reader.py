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

def load_train_data(ids, data_dir, batch_size, step_size):
  np.random.shuffle(ids)
  data_num = len(ids)
  x_data   = list()
  y_data   = list()
  z_data   = list()
  for id, hash, category in ids:
    x, y, z = load_doc_data(hash, data_dir)
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

  for id, hash, category in ids[0:train_num]:
    x, y, z = load_doc_data(hash, data_dir)
    train_data.append({ 'x':x, 'y':y, 'z':z })

  for id, hash, category in ids[train_num:test_num]:
    x, y, z = load_doc_data(hash, data_dir)
    test_data.append({ 'x':x, 'y':y, 'z':z })

  return train_data, test_data

def load_doc_data(hash, data_dir):
  x, y, z = np.load("%s/np/%s.npy" % (data_dir, hash.decode('utf-8')))
  return x, y, z

def load_master_data(data_dir):
  ids, vocabrary = np.load("%s/np/main.np.npy" % data_dir)
  np.random.shuffle(ids)
  return ids, vocabrary
