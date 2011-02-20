import numpy, Image
import matplotlib.pyplot as plt

Ravg = numpy.zeros( (3249) )
Gavg = numpy.zeros( (3249) )
Bavg = numpy.zeros( (3249) )

numpy.set_printoptions(threshold=4000000)

Im = Image.open('CSC Test1.png')
cropped = (280,133,420,3382)
region =Im.crop(cropped)

ArrPic = numpy.array(region)

R, G, B = (ArrPic[:,:,i] for i in range(3))

pltIm = region.transpose(Image.ROTATE_90)
pltImArr = numpy.array(pltIm)

for k in range(len(R[:,1])):
    Ravg[k] = sum(R[k,:])/len(R[1,:])
    Gavg[k] = sum(G[k,:])/len(G[1,:])
    Bavg[k] = sum(B[k,:])/len(B[1,:])
    
Xax = range(len(R[:,1]))
plt.subplot(211)
plt.plot(Xax,Ravg,'r')
plt.plot(Xax,Gavg,'g')
plt.plot(Xax,Bavg,'b')
plt.xlim(0,len(Ravg))

plt.subplot(212)
plt.imshow(pltImArr)
plt.show()
