# coding: utf-8
#
# data.csv と html doc から numpy 互換のデータを生成する
#
import numpy as np
from scipy.sparse import *
import csv

base_dir = 'tabelog_final_s'
csv_file = ('%s/data.csv' % base_dir)
doc_dir  = ('%s/docs/' % base_dir)

vocabrary     = {}
vocab_counter = {}

data_num  = 0
max_step  = 0
max_vocab = 0

def add_vocab(text):
  if not text in vocabrary:
    vocabrary[text] = len(vocabrary)
    vocab_counter[text] = 1
  else:
    vocab_counter[text] += 1
  return vocabrary[text]

add_vocab('<UNK>')
vocab_counter['<UNK>'] = 100000

def open_csv(doc_dir, csv_file):
  global data_num
  global max_step
  with open(csv_file, 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
      data_num += 1
      step = 0
      id, url, hash, name, addr = row
      html_file = ('%s/%s' % (doc_dir, hash))
      with open(html_file, 'r') as hf:
        tsv_reader = csv.reader(hf, delimiter='\t')
        for tsv_row in tsv_reader:
          step += 1
          if len(tsv_row) == 2:
            token, category = tsv_row
            if type(token) == bytes:
              token = token.decode('utf-8')
            yield data_num, step, token, hash, int(category)
          else:
            yield data_num, step, "", "", int(category)
      if max_step < step:
        max_step = step

for id, step, token, hash, category in open_csv(doc_dir, csv_file):
  add_vocab(token)

def reduce_vocabrary(vocabrary, minimum_vocab):
  return dict([(k,v) for k,v in vocabrary.items() if vocab_counter[k] > minimum_vocab])

def get_vocab_id(vocabrary, key):
  if key in vocabrary:
    return vocabrary[key]
  else:
    return vocabrary['<UNK>']

minimum_vocab = 2000 # 2000 回以上存在するコーパスのみ扱う
vocabrary     = reduce_vocabrary(vocabrary, minimum_vocab)
max_vocab     = len(vocabrary)
x_data_num    = data_num
x_max_step    = max_step + 1
x_max_vocab   = max_vocab

shape     = (x_max_step, x_max_vocab)
yshape    = (x_max_step, 3)
zshape    = (x_max_step, 1)
x_matrixs = list()
y_matrixs = list()
z_matrixs = list()
data_num  = 0
max_step  = 0
last_hash = None
hash_map  = {}

final_result = list()

for id, step, token, hash, category in open_csv(doc_dir, csv_file):
  i = id - 1
  if len(x_matrixs) == i:
    x_matrixs.append(np.zeros(shape))
    y_matrixs.append(np.zeros(yshape))
    z_matrixs.append(np.zeros(zshape))
    final_result.append([id, hash, category])
    hash_map[i] = hash
  x_matrixs[i][step, get_vocab_id(vocabrary, token)] = 1.0
  y_matrixs[i][step, category] = 1.0
  z_matrixs[i][step, 0] = get_vocab_id(vocabrary, token)

for i in range(len(x_matrixs)):
  np_file = ('%s/np/%s' % (base_dir, hash_map[i]))
  np.save(np_file, (x_matrixs[i], y_matrixs[i], z_matrixs[i]))

np_file = ('%s/np/main.np' % base_dir)
np.save(np_file, (np.array(final_result), np.array(vocabrary)))

for key, value in vocabrary.items():
  print("%s\t%s" % (key.encode('utf-8'), value))
