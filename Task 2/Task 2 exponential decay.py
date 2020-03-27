# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 01:50:15 2019

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
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

N=int(1e3)
Rand=np.random.rand(N)
DecayPos=DecayPosition(Rand)
plt.hist(DecayPos,100)
plt.show()
plt.clf()


Theta,Phi=DecayAngles(1e4)
x=np.sin(Phi)*np.cos(Theta)
y=np.sin(Phi)*np.sin(Theta)
z=np.cos(Phi)

fig = plt.figure()#figsize=(6,6))#increases figure size in kernel
ax = Axes3D(fig)
ax.set_aspect('equal')#sets the scales of the axes as equal
ax.scatter(x, y, z, s=0.25)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_ylabel('Z')
plt.show()
plt.clf()