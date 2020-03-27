# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 17:34:33 2019

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare 

x=np.linspace(0,np.pi,100)
y=(1/2)*np.sin(x)

Rand=np.random.rand(int(1e2))
Theta=np.arccos(1-2*Rand)

#plt.hist(Theta,100,normed=True)
#plt.plot(x,y)
#plt.show()
#plt.clf()

g,h=np.histogram(Theta,100,normed=True)


hm=[]
for i in range(0,100):
    hm+=[(h[i]+h[i+1])/2]

y=(1/2)*np.sin(hm)
#plt.plot(x,y)
#plt.plot(h[0:100],g,'.')
#plt.show()
#plt.clf()

print(chisquare(g,y))


N=int(1e5)
xRand=np.random.uniform(0,np.pi,N)
yMax=np.sin(xRand)
yRand=np.random.rand(N)
X=[]

for i in range(N):
    if yRand[i]>yMax[i]:
        pass
    elif yRand[i]<=yMax[i]:
        X+=[xRand[i]]

#plt.hist(X,100,normed=True)
#plt.plot(x,y)
#plt.show()
#plt.clf()


plt.hist(X,100,normed=True)
plt.hist(Theta,100,normed=True)
plt.plot(x,y)
plt.show()
plt.clf()

plt.plot(hm,Theta)
plt.sho()


        
    
    
    