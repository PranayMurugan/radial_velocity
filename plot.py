from matplotlib import pyplot as plt
from matplotlib import style

from numpy import genfromtxt

data = genfromtxt('GfG.csv',delimiter=',')

plt.plot(data)

plt.title('Epic Info')
plt.ylabel('Y axis')
plt.xlabel('X axis')

plt.show()
