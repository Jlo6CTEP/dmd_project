f = open('.\\sample_data\\terminal\\color.txt', 'r').read()
f = f.replace('color_', '')
print(f)
f = open('.\\sample_data\\terminal\\color.txt', 'w').write(f)
