import chainer
from chainer import serializers
from IPython import embed

import cmain
import sys

model    = cmain.model()
npy_file = sys.argv[1]
serializers.load_npz(npy_file, model)

embed()
