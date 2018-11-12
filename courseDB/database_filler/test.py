import random
x = lambda: random.sample(range(1, 100), 1)
f = []
[f.append(x()[0]) for l in range(50)]
print([f.count(x) for x in range(100)])