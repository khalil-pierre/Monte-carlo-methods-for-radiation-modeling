# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:33:28 2019

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

#N=int(1e5)
#Sigma=np.linspace(0,1,10)
#for i in Sigma:
#    BackGroundExpectation=np.random.normal(5.7,0.4,N)
#    BackGround=np.random.poisson(BackGroundExpectation)
#    SignalExpectation=i*12
#    Signal=np.random.poisson(SignalExpectation,N)
#    NumberOfEvents=Signal+BackGround
#    
#    plt.title('Sigma=' +str(i))
#    plt.hist(NumberOfEvents,10)
#    plt.show()
#    plt.clf()
#    

#def ToyMonteCarlo():
#    '''
#    This function calculates the confidance level of
#    '''


#ConfidenceLevel=[]
#Sigma=[]
#for i in np.arange(0,1,0.1):
#    Count=0
#    for j in range(int(1e5)):
#        #Number of sudo experiments for each sigma
#        BackGroundExpectation=np.random.normal(5.7,0.4)
#        BackGround=np.random.poisson(BackGroundExpectation)
#        SignalExpectation=i*12
#        Signal=np.random.poisson(SignalExpectation)
#        TotalEvents=Signal+BackGround
#        if TotalEvents>5:
#            Count+=1
#    
#    ConfidenceLevel+=[Count/1e5]
#    Sigma+=[i]
#    
#plt.plot(Sigma,ConfidenceLevel)
#plt.show()
    
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
        
    return CrossSection,ConfidenceLevel

sigma,conflevel=ToyMonteCarlo(1e3,0,1,0.01)
plt.plot(sigma,conflevel,'.')
plt.title('Confidance level against Cross section')
plt.xlabel('Cross section (nb)')
plt.ylabel('Confidance level (%)')
plt.show()
plt.clf()
    
            
        
#import numpy as np
#import matplotlib.pyplot as plt
#
#l = 0
#exprun = 500000
#def pseudo_exp(N,a,b,step):
#    for i in np.arange(a,b,step):
#        sig = i
#        k=0
#        for j in range(N):
#            background_gauss = np.random.normal(5.7,0.4)
#            background_count = np.random.poisson(background_gauss)
#            L = 12
#            Lsig = L*sig
#            signal_count = np.random.poisson(Lsig)
#            total_count = background_count + signal_count
#            if total_count > 5:
#                k+=1
#        l = k/exprun
#        if l < 0.95:
#            continue
#        else:
#            x = sig
#            break
#
#    return x,l
#
#sig1,l1 = pseudo_exp(exprun,0,1,0.01)
#
#sig2,l2 = pseudo_exp(exprun,sig1-0.01,sig1+0.01,0.001)
#print(sig2, l2)
        
    





#
#for i in range(int(1e6)):
#    BackGroundExpectation=np.random.normal(5.7,0.4)
#    BackGround=np.random.poisson(BackGroundExpe)