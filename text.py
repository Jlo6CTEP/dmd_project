import re
file = r".\sample_data\static\shape.txt"
k = open(file, 'r').read()

k = k.replace('\n', ',')

#print(f)
open(file, 'w').write(k)
