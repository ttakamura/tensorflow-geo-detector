import chainer
from chainer import serializers

import cmain
import sys

model = cmain.model()

print(sys.argv[0])
print(sys.argv[1])

1/0

serializers.load_npz('', model)
