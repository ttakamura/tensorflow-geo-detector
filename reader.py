import numpy as np

def load_train_data(ids, data_dir):
  np.random.shuffle(ids)
  data_num   = len(ids)
  train_num  = floor(data_num * 0.7)
  test_num   = floor(data_num * 1.0)
  train_data = list()
  test_data  = list()

  for id, hash, category in ids[0:train_num]:
    x, y, z = load_doc_data(hash, data_dir)
    print(x.shape)
    print(y.shape)
    print(z.shape)
    train_data.append({ 'x':x, 'y':y, 'z':z })

  for id, hash, category in ids[train_num:test_num]:
    x, y, z = load_doc_data(hash, data_dir)
    test_data.append({ 'x':x, 'y':y, 'z':z })

  return train_data, test_data

def load_doc_data(hash, data_dir):
  x, y, z = np.load("%s/np/%s.npy" % (data_dir, hash))
  return x, y, z

def load_master_data(data_dir):
  ids, vocabrary = np.load("%s/np/main.np.npy" % data_dir)
  np.random.shuffle(ids)
  return ids, vocabrary
