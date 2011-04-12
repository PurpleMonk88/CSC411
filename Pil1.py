from __future__ import division
import numpy, Image, math, csv
import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=4000000)

#Open Image and CSV files and put them into Arrays
FileCSV = csv.writer(open('PVC_1.csv','ab'))
ImageName = 'C12R01' 
region = Image.open(ImageName+'.png')   
ArrPic = numpy.array(region)
R, G, B = (ArrPic[:,:,i] for i in range(3))
Etot1 = 10000000000

#Define matrices and arrays 
Ravg = numpy.zeros( (len(R[:,1])) )
Gavg = numpy.zeros( (len(G[:,1])) )
Bavg = numpy.zeros( (len(B[:,1])) )
R2 = numpy.zeros( (len(R[:,1])) )
G2 = numpy.zeros( (len(G[:,1])) )
B2 = numpy.zeros( (len(B[:,1])) )
ERGB = numpy.zeros(len(Ravg))
Etot = numpy.zeros(len(Ravg))

#Find the RGB average values accross the width of the strip
for k in range(len(R[:,1])):
    Ravg[k] = numpy.median(R[k,:])/2.54
    Gavg[k] = numpy.median(G[k,:])/2.54
    Bavg[k] = numpy.median(B[k,:])/2.54

#Find the startpoint of the strip
for j in range (2000):
    if Ravg[j] >90:
        startpoint = j+50
        
#Smooth out any spikes in the data
for k in range(len(Ravg)-startpoint):
    if Ravg[k+startpoint]>1.15*Ravg[k+startpoint-1]:
        Ravg[k+startpoint]=numpy.median(Ravg[k+startpoint-20:k+startpoint-1])
    if Gavg[k+startpoint]>1.15*Gavg[k+startpoint-1]:
        Gavg[k+startpoint]=numpy.median(Gavg[k+startpoint-20:k+startpoint-1])
    if Bavg[k+startpoint]>1.15*Bavg[k+startpoint-1]:
        Bavg[k+startpoint]=numpy.median(Bavg[k+startpoint-20:k+startpoint-1])
        
#Smooth the data slighlty by using the median values of the next 40 pixels
for k in range(len(Ravg)-50):
    if k>50:
        R2[k] = numpy.median(Ravg[k-50:k+50])
        G2[k] = numpy.median(Gavg[k-50:k+50])
        B2[k] = numpy.median(Bavg[k-50:k+50])
    else:
        R2[k] = numpy.median(Ravg[k:k+50])
        G2[k] = numpy.median(Gavg[k:k+50])
        B2[k] = numpy.median(Bavg[k:k+50])

#Use the startpoint values for reverence for finding the pinking and yellowing points            
Ravg0 = numpy.mean(R2[startpoint:startpoint+20])
Gavg0 = numpy.mean(G2[startpoint:startpoint+20])
Bavg0 = numpy.mean(B2[startpoint:startpoint+20])
RoverB = R2/B2
RoverG = R2/G2

#Find the ERGB values to be used to get the rate values
for n in range(len(ERGB)):
    #ERGB[n] = math.log10(100/Bavg[n]) + 0.95*math.log10(100/Gavg[n]) + 0.922*(100/Ravg[n])
    ERGB[n] = math.log10(100/B2[n]) + 0.95*math.log10(100/G2[n]) + 0.922*(100/R2[n])
for k in range(len(ERGB)):
    if ERGB[k] == numpy.inf :
        ERGB[k] = ERGB[k-1]
    
#Set up range for plotting the RGB values and time steps as well as the overall time
step = len(Ravg[startpoint:len(Ravg)])
length = step*0.08416
time = (length/300)*180
Xax = range(step)
Xax2 = numpy.zeros( (len(Xax)) )
for l in range(len(Xax)):
    Xax2[l] = Xax[l]/step*time

#Find the pinking point
m=startpoint
Pink = 0
while Pink == 0 :
   m = m+1
   if RoverB[m] > 1.05*(numpy.mean(RoverB[startpoint:(startpoint+10)])):
       Pink = ((m-startpoint)/step*time,(m-startpoint)/step*time)

#Find the Yellowing point
m=startpoint
Yellow = 0
while Yellow == 0:
    m = m+1
    if RoverG[m] > 1.15*(numpy.mean(RoverG[startpoint:(startpoint+10)])):
        Yellow = ((m-startpoint)/step*time,(m-startpoint)/step*time)

#Find the total degradation point if there is one
m=startpoint
Black = 0
while Black == 0:
    m = m+1
    if numpy.mean([Ravg[m],Gavg[m],Bavg[m]]) < 10:
        Black = ((m-startpoint)/step*time,(m-startpoint)/step*time)
    if m ==len(Ravg)-1:
        Black = (numpy.nan, numpy.nan)    
        
#Code used for finding the kinetics that best fit the ERGB data
for a in range(len(ERGB)):
    x0 = startpoint
    x1  = a+startpoint+1
    if Black[0]>0:
        x2 = int(Black[0]*step/time)+startpoint
    else:
        x2 = len(ERGB)-1
    FitData1 = ERGB[x0:x1]
    FitData2 = ERGB[x1:x2]
    if FitData2 == []:
        break
    xFit1 = range(len(FitData1))    
    xFit2 = range(x1-startpoint,x2-startpoint,1)
    Ratekm1 = (ERGB[x1]-ERGB[x0])/(x1-x0)
    Ratekm2 = (ERGB[x2]-ERGB[x1])/(x2-x1)
    Ratekc1 = ERGB[x1]-Ratekm1*x1
    Ratekc2 = ERGB[x2]-Ratekm2*x2   
    for k in range(len(FitData1)):    
        if FitData1[k] == numpy.inf:
            FitData1[k] = FitData1[k-1] 
    for k in range(len(FitData2)):    
        if FitData2[k] == numpy.inf:
            FitData2[k] = FitData2[k-1]
    yFit1 = numpy.zeros(len(xFit1))
    yFit2 = numpy.zeros(len(xFit2))
    for k in range(len(xFit1)):
        yFit1[k] = k*Ratekm1+Ratekc1   
    for k in range(len(xFit2)):
        j = k+x1
        yFit2[k] = j*Ratekm2+Ratekc2 
    Err1 = numpy.sum(numpy.abs(yFit1-ERGB[x0:x1]))
    Err2 = numpy.sum(numpy.abs(yFit2-ERGB[x1:x2]))
    Etot[a] = Err1+Err2 
    #print(Etot[a])
    if Black[1]>0 and (len(ERGB[a+1+startpoint:Black[1]*step/time+startpoint]))<2:
        break
    elif len(ERGB[a+1+startpoint:len(ERGB)*step/time]) < 2 :
        break    
    
 #FitData1 = ERGB[startpoint:a+1+startpoint]     
 #   if Black[1]>0:
 #       FitData2 = ERGB[a+1+startpoint:Black[1]*step/time+startpoint]
 #   else:
 #       FitData2 = ERGB[a+1+startpoint:len(ERGB)*step/time]
 #   xFit1 = range(len(FitData1))
 #   if FitData2 == []:
 #       break
 #   x2s = a+1
 #   if Black[1]>0:
 #       x2f = int((Black[1])*step/time)
 #   else:
 #       x2f = int(len(ERGB[a+startpoint:len(ERGB)*step/time]))
 #   xFit2 = range(x2s,x2f,1)
 #   for l in range(len(xFit1)):
 #       xFit1[l] = xFit1[l]/step*time
 #   for l in range(len(xFit2)):
 #       xFit2[l] = xFit2[l]/step*time
 #   for k in range(len(FitData1)):    
 #       if FitData1[k] == numpy.inf:
 #           FitData1[k] = FitData1[k-1] 
 #   for k in range(len(FitData2)):    
 #       if FitData2[k] == numpy.inf:
 #           FitData2[k] = FitData2[k-1]           
 #   RateG1 = numpy.polyfit(range(len(FitData1)),FitData1,1)
 #   RateG2 = numpy.polyfit(range(len(FitData2)),FitData2,1)
 #   yFit1 = numpy.zeros(len(xFit1))
 #   yFit2 = numpy.zeros(len(xFit2))
 #   for k in range(len(xFit1)):
 #       yFit1[k] = k*RateG1[0]+RateG1[1]
 #   for k in range(len(xFit2)):
 #       yFit2[k] = k*RateG2[0]+RateG2[1]    
 #   Err1 = numpy.sum(numpy.abs(yFit1-ERGB[startpoint:a+1+startpoint]))
 #   if Black[1]>0:
 #       Err2 = numpy.sum(numpy.abs(yFit2-ERGB[a+1+startpoint:Black[1]*step/time+startpoint]))
 #   else:
 #       Err2 = numpy.sum(numpy.abs(yFit2-ERGB[a+1+startpoint:(len(ERGB)-1)*step/time]))
 #   Etot[a] = Err1+Err2  
 #   if Black[1]>0 and (len(ERGB[a+1+startpoint:Black[1]*step/time+startpoint]))<2:
 #       break
 #   elif len(ERGB[a+1+startpoint:len(ERGB)*step/time]) < 2 :
 #       break

Estore = 10000000
for k in range(len(Etot)):
    if Etot[k] == 0:
         Etot[k] = 1000000;
    if Etot[k]<Estore:
        Estore = Etot[k]
        split = k

x1  = split+startpoint
FitData1 = ERGB[x0:x1]
FitData2 = ERGB[x1:x2]
xFit1 = range(len(FitData1))
xFit2 = range(x1-startpoint,x2-startpoint,1)
for l in range(len(xFit1)):
    xFit1[l] = xFit1[l]/step*time
for l in range(len(xFit2)):
    xFit2[l] = xFit2[l]/step*time
Ratekm1 = (ERGB[x1]-ERGB[x0])/(x1-x0)
Ratekm2 = (ERGB[x2]-ERGB[x1])/(x2-x1)
Ratekc1 = ERGB[x0]-Ratekm1*x0
Ratekc2 = ERGB[x1]-Ratekm2*x1
for k in range(len(FitData1)):    
    if FitData1[k] == numpy.inf:
        FitData1[k] = FitData1[k-1] 
for k in range(len(FitData2)):    
    if FitData2[k] == numpy.inf:
        FitData2[k] = FitData2[k-1]
yFit1 = numpy.zeros(len(xFit1))
yFit2 = numpy.zeros(len(xFit2))
for k in range(len(xFit1)):
    yFit1[k] = k*Ratekm1+Ratekc1
for k in range(len(xFit2)):
    j = k+x1
    yFit2[k] = j*Ratekm2+Ratekc2


#FitData1 = ERGB[startpoint:split+startpoint]
#if Black[1]>0:
#       FitData2 = ERGB[split+startpoint:Black[1]*step/time+startpoint]
#else:
#    FitData2 = ERGB[split+startpoint:len(ERGB)*step/time]
#xFit1 = range(len(FitData1))
#x2s = split
#if Black[1]>0:
#    x2f = numpy.int((Black[1])*step/time)
#else:
#    x2f = numpy.int(len(ERGB))
#xFit2 = range(x2s,x2f,1)
#for l in range(len(xFit1)):
#    xFit1[l] = xFit1[l]/step*time
#for l in range(len(xFit2)):
#    xFit2[l] = xFit2[l]/step*time
#for k in range(len(FitData1)):    
#    if FitData1[k] == numpy.inf:
#        FitData1[k] = FitData1[k-1] 
#for k in range(len(FitData2)):    
#    if FitData2[k] == numpy.inf:
#        FitData2[k] = FitData2[k-1]           
#RateG1 = numpy.polyfit(range(len(FitData1)),FitData1,1)
#RateG2 = numpy.polyfit(range(len(FitData2)),FitData2,1)
#yFit1 = numpy.zeros(len(xFit1))
#yFit2 = numpy.zeros(len(xFit2))
#for k in range(len(xFit1)):
#    yFit1[k] = k*RateG1[0]+RateG1[1]
#for k in range(len(xFit2)):
#    yFit2[k] = k*RateG2[0]+RateG2[1]           

FileCSV.writerow([ImageName, Pink[0], Yellow[0], Black[0], Ratekm1,Ratekm2])
plt.plot()      
y = 0,100
plt.subplots_adjust(hspace = 0.0001)
#Plot the image of the strip
pltIm1 = region.transpose(Image.ROTATE_90)
pltIm = pltIm1.transpose(Image.FLIP_TOP_BOTTOM)
pltImArr = numpy.array(pltIm)
s = (startpoint,0,len(pltImArr[1,:]),len(pltImArr[:,1]))
cropIm = pltIm.crop(s)
plt.subplot(311)
plt.imshow(cropIm)
plt.xticks(visible =False)
plt.yticks(visible =False) 
      
#Plot RGB values, which have been smoothed
ax1 = plt.subplot(312)
plt.plot(Xax2,R2[startpoint:len(Ravg)],'r')
plt.plot(Xax2,G2[startpoint:len(Gavg)],'g')
plt.plot(Xax2,B2[startpoint:len(Bavg)],'b')
if Black > 0:
    plt.plot(Black,y,'k',label = 'Black')
plt.plot(Yellow,y,'y',label = 'Yellows')
plt.plot(Pink,y,'pink',label = 'Pinking')
plt.xlim(0,time)
plt.ylabel("Reflectance %")
plt.legend()

#Plot the ERGB data as well as the fitted rates to the data
if Black[1]>0:
    Xax3 = numpy.zeros(len(ERGB[startpoint:Black[1]*step/time])+startpoint)
    for l in range(len(ERGB[startpoint:Black[1]*step/time])+startpoint):
        Xax3[l] = Xax[l]/step*time
 
plt.subplot(313,sharex = ax1)
plt.plot(xFit1,yFit1,'k')
plt.plot(xFit2,yFit2,'g')
plt.xlabel("Time")
plt.ylabel("ERGB value")
plt.xlim(0,time)
if Black[1] >0:
    plt.xlim(0,time)
    plt.ylim(0,0.5+numpy.max(ERGB[startpoint:Black[1]*step/time+startpoint]))
    plt.plot(Xax3,ERGB[startpoint:Black[1]*step/time+startpoint])
else:
    plt.plot(Xax2,ERGB[startpoint:len(Bavg)]) 
    
plt.savefig(ImageName+"_Analysed.png")
plt.show()



