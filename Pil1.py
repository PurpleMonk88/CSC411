from __future__ import division
import numpy, Image, math, csv,glob
import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=4000000)

#Open Image and CSV files and put them into Arrays
CSVname = raw_input('Please enter CSV File name: ')
FileCSV = csv.writer(open(CSVname+'.csv','ab'))
FileCSV.writerow(['Run Name', 'Pinking Time','Yellowing Time', 'Final Degredation Time','K1','K2'])
AllImages = glob.glob('*.png')
for S in range(len(AllImages)):
    ImNameEnd = AllImages[S].find('.')
    ImageName = AllImages[S][0:ImNameEnd]
    print('Busy with Image:'+str(S+1)+' of '+str(len(AllImages)))
    region = Image.open(ImageName+'.png')   
    ArrPic = numpy.array(region)
    R, G, B = (ArrPic[:,:,i] for i in range(3))
    Etot1 = 10000000000
    
    #Define matrices and arrays 
    Ravg = numpy.zeros( (len(R[:,1])) )
    r =   numpy.zeros_like(Ravg)
    Gavg=  numpy.zeros_like(Ravg)
    Bavg = numpy.zeros_like(Ravg)
    R2 =   numpy.zeros_like(Ravg)
    G2 =   numpy.zeros_like(Ravg)
    B2 =   numpy.zeros_like(Ravg)
    ERGB = numpy.zeros_like(Ravg)
    Etot = numpy.zeros_like(Ravg)
    
    #Find the RGB average values accross the width of the strip
    for k in range(len(R[:,1])):
        Ravg[k],Gavg[k],Bavg[k] = (numpy.median(i[k,:])/2.54 for i in (R,G,B))
        
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
    for k in range(len(Ravg)):
        if k>50 and k < (len(Ravg)-50):
            R2[k] = numpy.mean(Ravg[k-50:k+50])
            G2[k] = numpy.mean(Gavg[k-50:k+50])
            B2[k] = numpy.mean(Bavg[k-50:k+50])
        elif k < (len(Ravg)-50):
            R2[k] = numpy.mean(Ravg[k:k+50])
            G2[k] = numpy.mean(Gavg[k:k+50])
            B2[k] = numpy.mean(Bavg[k:k+50])
    
    #Use the startpoint values for reverence for finding the pinking and yellowing points            
    Ravg0,Gavg0,Bavg0 = (numpy.mean(i[startpoint:startpoint+20]) for i in (R2,G2,B2))
    RoverB = R2/B2
    RoverG = R2/G2
    
    #Find the ERGB values to be used to get the rate values
    for n in range(len(ERGB)):
        ERGB[n] = math.log10(100/B2[n]) + 0.95*math.log10(100/G2[n]) + 0.922*(100/R2[n])
    for k in range(len(ERGB)):
        if ERGB[k] == numpy.inf :
            ERGB[k] = ERGB[k-1]
        
    #Set up range for plotting the RGB values and time steps as well as the overall time
    step = len(Ravg[startpoint:len(Ravg)])
    length = step*0.08416
    time = (length/300)*180
    Xax = range(step)
    Xax2 = numpy.zeros(len(Xax))
    for l in range(len(Xax)):
        Xax2[l] = Xax[l]/step*time
    
    #Find the pinking point
    for m in range(startpoint,len(RoverB),1):
       if RoverB[m] > 1.05*(numpy.mean(RoverB[startpoint:(startpoint+10)])):
           Pink = ((m-startpoint)/step*time,(m-startpoint)/step*time)
           break
    
    #Find the Yellowing point
    
    for m in range(startpoint,len(RoverB),1):
        if RoverG[m] > 1.15*(numpy.mean(RoverG[startpoint:(startpoint+10)])):
            Yellow = ((m-startpoint)/step*time,(m-startpoint)/step*time)
            break
            
    #Find the total degradation point if there is one
    Black = (numpy.nan,numpy.nan)
    for m in range(startpoint,len(RoverB),1):
        if numpy.mean([Ravg[m],Gavg[m],Bavg[m]]) < 12:
            Black = ((m-startpoint)/step*time,(m-startpoint)/step*time)
            break
    p = 0
    #Code used for finding the kinetics that best fit the ERGB data
    for a in range(1,len(ERGB),50):
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
        Rate1 = numpy.polyfit(xFit1,FitData1,1)
        Rate2 = numpy.polyfit([x1,x2],[Rate1[0]*x1+Rate1[1],ERGB[x2]],1)
        Ratekm1 = Rate1[0] 
        Ratekm2 = Rate2[0]
        Ratekc1 = Rate1[1]
        Ratekc2 = Rate2[1]
        yFit1 = numpy.zeros(len(xFit1))
        yFit2 = numpy.zeros(len(xFit2))
        for k in range(len(xFit1)):
            j = k+startpoint
            yFit1[k] = j*Ratekm1+Ratekc1   
        for k in range(len(xFit2)):
            j = k+x1
            yFit2[k] = j*Ratekm2+Ratekc2 
        Err1 = numpy.sum(numpy.abs(yFit1-ERGB[x0:x1]))
        Err2 = numpy.sum(numpy.abs(yFit2-ERGB[x1:x2]))
        Etot[a] = Err1+Err2 
        if Black[1]>0 and (len(ERGB[a+1+startpoint:Black[1]*step/time+startpoint]))<2:
            break
        elif len(ERGB[a+1+startpoint:len(ERGB)*step/time]) < 50 :
            break
        
        
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
    Rate1 = numpy.polyfit(xFit1,FitData1,1)
    Rate2 = numpy.polyfit([x1,x2],[Rate1[0]*x1+Rate1[1],ERGB[x2]],1)
    Ratekm1 = Rate1[0]
    Ratekm2 = Rate2[0]
    Ratekc1 = Rate1[1]
    Ratekc2 = Rate2[1]  
    yFit1 = numpy.zeros(len(xFit1))
    yFit2 = numpy.zeros(len(xFit2))
    for k in range(len(xFit1)):
        j = k+startpoint
        yFit1[k] = j*Ratekm1+Ratekc1
    for k in range(len(xFit2)):
        j = k+x1
        yFit2[k] = j*Ratekm2+Ratekc2
    
    for l in range(len(xFit1)):
        xFit1[l] = xFit1[l]/step*time
    for l in range(len(xFit2)):
        xFit2[l] = xFit2[l]/step*time
    
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
    PltImArr = numpy.array(cropIm)
    plt.axes([0.125,0.87,0.775,0.1])
    plt.imshow(cropIm)
    plt.xticks(visible = False)
    plt.yticks(visible =False) 
    
    #Plot RGB values, which have been smoothed
    ax1 = plt.axes([0.125,0.5,0.775,0.4])
    plt.plot(Xax2,R2[startpoint:len(Ravg)],'r')
    plt.plot(Xax2,G2[startpoint:len(Gavg)],'g')
    plt.plot(Xax2,B2[startpoint:len(Bavg)],'b')
    if Black > 0:
        plt.plot(Black,y,'k',label = 'Black')
    plt.plot(Yellow,y,'y',label = 'Yellows')
    plt.plot(Pink,y,'pink',label = 'Pinking')
    plt.xlim(0,time)
    plt.xticks(visible = False)
    plt.ylabel("Reflectance %")
    plt.legend()
    
    #Plot the ERGB data as well as the fitted rates to the data
    if Black[1]>0:
        Xax3 = numpy.zeros(len(ERGB[startpoint:Black[1]*step/time])+startpoint)
        for l in range(len(ERGB[startpoint:Black[1]*step/time])+startpoint):
            Xax3[l] = Xax[l]/step*time
    
    ax3 = plt.subplot(212,sharex = ax1)
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
    plt.clf()
    
print('Done')