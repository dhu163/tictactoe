# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
import tkinter.messagebox
from PIL import ImageTk, Image
import pandas as pd
import time

import math

from nn import randt, game
#path = 'C:/Users/Daniel Hu/OneDrive/OneDrive-2014-04-28 20170626/Cam Lent 2014/Python/ttt/'

class ttt:
    tokens = 'XO'
    blength = 270 #board size in pixels
    com1 = 1 #0 if none, or +1  if cross or -1 if noughts
    com2 = 0 #0 if none, or -1 if noughts
    #weights

    
    def __init__(self,T11=randt()[0][0],T12=randt()[1][0],T21=randt()[0][0],T22=randt()[1][0]):
        self.parity = 1 #counts move number 'X' goes first
        self.state = [' ']*9 #board state (first row first) #shouldnt need to store this, just store list of moves
        self.marks = [0]*9
        self.T11 = T11
        self.T12 = T12
        self.T21 = T21
        self.T22 = T22

        
        self.root = tk.Tk()
        # Code to add widgets will go here...
        #size
#        bheight = 200
#        bwidth = 300
        
        #board image
        img = ImageTk.PhotoImage(Image.open("board.png"))
        panel = tk.Label(self.root, image = img)
        self.board = img #keep own reference
        panel.pack(side = "bottom", fill = "both", expand = "yes")
#
        tk.Button(self.root, text="Quit", command=self.root.destroy).pack()


        #variables
#        self.Squares = [0]*9
#        for t in range(9):
#            options = {"text":str(t),"height":20,"width":30,"bg":"white"}
#            self.Squares[t]= tk.Button ( root, options, command = self.playmove(t) )
#            self.Squares[t].place(x=bwidth//3 *t %bwidth,y=(bheight//3)*(t-3*(t//3)) % bheight)
#        

        self.root.bind('<Button-1>',self.button) #left click plays move
        
        self.root.resizable(width=False, height=False)
            

        

        if self.com2:
            self.game = game(T11,T12,T21,T22)
            
            while 1:
                if self.parity ==1:
                    t = self.game.fp(self.T11,self.T12)
                    if self.state[t]==' ':
                        self.game.playmove(t)
                        self.playmove(t)
                        
                    print(t)
                

                self.pause(0.5)
                
                if self.parity == -1:
                    t = self.game.fp(self.T21,self.T22)
                    if self.state[t]==' ':
                        self.game.playmove(t)
                        self.playmove(t)
                        
                    print(t)
        
        elif self.com1==1:
    
            self.game = game(T11=T11,T12=T12)
            t = self.game.fp(T11,T12)
            self.game.playmove(t)
            self.playmove(t)
        elif self.com1==-1:
            self.game = game(T21=T21,T22=T22)
            
        self.root.mainloop()
        
    def pause(self,t):
        print(t)
        time.sleep(t)
    
    def button(self,e): #mouse click
        if self.com1==self.parity:
            print('error')
            quit()
        if self.com2:
            quit()
        
        x,y = e.x,e.y
        
        if y<26:
            quit()
        #convert to coordinates
        #calculate boardlength, margin length, square size, and the x and y of the board centre
        #mlength = 0
        sq = self.blength/3
        
        bx = math.floor(x/sq)
        by = math.floor((y-26)/sq)
        
        t = 3*by + bx
        
        if self.state[t]!=' ':
            quit()
        self.playmove(t)
        self.game.playmove(t)
        
        if self.com1 == self.parity:
            t = self.game.fp(self.T11,self.T12)
            if self.state[t]!=' ':
                quit()
            time.sleep(0.5)
            self.game.playmove(t)
            self.playmove(t) #get com1 to play a move
        
        
    def playmove(self,t): #box number t
        if t<0 or t>8:
            return
        if self.state[t]!=' ':
            return
        
        
        g = self.tokens[(-self.parity+1)//2]
        

        img = ImageTk.PhotoImage(Image.open(g+".png"))
        panel = tk.Label(self.root, image = img)
        self.marks[t]=img
        options = {'x':(t%3)*self.blength/3, 'y':(t//3)*self.blength/3 + 26}
        panel.place(options)
        
        self.state[t] = g
        self.parity *= -1
        
        self.hasWon(g)
    
    def hasWon(self,g):
        if self.state[0]==self.state[3]==self.state[6]==g or \
            self.state[1]==self.state[4]==self.state[7]==g or \
            self.state[2]==self.state[5]==self.state[8]==g or \
            self.state[0]==self.state[1]==self.state[2]==g or \
            self.state[3]==self.state[4]==self.state[5]==g or \
            self.state[6]==self.state[7]==self.state[8]==g or \
            self.state[0]==self.state[4]==self.state[8]==g or \
            self.state[2]==self.state[4]==self.state[6]==g:
                winm = tk.messagebox.showinfo("Congrats!", g+" has won!")
                self.newGame()
        if not(' ' in self.state):
            winm = tk.messagebox.showinfo("Tie!", "Draw!")
            self.newGame()
    
    def newGame(self):
        self.state = [' '] *9 
        self.marks = [0]*9 #delete images
        self.parity = 1
        
        panel = tk.Label(self.root, image = self.board)
        panel.place(x=0,y=26)
        
        if self.com2:
            self.game = game(self.T11,self.T12,self.T21,self.T22)
            time.sleep(1)
        
        elif self.com1 == 1:
            self.game = game(T11=self.T11,T12=self.T12)
            time.sleep(1)
            t = self.game.fp(self.T11,self.T12)
            self.game.playmove(t)
            self.playmove(t)
            
        elif self.com1 == -1:
            self.game = game(T21=self.T11,T22=self.T12)
            print(self.com1, self.parity)
    

        
a = pd.read_excel('theta1000.xlsx',sheetname=0, header=None)
b = pd.read_excel('theta1000.xlsx',sheetname=1, header=None)       
a = a.values
b = b.values

     
ttt(a,b)
        