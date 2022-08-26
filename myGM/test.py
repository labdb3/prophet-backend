import numpy as np

a = np.ones((3,3))
b = a[1,:]
b = np.append(b,2)
print(b)