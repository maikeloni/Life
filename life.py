#!/usr/bin/python
# -*- coding: utf-8 -*-


# For Windows: update line 277



from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from copy import *
from functions import *
from tkinter import messagebox
import pickle
import platform, sys, shutil, io
import time, datetime, random
import traceback
import subprocess

# Program Version
version = 1.2
        

class gol():
    
    def __init__(self,mapLength):
               
        self.showPerformance = False
        self.showDurchschnitt = False
        self.paused = True
        self.time=[];
        self.mapLength = mapLength

        # Window
        self.root = Tk()
        self.root.focus_set()
        self.root.title('gol')
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_height = screen_height-55
        heightSettings = 90
        self.heightSettings = heightSettings
        maxCanvasLength = window_height-heightSettings-4        
        self.fieldWidth = 1
        canvasLength = self.findCanvasLengthAndFieldWidth(maxCanvasLength)
        #canvasLength = maxCanvasLength#self.fieldWidth*mapLength
        
        window_width = max(656,canvasLength)
        self.window_width = window_width
        self.window_height = window_height
        self.root.geometry('656x'+str(window_height)) 
        
        # Frames
        
        self.frameSettings = Frame(self.root, width=canvasLength, height=heightSettings)
        self.frameSettings.grid(row=0, column=0)
        
        self.frameRadiobuttons = Frame(self.frameSettings, height=heightSettings, pady=3, bd=1, relief=GROOVE)
        self.frameRadiobuttons.grid(row=0, column=0)
        
        self.frameRule = Frame(self.frameSettings, height=heightSettings, bd=1, relief=GROOVE)
        self.frameRule.grid(row=0, column=1)
        self.frameRuleCB = Frame(self.frameRule, height=int(heightSettings*4/5))
        self.frameRuleCB.grid(row=0, column=0)
        self.frameRuleLabel = Frame(self.frameRule, height=int(heightSettings*1/5))
        self.frameRuleLabel.grid(row=1, column=0)
        
        self.frameRuleButtons = Frame(self.frameSettings, height=heightSettings)
        self.frameRuleButtons.grid(row=0, column=2)
        
        self.framePlaySpeed = Frame(self.frameSettings, width=canvasLength, height=heightSettings, pady=10, bd=1, relief=GROOVE)
        self.framePlaySpeed.grid(row=0, column=3)
        
        self.frameCanvas = Frame(self.root, width=canvasLength, height=canvasLength, bd=1, relief=GROOVE)
        self.frameCanvas.grid(row=1, column=0)
        
        self.canvas = Canvas(self.frameCanvas, width=canvasLength+1, height = canvasLength+1, background="white")#, borderwidth=1)
        self.canvas.grid(row=0, column=0)
        
        # Radiobuttons for topology
        self.radioButtonVar = StringVar()
        self.radioButtonVar.set('-n')
        topologyDict = {'Normal':'-n','Torus':'-t','Klein Bottle':'-k','Projective Plane':'-p'}
        topologyList = ['Normal','Torus','Klein Bottle','Projective Plane']
        n = 0
        for topology in topologyList:
            Radiobutton(self.frameRadiobuttons, 
                text=topology,
                variable=self.radioButtonVar, 
                value=topologyDict[topology]).grid(row=n,column = 0,sticky = (W))
            n+=1
        
        # Checkboxes for rules
        self.ruleList = [[],[]]  # ruleList[0] contains ceckboxvariables for ruleAlive, ruleList[1] contains ceckboxvariables for ruleDead
        Label(self.frameRuleCB, text="Alive").grid(row=1,column=0,sticky=(NE))
        Label(self.frameRuleCB, text="Dead").grid(row=2,column=0,sticky=(NE))
        self.cbList=[[None]*9,[None]*9]
        for k in range(9):
            Label(self.frameRuleCB, text=str(k), padx=6).grid(row=0,column=k+1,sticky=(NW))
            for l in range(2):
                self.ruleList[l].append(IntVar())
                self.cbList[l][k]=(Checkbutton(self.frameRuleCB, variable = self.ruleList[l][k], command=self.updateRuleFromCheckboxes, padx=0, pady=0))
                self.cbList[l][k].grid(row=l+1, column=k+1, sticky=(NW))
                #cbList[l][k] = ruleList[l][k]
        Button(self.frameRuleCB, text="Anti", height=1, pady=0, padx=4, command = self.setAntirule).grid(row = 0, column = 0)
        
        # Label Rule and DropdownMenu
        self.rule=''
        self.ruleInfo=StringVar()
        self.ruleInfo.set("23/3 Conways Game Of Life")
        Label(self.frameRuleLabel, text="Rule: ").grid(row=0,column=0)
        #Label(self.frameRuleLabel, textvariable=self.rule).grid(row=0,column=1)
        OptionMenu(self.frameRuleLabel,self.ruleInfo, "23/3 Conways Game Of Life", "3/3", "13/3", "236/3    Exploding World", "12345/3  Labyrinth", "0246/1357  Copy World", "1357/1357  Copy World 2", "24/35", "0123/01234   Blur").grid(row=0,column=2)
        
        # Paint
        self.canvas.bind( "<B1-Motion>", self.paintAlive )
        self.canvas.bind( "<Button-1>", self.paintAlive )
        self.canvas.bind( "<B3-Motion>", self.paintDead )
        self.canvas.bind( "<Button-3>", self.paintDead )
        
        # Canvas
        self.fields = [None]*mapLength
        for k in range(len(self.fields)):
            self.fields[k]=[]
        for x in range(mapLength):
            for y in range(mapLength):
                k = x*self.mapLength+y
                self.fields[x].append(field(k,self.canvas,self.fieldWidth,[x,y] ,self.canvas.create_rectangle(self.fieldWidth*x+1, self.fieldWidth*y+1, self.fieldWidth*(x+1), self.fieldWidth*(y+1), fill="white", outline='black'), False, True))
                self.fields[x][y].setDead()

        
        #Button and Keys for play / pause and speeder     
        self.textGrid = StringVar()   
        self.textGrid.set("Grid On")
        Button(self.framePlaySpeed, text="Play / Pause", command = self.changePauseStatus).grid(row = 0, column = 0)
        Button(self.framePlaySpeed, textvariable=self.textGrid, command = self.toggleGrid).grid(row = 0, column = 3)
        Button(self.framePlaySpeed, text="clear", command = self.clearBoard).grid(row = 1, column = 3)
        self.root.bind('<KeyPress-space>', self.changePauseStatusKey)
        
        self.status = StringVar()
        Label(self.framePlaySpeed, textvariable = self.status).grid(row = 1, column = 0)
    
        self.speeder = Scale(self.framePlaySpeed, from_=0.1, digits=2, to=5, resolution=0.1, orient=HORIZONTAL)
        self.speeder.set(1)
        self.speeder.grid(row = 0, column = 1)
        
        
        self.idle()
        
        while 0:
            self.root.update()
            self.root.update_idletasks()
            
        self.root.mainloop()
    
    def findCanvasLengthAndFieldWidth(self,maxCanvasLength):
        for k in range(1,11):
            if k*self.mapLength < maxCanvasLength:
                self.fieldWidth=k
        return self.fieldWidth*self.mapLength
    
    def ruleInfoToRule(self):
        self.rule=''
        for char in self.ruleInfo.get():
            if char == ' ':
                break
            self.rule+=char
        return None
    
    def paintAlive(self,event):
        if not self.paused:
            return None
        x, y = int(event.x/self.fieldWidth) , int(event.y/self.fieldWidth)
        self.fields[x][y].setAlive()
        return None
            
    def paintDead(self,event):
        if not self.paused:
            return None
        x, y = int(event.x/self.fieldWidth) , int(event.y/self.fieldWidth)
        self.fields[x][y].setDead()
        return None
        
    def changePauseStatus(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True
            # compute mean of time for stringtofield
            if self.showDurchschnitt:
                print("Durchschnitt:",round((sum(self.time)/ float(len(self.time)))*1000,4),"ms.")
        return None
    
    def changePauseStatusKey(self,event):
        self.changePauseStatus()
        return None
        
    def toggleGrid(self):
        if self.textGrid.get() == "Grid Off":
            self.textGrid.set("Grid On")
        elif self.textGrid.get() == "Grid On":
            self.textGrid.set("Grid Off")        
        for x in range(self.mapLength):
            for y in range(self.mapLength):
                self.fields[x][y].toggleGrid()
                if self.fields[x][y].getStatus():
                    self.fields[x][y].canvas.itemconfigure( self.fields[x][y].rectangle,fill='black', outline='black')
                elif self.fields[x][y].getGrid() and not self.fields[x][y].getStatus():
                    self.fields[x][y].canvas.itemconfigure( self.fields[x][y].rectangle,fill='white', outline='black')
                elif not self.fields[x][y].getGrid() and  not self.fields[x][y].getStatus():
                    self.fields[x][y].canvas.itemconfigure( self.fields[x][y].rectangle,fill='white', outline='white')
        return None
        
    def clearBoard(self):
        if self.paused:
            for x in range(self.mapLength):
                for y in range(self.mapLength):
                    self.fields[x][y].setDead()
        return None
    
    def idle(self):
        self.ruleInfoToRule()
        #self.updateCanvas()
        if not self.paused:
            # run game of life
            if self.showPerformance or self.showDurchschnitt:
                startTime = time.time()
            self.updateField()
            if self.showPerformance or self.showDurchschnitt:
                now = (time.time()-startTime)
                self.time.append(now)                
                if self.showPerformance:
                    print('Total time:',round(now*1000,4),'ms.\n')
        # update status
            self.status.set("Runs")
        else:
            self.status.set("Paused")
        
        #update checkbox
        self.updateCheckboxesFromRule()
        
        # update status
        if self.paused:
            self.status.set("Paused")
        else:
            self.status.set("Runs...")
        
        # update speeder        
        speed = int(50/self.speeder.get()) 
        
        self.root.after(speed, self.idle)
        return None
    
    def updateCanvas(self):
        if self.window_height != self.root.winfo_height() or self.window_width != self.root.winfo_width():
            print("hier")            
            self.window_height = self.root.winfo_height()
            self.window_width = self.root.winfo_width()
            canvasLength = self.findCanvasLengthAndFieldWidth(self.window_height-self.heightSettings-4)
            print(self.frameCanvas)
            self.frameCanvas.destroy()
            self.canvas.destroy()
            print(self.frameCanvas)
            #self.frameCanvas = Frame(self.root, width=canvasLength, height=canvasLength, bd=1, relief=GROOVE)
            #self.frameCanvas.grid(row=1, column=0)
            #self.canvas = Canvas(self.frameCanvas, width=canvasLength+1, height = canvasLength+1, background="white")#, borderwidth=1)
            #self.canvas.grid(row=0, column=0)
            self.root.update()
            for x in range(self.mapLength):
                for y in range(self.mapLength):
                    k = x*self.mapLength+y
                    self.fields[x][y]=field(k,self.canvas,self.fieldWidth,[x,y] ,self.canvas.create_rectangle(self.fieldWidth*x+1, self.fieldWidth*y+1, self.fieldWidth*(x+1), self.fieldWidth*(y+1), fill="white", outline='black'), False, True)
                    self.fields[x][y].setDead()
        return None
    
    def updateCheckboxesFromRule(self):
        #split rule into ruleDead and ruleAlive (e.g.: rule = 23/3, then ruleDead=23 and ruleAlive=3
        ruleDead = ''
        ruleAlive = ''
        RuleDeadBoolean = True
        for char in self.rule:
            if char == '/':
                RuleDeadBoolean = False
            else:
                if RuleDeadBoolean:
                    ruleDead += char
                else:
                    ruleAlive += char
        
        for k in range(9):
            # ruleDead
            CharIsSet = False
            for char in ruleDead:
                if int(char)==k:
                    self.cbList[0][k].select()
                    CharIsSet = True
            if not CharIsSet:
                self.cbList[0][k].deselect()
            # ruleAlive
            CharIsSet = False
            for char in ruleAlive:
                if int(char)==k:
                    self.cbList[1][k].select()
                    CharIsSet = True
            if not CharIsSet:
                self.cbList[1][k].deselect()
        return None
    
    def updateRuleFromCheckboxes(self):
        # update Rule
        self.ruleInfo.set('')
        #dead
        for k in range(9):
            if self.ruleList[0][k].get():
                self.ruleInfo.set(self.ruleInfo.get()+str(k))
        self.ruleInfo.set(self.ruleInfo.get()+'/')
        #alive
        for k in range(9):
            if self.ruleList[1][k].get():
                self.ruleInfo.set(self.ruleInfo.get()+str(k))
        return None
    
    def updateField(self):
        if self.showPerformance:
            startTime = time.time()
        string=convertFieldsToString(self.fields)
        if self.showPerformance:
            print('Converted fields to string in',round((time.time()-startTime)*1000,4),'ms.')
        
        if self.showPerformance:
            startTime = time.time()
        self.ruleInfoToRule()
        if platform.system() == 'Windows':
            proc = subprocess.Popen(['life.exe', self.rule, self.radioButtonVar.get() ,string], stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen(['./life', self.rule, self.radioButtonVar.get() ,string], stdout=subprocess.PIPE)
        if self.showPerformance:
            print('Processed calculations in',round((time.time()-startTime)*1000,4),'ms.')
        
        if self.showPerformance:
            startTime = time.time()
        output = proc.stdout.read().decode("utf-8")
        if self.showPerformance:
            print('Processed decoding in',round((time.time()-startTime)*1000,4),'ms.')
        
        startTime = time.time()
        convertStringToFields(output,self.fields,self.mapLength)
        if self.showPerformance:
            print('Processed string to field in',round((time.time()-startTime)*1000,4),'ms.')
        
        return None
    
    def setAntirule(self):
        temp=[[None]*9,[None]*9]
        for k in range(9):
            for l in range(2):
                temp[l][k]=self.ruleList[l][k].get()
        for k in range(9):
            for l in range(2):
                if not temp[l][k]:
                    self.cbList[(l+1)%2][8-k].select()
                else:
                    self.cbList[(l+1)%2][8-k].deselect()
        self.updateRuleFromCheckboxes()
        return None
        
        
while True:
    try:
        size = eval(input('Which size shall the world have? (10<=size<=200)\n'))
        size = int(size)
        if isinstance( size, int ) and size >= 10 and size <= 200:
            break   
        else:
            print('Size must be an integer between 10 and 200!\n')
    except Exception:#(SyntaxError, NameError, ValueError):
        print('Size must be an integer between 10 and 200!\n')
gol(size)


