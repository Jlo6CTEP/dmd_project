import random
import re

file = r".\sample_data\terminal\email.txt"
k = open(file, 'r').read().replace('\n', ',')
open(file, 'w').write(k)
