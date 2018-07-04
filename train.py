# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 14:35:32 2018

@author: Daniel Hu
"""
import pandas as pd
import numpy as np
from nn import game

def randt(n=1,eps=1):
    #generates list of random theta matrices for n players
    #eps determines magnitude of variation
    T1 = []
    T2 = []
    for i in range(n):
        
        T1.append(eps * np.random.random((9,11)))
        T2.append( eps * np.random.random((9,9)))
    return [T1,T2]


#generate n random players


class train:
    n = 1 #must be at least 3
    oppn = 1000
    win =0
    draw =0
    loss =0
    
    def __init__(self, T1, T2):
        [self.T1,self.T2] = randt(n=self.n)
        self.T1[0] = T1
        self.T2[0] = T2
            
    def tourn(self):
        [opp1,opp2] = randt(n=self.oppn)
        
        
        score = np.zeros(self.n)
        
        for i in range(self.n):
            for j in range(self.oppn):
                h = game(self.T1[i],self.T2[i],opp1[j],opp2[j])
                score[i] += h.playgame()
                
                w = h.playgame()
                if w ==1:
                    self.win +=1
                elif w==0:
                    self.draw +=1
                elif w ==-1:
                    self.loss +=1
                
                h = game(opp1[j],opp2[j],self.T1[i],self.T2[i])
                score[i] -= h.playgame()
                
                w = h.playgame()
                if w ==-1:
                    self.win +=1
                elif w==0:
                    self.draw +=1
                elif w ==1:
                    self.loss +=1
                
            for j in range(self.n):
                h = game(self.T1[i],self.T2[i],self.T1[j],self.T2[j])
                score[i] += h.playgame()
                score[j] -= h.playgame()

            
        
        #sort
        a = []
        
        for i in range(self.n):
            a.append([score[i],self.T1[i],self.T2[i]])
       
        a = sorted(a,key=lambda x: x[0], reverse = True)
        
        return [[a[i][1] for i in range(self.n)],[a[i][2] for i in range(self.n)]]
      
    def newgen(self,T1,T2):
        a1 = [T1[0],T1[1]]
        a2 = [T2[0],T2[1]]
        
        for i in range(self.n):
            over = T1[i]>50
            T1[i] = T1[i]*(1-over)+50*over
            under = T1[i]<-50
            T1[i] = T1[i]*(1-under)-50*under
            
            over = T2[i]>50
            T2[i] = T2[i]*(1-over)+50*over
            under = T2[i]<-50
            T2[i] = T2[i]*(1-under)-50*under
        
        for i in range(self.n-2):
            p1 = np.random.rand()
            k1 = int(np.floor(- np.log2(p1)))
            p2 = np.random.rand()
            k2 = int(np.floor(- np.log2(p2)))
            
            if k1>self.n-1:
                k1=self.n-1
            if k2>self.n-1:
                k2=self.n-1 
            
                  
            
            gene1 = np.random.random([9,11]) <0.5
            gene2 = np.random.random([9,9]) <0.5
            
            
            
            [b1,b2]= randt()
           
            a1.append(T1[k1]*gene1+T1[k2]*(1-gene1) +b1[0])
            a2.append(T2[k1]*gene2+T2[k2]*(1-gene2) + b2[0])
            
        self.T1 = a1
        self.T2 = a2
 

a = pd.read_excel('theta1000.xlsx',sheetname=0, header=None)
b = pd.read_excel('theta1000.xlsx',sheetname=1, header=None)       
a = a.values
b = b.values

t = train(c,d)

#for i in range(10000):
#    [a,b] = t.tourn()
#    t.newgen(a,b)
#    
#    if i%1000 ==0:
#        print(i)

win =0
draw = 0
loss = 0
t.tourn()
print (t.win,t.draw,t.loss)