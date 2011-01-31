import numpy
import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=4000000)

s = plt.imread("2.png")

# Note the use of unpacking and the : index to select all from that dimension
r, g, b = (s[:,:,i] for i in range(3))

# numpy arrays support whole-array operations.
# Never use loops if you can avoid it
lumin = numpy.floor(256*(0.3*r+0.59*g+0.11*b))
rgb = numpy.floor(256*(numpy.average(s, 2)))

histrange = range(256)
# unpacking again, also - always try to find a built-in function to do what you want.
lumin_hist, rgb_hist = (numpy.histogram(item.flat, histrange)[0] for item in [lumin, rgb])

# use loops for repetitive code.  Also note the use of the enumerate function
for i, title in enumerate(['Red', 'Green', 'Blue']):
   plt.subplot(2, 3, i+1)
   plt.title(title)
   plt.imshow(s[:, :, i], cmap=plt.cm.binary)

plt.subplot(2, 3, 4)
plt.title("Luminosity")
plt.plot(lumin_hist)

plt.subplot(2, 3, 5)
plt.title("RGB Brightness")
plt.plot(rgb_hist)

plt.show()

