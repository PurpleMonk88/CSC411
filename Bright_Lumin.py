import numpy
import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=4000000)

s = plt.imread("1.png")
s0 = numpy.zeros( (400,265) )
s1 = numpy.zeros( (400,265) )
s2 = numpy.zeros( (400,265) )
rgb = numpy.zeros( (400,265) )
lumin = numpy.zeros( (400,265) )
lumin_hist = numpy.zeros( (256) )
rgb_hist = numpy.zeros( (256) )
x = numpy.zeros( ( 256) )
k =0
j =0

for k in range(400):
   
   for j in range(265):
      lumin[k,j] = numpy.floor(256*(0.3*(s[k,j,0])+0.59*(s[k,j,1])+0.11*(s[k,j,2])))
      rgb[k,j] = numpy.floor(256*(s[k,j,0]/3 + s[k,j,1]/3 + s[k,j,2]/3))
      s0[k,j] = 1-s[k,j,0]
      s1[k,j] = 1-s[k,j,1]
      s2[k,j] = 1-s[k,j,2]
      
      for l in range(256):
         x[l] = l
         if lumin[k,j] == l:
            lumin_hist[l] += 1
         if rgb[k,j] == l:
            rgb_hist[l] +=1
          
#print(lumin_hist)
#print(rgb_hist)

plt.subplot(231)
plt.title("Red")
g0 =plt.imshow(s0,cmap=plt.cm.binary)

plt.subplot(232)
plt.title("Green")
g1 =plt.imshow(s1,cmap=plt.cm.binary)

plt.subplot(233)
plt.title("Blue")
g2 =plt.imshow(s2,cmap=plt.cm.binary)

plt.subplot(234)
plt.title("Luminoscity")
plt.plot(x,lumin_hist)

plt.subplot(235)
plt.title("RGB Brightness")
plt.plot(x,rgb_hist)

plt.show()

