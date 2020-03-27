# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 12:26:33 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

X=np.array([1000,5000,10000,15000,20000,25000,30000,35000,40000,45000])

AnalyticalMethod=np.array([0.000036,0.000159,0.000325,0.000505,0.00063,0.000798,0.000957,0.00105,0.00118,0.00132])
RejectMethod=np.array([0.00316,0.0165,0.0344,0.0497,0.0653,0.0839,0.0978,0.117,0.135,0.154])

AnalyticalMethodError=np.array([0.000001,0.000002,0.00002,0.00004,0.00003,0.00004,0.00007,0.00003,0.00003,0.000015])
RejectMethodError=np.array([0.0001,0.0004,0.001,0.003,0.001,0.005,0.002,0.005,0.004,0.008])

f, axarr = plt.subplots(2, sharex=True)
xp=X
z = np.polyfit(X,AnalyticalMethod,1)
p = np.poly1d(z)
axarr[0].plot(X,AnalyticalMethod,'.',xp,p(xp),'--')
axarr[0].errorbar(X,AnalyticalMethod , yerr=AnalyticalMethodError, fmt='.')

z1 = np.polyfit(X,RejectMethod,1)
p1 = np.poly1d(z1)
axarr[1].plot(X,RejectMethod,'.',xp,p1(xp),'--')
axarr[1].errorbar(X,RejectMethod , yerr=RejectMethodError, fmt='.')
axarr[0].set(ylabel='Time (s)')
axarr[1].set(ylabel='Time (s)')
axarr[1].set(xlabel='Number of samples')
axarr[0].set_title('Inverse transform sampling')
axarr[1].set_title('Rejection sampling')
plt.savefig('Time', dpi=250)
plt.show()
plt.clf()