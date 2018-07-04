# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 11:12:16 2018

@author: Daniel Hu
"""

#single layer net 9,9,9
#get output y from input x board board (X is +1, O is -1, empty is 0)
import numpy as np
import time



def randt(eps=1):
    theta1 = eps * np.random.random((9,11))
    theta2 = eps * np.random.random((9,9))
    return [np.array([theta1]),np.array([theta2])]


class game: 
    def __init__(self,T11=randt()[0][0],T12=randt()[1][0],T21=randt()[0][0],T22=randt()[1][0]):
        self.board = np.zeros(9)
        self.parity = 1
        self.T11 = T11
        self.T12 = T12
        self.T21 = T21
        self.T22 = T22
    
    def fp(self, theta1, theta2):
    #all entries are np.array type
    
        
        z = theta1.dot(np.concatenate((np.array([self.parity,1]),self.board))) #player term +bias term
        a1 = 1/(1+np.exp(z))
        

        z = theta2.dot(a1)
        a2 = 1/(1+np.exp(z))
        
        #only play on blank squares
        a2 = a2 * (1-self.board **2)
        
        return np.argmax(a2)
    
    def playcmove(self,theta1,theta2):
        
        t = self.fp(theta1, theta2)
        
        return self.playmove(t)
    
    def playmove(self,t):
        if self.board[t]==0:
            self.board[t] = self.parity
            self.parity *= -1
            return 0
        else:
            return 1# i.e. pass error, so player loses
    
    def playgame(self,disp = 0):
        #1t are player 1's weights
        
        
        while 1:
            
            
            if self.parity==1:
                
                if(self.playcmove(self.T11,self.T12)): 
                    return -1
            else:
                if(self.playcmove(self.T21,self.T22)):
                    return 1
              
                
            if disp:
                print(self.board)
            #winning
            g = self.parity
            
            if self.board[0]==self.board[3]==self.board[6]==g or \
                self.board[1]==self.board[4]==self.board[7]==g or \
                self.board[2]==self.board[5]==self.board[8]==g or \
                self.board[0]==self.board[1]==self.board[2]==g or \
                self.board[3]==self.board[4]==self.board[5]==g or \
                self.board[6]==self.board[7]==self.board[8]==g or \
                self.board[0]==self.board[4]==self.board[8]==g or \
                self.board[3]==self.board[4]==self.board[5]==g:
                return g #who won
            
            if not(0 in self.board):
                return 0 #draw
            
#g = game(a,b,a,b)
#
#print(g.playgame(1))
#[p1t1,p1t2] = randt(1)
#[p2t1,p2t2] = randt(1)
#h = game(p1t1[0],p1t2[0],p2t1[0],p2t2[0])
#print(h.playgame(1))
##
#h = game(p2t1[0],p2t2[0],p1t1[0],p1t2[0])
#print(h.playgame(1))

#conduct tournament to select winner

#eps=1e-1
#
#p1 = randt(1)[0]
#
#p2 = randt(1)[1]
#
#
#pnum = 10 #num of players
#
#for i in range(1000):
#    players1 = p1
#    players2 = p2
#    
#    for i in range(pnum-1): 
#        players1 = np.concatenate((players1,p1+randt(eps)[0]))
#        players2 = np.concatenate((players2,p2+randt(eps)[1]))
#        
#    score = np.zeros([pnum,pnum])
#    
#    for i in range(pnum):
#        for j in range(pnum):
#            h = game(players1[i],players2[i],players1[j],players2[j])
#            win = h.playgame()
#            
#            if win==1:
#                score[i][j]=1
#            if win==-1:
#                score[i][j]=-1
#    
#    
#    k = np.sum(score, axis=1) #for now just count wins with first to play
#    t = np.argmax(k)
#
#    #print(score)
#    p1 = [players1[t]]
#    p2 = [players2[t]]
#    #time.sleep(3)
#            
#h = game(players1[0],players2[0],players1[1],players2[1])
#print(h.playgame(disp=1))
#
#for i in range(5):
#    h = game(players1[0],players2[0],randt(1)[0][0],randt(1)[1][0])
#    print(h.playgame(disp=1))