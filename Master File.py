# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:34:41 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare 
from matplotlib.colors import LogNorm
from mpl_toolkits.mplot3d import Axes3D

'''-------------------------------Task 1------------------------------------'''
'''
In the fist task we have been asked to investegate two different methods for 
creating a distribution of random numbers proportinal to a sine curve btween 0
and pi.
'''

def AnalyticalSinDistribution(N=1):
    '''
    This function returns a list of random angles in a distribution that is 
    proportinal to sin(theta) between 0 and pi. A uniform distribution is 
    generated and then transformed into a non uniform distribution using 
    inverse transorm sampling. N is the size of the list returned.
    '''
    N=int(N)
    Rand=np.random.rand(N)
    return np.arccos(1-2*Rand)

def AcceptRegect(f,a,b,c,d,N=1):
    '''
    This function returns a list of random numbers in a distribution that is 
    proportinal to a specified function, f. a and b are the limits of the domain
    of f you are interested in and c and d are the limits of the range over
    the specifeid domain. This function works by generating a random x' value
    and y' value. The function f is the applied to x' generating a ymax value if
    the y' value is greater then the ymax value then x value is ignored. If the
    y value is less then the ymax value the x value is appended to a list. Note
    this method only works for postive ranges.
    '''
    N=int(N)
    X=[]
    for i in range(N):
        xprime=np.random.uniform(a,b)
        yprime=np.random.uniform(c,d)
        ymax=f(xprime)
        if yprime<ymax:
            X+=[xprime]
    return X    

def SineFitting(x,A,B):
    '''
    This function returns a scaled sine curve that can be used to fit the histogram
    data produced in the first task.
    '''
    return A*np.sin(x)+B

def Fitting(X,TheorticalFit,NumBins,Title,Xlabel,Plot=True):
    '''
    This function fits a specified theoritcal fit to a histogram and returns
    a chis squared value. X is the histogram data that we want to fit, 
    TheorticalFit is the theoretical distribution of our data and NumBins
    is the number of bins we want our data to be fitted to.
    '''
    NumBins=int(NumBins)
    BinValue,BinEdgevalue=np.histogram(X,NumBins)
    #The histogram function returns the bin edge value and not the 
    #mid point (bin position) so these need to be calculated.
    BinPosition=[]
    for i in range(NumBins):
        BinPosition+=[(BinEdgevalue[i]+BinEdgevalue[i+1])/2]
    
    #The bellow function is from the SciPy libary and calculates the parameters
    #needed to scale the theoritical fit to the random distributions. The paramaters 
    #are calculated by reducing the residual of the TheorticalFit against the
    #random distribution.
    ScalingParameters=curve_fit(TheorticalFit,BinPosition,BinValue)[0]
    FittingCurve=TheorticalFit(BinPosition,ScalingParameters[0],ScalingParameters[1])
    
    if Plot==True:
        plt.title(Title)
        plt.hist(X,NumBins)
        plt.plot(BinPosition,FittingCurve)
        plt.ylabel('Frequency')
        plt.xlabel(Xlabel)
        plt.show()
        plt.clf()
        
    #To calculate the reduced chisquare we need to know the number of degrees of 
    #freedom. The degrees of freedom is given by the number of bins subtracted
    #by the number of parameters used too fit the curve in our case 2.
    DegreesOfFreedom=NumBins-2
    return chisquare(BinValue,FittingCurve)[0]/DegreesOfFreedom


x=AnalyticalSinDistribution(1e4)
print('The reduced chi squared of our fit is '+str(Fitting(x,SineFitting,100,'Analytical method','Angle $\\theta$',Plot=True)))

y=AcceptRegect(np.sin,0,np.pi,0,1,1e4)

print('The reduced chi squared of our fit is '+str(Fitting(y,SineFitting,100,'Reject accept method','Angle $\\theta$',Plot=True)))

#The commented out code is what was used to compare the times of the different methods.
#The time values and errors where found by using %timeit function in the I python 
#consol.

#X=np.array([1000,5000,10000,15000,20000,25000,30000,35000,40000,45000])
#
#AnalyticalMethod=np.array([0.000036,0.000159,0.000325,0.000505,0.00063,0.000798,0.000957,0.00105,0.00118,0.00132])
#RejectMethod=np.array([0.00316,0.0165,0.0344,0.0497,0.0653,0.0839,0.0978,0.117,0.135,0.154])
#
#AnalyticalMethodError=np.array([0.000001,0.000002,0.00002,0.00004,0.00003,0.00004,0.00007,0.00003,0.00003,0.000015])
#RejectMethodError=np.array([0.0001,0.0004,0.001,0.003,0.001,0.005,0.002,0.005,0.004,0.008])
#
#f, axarr = plt.subplots(2, sharex=True)
#xp=X
#z = np.polyfit(X,AnalyticalMethod,1)
#p = np.poly1d(z)
#axarr[0].plot(X,AnalyticalMethod,'.',xp,p(xp),'--')
#axarr[0].errorbar(X,AnalyticalMethod , yerr=AnalyticalMethodError, fmt='.')
#
#z1 = np.polyfit(X,RejectMethod,1)
#p1 = np.poly1d(z1)
#axarr[1].plot(X,RejectMethod,'.',xp,p1(xp),'--')
#axarr[1].errorbar(X,RejectMethod , yerr=RejectMethodError, fmt='.')
#axarr[0].set(ylabel='Time (s)')
#axarr[1].set(ylabel='Time (s)')
#axarr[1].set(xlabel='Number of samples')
#axarr[0].set_title('Inverse transform sampling')
#axarr[1].set_title('Rejection sampling')
#plt.savefig('Time', dpi=250)
#plt.show()
#plt.clf()

  
'''-------------------------------Task 2------------------------------------'''
'''
For the second exercise we were asked to calculate the distribution of gamma 
ray on a 2D array. The gamma rays are produced by a unstable particles that are 
traveling at 2000m/s perpendicular to our array. To produce the gamma ray 
distribution I had to solve 3 main problems the position each particle decays, 
the direction the particle is moving in after it decays and the position of the
gamma rays that reach the array.
'''
MeanDecayTime=550e-6
def DecayPosition(xgen):
    '''
    Returns random decay position of particle. The random distribution for
    a large number of particles is exponential. The method used to produce
    the random distribution is the inverse sampling method.
    '''
    DecayConstant=1/MeanDecayTime
    Normalisation=-DecayConstant/(2000*(np.exp(-DecayConstant/1000)-1))
    #Nomalisation is very important. It means the random positions produced will
    #all be within our required range (between ingection point and screen).
    #Normalisation factor is calculated by intergrating a exponential
    #decay function across our range.
    return -(2000/DecayConstant)*np.log(1-(DecayConstant/(2000*Normalisation))*xgen)

def DecayAngles(N,Isotropic=True):
    '''
    This function returns a random distribution of angles. If Isotropic is true 
    then the angles will be distributed isotropically. If isotropic is false then 
    the theta and phi angles will be distributed uniformly.
    '''
    N=int(N)
    theta=np.random.uniform(0,2*np.pi,N)
    if Isotropic==True:
        #Size of differential surface element gets smaller as you approach the 
        #poles of a sphere. So to get a truly isotropic angular distribution in 
        #spherical corrdinates less angles need to be produced around the pole 
        #positions. This is explained more in the report.
        phi=np.arccos(1-2*np.random.uniform(0,1,N))
    elif Isotropic==False:
        phi=np.random.uniform(0,np.pi,N)
    return theta,phi

def ScreenPositions(N,ScreenSize):
    '''
    This function calculates the position of the gamma rays from the particle decays
    on a square screen. The number of particles and the screens dimensions can be edited. 
    '''
    N=int(N)
    Rand=np.random.rand(N)
    #The decay position and angles are generated for N particles.
    DecayPos=DecayPosition(Rand)
    Theta,Phi=DecayAngles(N)
    X=[]
    Y=[]
    for i in range(N):
        #Using trig I was able to work out the position the gamma ray hit on a 2D
        #plane placed 2m away from ingection point of the particles.
        Distance=2-DecayPos[i]
        y=Distance/(np.sin(Theta[i])*np.tan(Phi[i]))
        x=Distance/np.tan(Theta[i])
        if abs(x)<ScreenSize and abs(y)<ScreenSize and Theta[i]<np.pi:
            #The condition makes sure we only recored the positions of gamma rays
            #that hit our finite sized gamma array. The condition on theta makes
            #sure only forward traveling particles are plotted (don't want to plot
            #the back image).
            X+=[x]
            Y+=[y]
            
    return X,Y
                
def Smearing(X,Y):
    '''
    Real detector arrays are resolotuion limited this has been approximated 
    for our detectors by generating a random number using a normal distribution 
    centered on the true detector value. The standard deviation is equal to the 
    resolution of the detectors.
    '''
    X=np.random.normal(X,0.1)
    Y=np.random.normal(Y,0.3)    
    return X,Y

def ExponentialFitting(x,A,B):
    '''
    This function returns a scaled exponential curve that can be used to fit the
    decay position data. 
    '''
    a = [i*(-1)/(2000*MeanDecayTime) for i in x]
    return np.exp(a)*A + B

#This segment of code uses the decay position function and the fitting function 
#to create a plot of the decay position for N particles. 
N=int(1e7)
DecayPos=DecayPosition(np.random.rand(N))
print('The reduced chi squared of our fit is ' +str(Fitting(DecayPos,ExponentialFitting,100,'Decay position','Position (m)',Plot=True)))


#The following segment of code generates a 3D scatter of gamma ray position for a 
#range of different emission angles. The points are all ploted at a radius of 1m
#from the emmision point. If you want to see the difference between and isotropic
#and uniform random angles change Isotropic to false.

Theta,Phi=DecayAngles(1e4,Isotropic=True)

x=np.sin(Phi)*np.cos(Theta)
y=np.sin(Phi)*np.sin(Theta)
z=np.cos(Phi)

fig = plt.figure()
fig.suptitle('Scatter plot of gamma ray emission')
ax = Axes3D(fig)
ax.set_aspect('equal')
ax.scatter(x, y, z, s=0.25)
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_ylabel('Z (m)')
plt.show()
plt.clf()

#The following segment of code plots the image seen by the detector array.

GammaPosX,GammaPosY=ScreenPositions(1e6,4)
plt.hist2d(GammaPosX,GammaPosY,bins=200,cmap='jet',norm=LogNorm())
plt.colorbar()
plt.title('Detector array')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.show()
plt.clf()


fig1,(ax1, ax2)=plt.subplots(1, 2, sharey=True)
fig1.suptitle('Gamma ray position')
ax1.hist(GammaPosX,200)
ax2.hist(GammaPosY,200)
ax1.set(ylabel='Frequency')
ax1.set(xlabel='X position (m)')
ax2.set(xlabel='Y position (m)')
plt.show()
plt.clf()


GammaPosSX,GammaPosSY=Smearing(GammaPosX,GammaPosY)
plt.hist2d(GammaPosSX,GammaPosSY,bins=200,cmap='jet',norm=LogNorm())
plt.ylim(-4,4)
plt.xlim(-4,4)
plt.colorbar()
plt.title('Detector array with position smearing')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.show()
plt.clf()



'''-------------------------------Task 3------------------------------------'''

def ToyMonteCarlo(N,a,b,step):
    '''
    This function run a number of sudo experments to calculate the upper bound 
    of the cross section for a particle physics experement. a and b define the 
    range the cross section is belived to be in, step is the size of the steps
    that will be taken to itterate over the possible values of the cross section
    and N is the number of sudo experments that will be calculated for each value 
    of the cross section. When the particle physics experiment was conducted 
    there were five events observed. By modeling the number of events with random 
    numbers and finding the value of the cross section when more then 5 events
    occur 95% of the time an upper limit of the cross section can be calculated.
    '''
    ConfidenceLevel=[]
    CrossSection=[]
    for i in np.arange(a,b,step):
    #i represents the value of the cross section
        Count=0
        for j in range(int(N)):
            #In each sudo experiment a random number of back ground and signal 
            #events are generated. Both the background and signal events are 
            #modeled by a poisson distribution.The expectation of the poisson 
            #models is given in the problems sheet.
            BackGroundExpectation=np.random.normal(5.7,0.4)
            BackGround=np.random.poisson(BackGroundExpectation)
            lumError=12/100
            luminosity = np.random.normal(12, lumError)
            SignalExpectation=i*luminosity
            Signal=np.random.poisson(SignalExpectation)
            TotalEvents=Signal+BackGround
            
            if TotalEvents>5:
                Count+=1
                
        ConfidenceLevel+=[Count/N]
        CrossSection+=[i]
        
    for k in range(len(ConfidenceLevel)):
        if ConfidenceLevel[k]>=0.95:
            sigma=CrossSection[k]
            break
        
    return CrossSection,ConfidenceLevel,sigma

cross_section,conflevel,sigma=ToyMonteCarlo(1e3,0,1,0.01)
plt.plot(cross_section,conflevel,'.')
plt.hlines(0.95,0,1)
plt.vlines(sigma,0.5,1)
plt.title('Confidance level against Cross section')
plt.xlabel('Cross section (nb)')
plt.ylabel('Confidance level (%)')
plt.show()
plt.clf()

print('The upperbound of the cross section is ' + str(sigma))






