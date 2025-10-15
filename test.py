"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

#https://matplotlib.org/stable/gallery/mplot3d/contour3d_3.html
ax = plt.figure().add_subplot(projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
print(axes3d.get_test_data(0.05))


ax.plot_surface(X, Y, Z, edgecolor='royalblue', lw=0.5, rstride=8, cstride=8, alpha=0.3)
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
plt.show()
"""


import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set up grid and test data
nx, ny = 256, 1024
x = range(nx)
y = range(ny)

data = numpy.random.random((nx, ny))

hf = plt.figure()
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
ha.plot_surface(X.T, Y.T, data)

plt.show()
