# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 19:48:30 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate_decay_positions(frequency, speed, num):
    # Simulate num decays using Poisson distribution, and return the an array of the lifetimes and decay positions from injection point of the nuclei.

    # Lifetimes follow Poisson distribution with mean num events per sec 1/520e-6
    num_events_per_sec = np.random.poisson(frequency, num)

    # Time is reciprocal of frequency
    lifetimes = 1 / num_events_per_sec

    # Distance is time*speed
    decay_positions = lifetimes*speed

    return lifetimes, decay_positions

DecayConstant=1/(550e-6)
DecayPos=simulate_decay_positions(DecayConstant,2000,int(1e5))[1]
plt.hist(DecayPos,100)
plt.show()
plt.clf()
