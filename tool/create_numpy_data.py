# coding: utf-8
#
# data.csv と html doc から numpy 互換のデータを生成する
#
import numpy as np
from scipy.sparse import *
import csv

csv_file = 'tabelog_final/data.csv'
doc_dir  = 'tabelog_final/docs/'

vocabrary     = {}
vocab_counter = {}

data_num  = 0
max_step  = 0
max_vocab = 0

def add_vocab(text):
  if not vocabrary.has_key(text):
    vocabrary[text] = len(vocabrary)
    vocab_counter[text] = 1
  else:
    vocab_counter[text] += 1
  return vocabrary[text]

with open(csv_file, 'r') as f:
  csv_reader = csv.reader(f)

  for row in csv_reader:
    data_num += 1
    step = 0
    id, url, hash, name, addr = row
    html_file = ('%s/%s' % (doc_dir, hash))

    with open(html_file, 'r') as hf:
      step += 1
      tsv_reader = csv.reader(hf, delimiter='\t')

      for tsv_row in tsv_reader:
        if len(tsv_row) == 2:
          token, category = tsv_row
          token = token.decode('utf-8')
          add_vocab(token)

    if max_step < step:
      max_step = step

max_vocab = len(vocabrary)
mat = lil_matrix((data_num, max_step, max_vocab))

print(mat)

1 / 0

with open(csv_file, 'r') as f:
  csv_reader = csv.reader(f)
  for row in csv_reader:
    id, url, hash, name, addr = row
    html_file = ('%s/%s' % (doc_dir, hash))
    with open(html_file, 'r') as hf:
      tsv_reader = csv.reader(hf, delimiter='\t')
      for tsv_row in tsv_reader:
        token, category = tsv_row
        token = token.decode('utf-8')
