# coding: utf-8

import scipy.misc
import matplotlib.pyplot as plt

f = scipy.misc.face(gray=True)
f = f[230:290, 220:320]

plt.imshow(f, cmap=plt.cm.gray)
#plt.colorbar()
plt.show()
