# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 21:46:34 2019

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.mplot3d import Axes3D

def DecayPosition(xgen):
    '''
    Returns random decay position of particle. The random distribution for
    a large number of particles is exponential. The method used to produce
    the random distribution is the inverse sampling method.
    '''
    DecayConstant=1/(550e-6)
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
        phi=np.arccos(1-2*np.random.uniform(0,1,N))
    elif Isotropic==False:
        phi=np.random.uniform(0,np.pi,N)
    return theta,phi

def ScreenPositions(N,ScreenSize,Smearing=True):
    '''
    This function calculates the position of the gamma rays from the particle decays
    on a square screen. The screens dimensions can be edited. 
    
    '''
    N=int(N)
    Rand=np.random.rand(N)
    DecayPos=DecayPosition(Rand)
    plt.show()
    plt.clf()
    Theta,Phi=DecayAngles(N)
    X=[]
    Y=[]
    for i in range(N):
        Distance=2-DecayPos[i]
        y=Distance/(np.sin(Theta[i])*np.tan(Phi[i]))
        x=Distance/np.tan(Theta[i])
        if abs(x)<ScreenSize and abs(y)<ScreenSize and Theta[i]<np.pi:
            X+=[x]
            Y+=[y]
            
    return X,Y
                
def Smearing(X,Y):
    '''
    This function takes the calculated screen positions.
    '''
    X=np.random.normal(X,0.1)
    Y=np.random.normal(Y,0.3)    
    return X,Y
    
    
GammaPosX,GammaPosY=ScreenPositions(1e8,4)
plt.hist2d(GammaPosX,GammaPosY,bins=200,cmap='jet',norm=LogNorm())
plt.colorbar()
plt.title('Detector array')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.show()
plt.clf()

GammaPosX,GammaPosY=Smearing(GammaPosX,GammaPosY)
plt.hist2d(GammaPosX,GammaPosY,bins=200,cmap='jet',norm=LogNorm())
plt.ylim(-4,4)
plt.xlim(-4,4)
plt.colorbar()
plt.title('Detector array with position smearing')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.show()
plt.clf()


#N=int(1e6)
#Rand=np.random.rand(N)
#DecayPos=DecayPosition(Rand)
#Theta,Phi=DecayAngles(N)
#X=[]
#Y=[]
#SX=[]
#SY=[]
#
#for i in range(N):
#    Distance=2-DecayPos[i]
#    y=Distance/(np.sin(Theta[i])*np.tan(Phi[i]))
#    x=Distance/np.tan(Theta[i])
#    if abs(x)<5 and abs(y)<5:
#        X+=[x]
#        Y+=[y]
#        SX+=[np.random.normal(x,0.1)]
#        SY+=[np.random.normal(y,0.3)]
#        
#        
#plt.hist2d(X,Y,bins=200,norm=LogNorm())
#plt.colorbar()
#plt.show()
#plt.clf()
#
#plt.hist2d(SX,SY,bins=200,norm=LogNorm()) 
#plt.ylim(-5,5)
#plt.xlim(-5,5)
#plt.colorbar()
#plt.show()
#plt.clf()









