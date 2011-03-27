from __future__ import division
import numpy, Image, math, csv
import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=4000000)
FileCSV = csv.writer(open('PVC_1.csv','ab'))
ImageName = 'C19R01' 
region = Image.open(ImageName+'.png')   

ArrPic = numpy.array(region)

R, G, B = (ArrPic[:,:,i] for i in range(3))

Ravg = numpy.zeros( (len(R[:,1])) )
Gavg = numpy.zeros( (len(G[:,1])) )
Bavg = numpy.zeros( (len(B[:,1])) )

for k in range(len(R[:,1])):
    Ravg[k] = numpy.mean(R[k,:])/2.54
    Gavg[k] = numpy.mean(G[k,:])/2.54
    Bavg[k] = numpy.mean(B[k,:])/2.54

for j in range (2000):
    if Ravg[j] >90:
        startpoint = j+30
            
Ravg0 = numpy.mean(Ravg[startpoint:startpoint+20])
Gavg0 = numpy.mean(Gavg[startpoint:startpoint+20])
Bavg0 = numpy.mean(Bavg[startpoint:startpoint+20])
RoverB = Ravg/Bavg
RoverG = Ravg/Gavg

ERGB = numpy.zeros(len(Ravg))

for n in range(len(ERGB)):
    ERGB[n] = math.log10(100/Bavg[n]) + 0.95*math.log10(100/Gavg[n]) + 0.922*(100/Ravg[n])
        
step = len(Ravg[startpoint:len(Ravg)])
length = step*0.08416
time = (length/300)*180
Xax = range(step)
Xax2 = numpy.zeros( (len(Xax)) )
for l in range(len(Xax)):
    Xax2[l] = Xax[l]/step*time
    
m=startpoint
Pink = 0
while Pink == 0 :
   m = m+1
   if RoverB[m] > 1.05*(numpy.mean(RoverB[startpoint:(startpoint+10)])):
       Pink = ((m-startpoint)/step*time,(m-startpoint)/step*time)

m=startpoint
Yellow = 0
while Yellow == 0:
    m = m+1
    if RoverG[m] > 1.15*(numpy.mean(RoverG[startpoint:(startpoint+10)])):
        Yellow = ((m-startpoint)/step*time,(m-startpoint)/step*time)
        
m=startpoint
Black = 0
while Black == 0:
    m = m+1
    if numpy.mean([Ravg[m],Gavg[m],Bavg[m]]) < 10:
        Black = ((m-startpoint)/step*time,(m-startpoint)/step*time)
    if m ==len(Ravg)-1:
        Black = (1, 1)    
        

plt.plot()
plt.plot(Xax2,ERGB[startpoint:len(Bavg)])
plt.title('Please select the start and finish of  the second straight line')
setX = plt.ginput(2)
plt.close()
setX = numpy.array(setX)

FitData1 = ERGB[startpoint:numpy.int(setX[0,0])*step/time+startpoint]
FitData2 = ERGB[numpy.int(setX[0,0])*step/time+startpoint:numpy.int(setX[1,0])*step/time+startpoint]
xFit1 = range(len(FitData1))
x2s = numpy.int((setX[0,0])*step/time)
x2f = numpy.int((setX[1,0])*step/time)
xFit2 = range(x2s,x2f,1)

for l in range(len(xFit1)):
    xFit1[l] = xFit1[l]/step*time
for l in range(len(xFit2)):
    xFit2[l] = xFit2[l]/step*time

for k in range(len(FitData1)):    
    if FitData1[k] == numpy.inf:
        FitData1[k] = FitData1[k-1] 
for k in range(len(FitData2)):    
    if FitData2[k] == numpy.inf:
        FitData2[k] = FitData2[k-1]        
    
   
RateG1 = numpy.polyfit(range(len(FitData1)),FitData1,1)
RateG2 = numpy.polyfit(range(len(FitData2)),FitData2,1)
yFit1 = numpy.zeros(len(xFit1))
yFit2 = numpy.zeros(len(xFit2))
for k in range(len(xFit1)):
    yFit1[k] = k*RateG1[0]+RateG1[1]
for k in range(len(xFit2)):
    yFit2[k] = k*RateG2[0]+RateG2[1]    

FileCSV.writerow([ImageName, Pink[0], Yellow[0], Black[0], RateG1[0]])
plt.plot()      
y = 0,100       
plt.subplot(311)
plt.plot(Xax2,Ravg[startpoint:len(Ravg)],'r')
plt.plot(Xax2,Gavg[startpoint:len(Gavg)],'g')
plt.plot(Xax2,Bavg[startpoint:len(Bavg)],'b')
if Black > 1:
    plt.plot(Black,y,'k',label = 'Black')
plt.plot(Yellow,y,'y',label = 'Yellows')
plt.plot(Pink,y,'pink',label = 'Pinking')
plt.xlabel("Time")
plt.xlim(0,time)
plt.ylabel("Reflectance %")
plt.legend()

pltIm1 = region.transpose(Image.ROTATE_90)
pltIm = pltIm1.transpose(Image.FLIP_TOP_BOTTOM)
pltImArr = numpy.array(pltIm)
s = (startpoint,0,len(pltImArr[1,:]),len(pltImArr[:,1]))
cropIm = pltIm.crop(s)

plt.subplot(312)
plt.imshow(cropIm)

plt.subplot(313)
plt.plot(xFit1,yFit1)
plt.plot(xFit2,yFit2)
plt.plot(Xax2,ERGB[startpoint:len(Bavg)])
plt.xlim(0,time)
plt.savefig(ImageName+"_Analysed.png")
plt.show()



