#!/usr/bin/python
# -*- coding: utf-8 -*-

# Classes

import time

class field:

    def __init__(self, id, canvas, fieldWidth, position, rectangle, status, grid):
        self.id = id
        self.canvas = canvas
        self.fieldWidth = fieldWidth
        self.position = position	# [int,int]
        self.rectangle = rectangle
        self.status = status # True: alive => black, False: dead => white
        self.grid = grid
    
    def setAlive(self):
        if not self.status:
            self.canvas.itemconfigure(self.rectangle,fill='black', outline='black')
            #self.canvas.create_rectangle(self.fieldWidth*self.position[0]+1, self.fieldWidth*self.position[1]+1, self.fieldWidth*(self.position[0]+1), self.fieldWidth*(self.position[1]+1), fill="black")
            self.status = True
        return None
    
    def setDead(self):
        if self.status and self.grid:
            self.canvas.itemconfigure(self.rectangle,fill='white', outline='black')
            #self.canvas.create_rectangle(self.fieldWidth*self.position[0]+1, self.fieldWidth*self.position[1]+1, self.fieldWidth*(self.position[0]+1), self.fieldWidth*(self.position[1]+1), fill="white")
            self.status = False
        elif self.status and not self.grid:
            self.canvas.itemconfigure(self.rectangle,fill='white', outline='white')
            self.status = False
        return None
    
    def getStatus(self):
        return self.status
    
    def getPosition(self):
        return self.position
        
    def getID(self):
        return self.id
        
    def getGrid(self):
        return self.grid
    
    def toggleGrid(self):
        if self.grid:
            self.grid = False
        else:
            self.grid = True
        return None

# Functions

def convertFieldsToString(fields):
    """length=len(fields)
    str_list=[None]*length*(length+1)
    k=0
    for x in range(len(fields)):
        for y in range(len(fields[x])):
            if fields[y][x].getStatus():
                str_list[k]="1"
                k+=1
            else:
                str_list[k]="0"
                k+=1
        str_list[k]="\n"
        k+=1
    return "".join(str_list)"""
    
    string = ""
    for x in range(len(fields)):
        for y in range(len(fields[x])):
            if fields[y][x].getStatus():
                string+="1"
            else:
                string+="0"
        string+="\n"
    return string
    
def convertStringToFields(string,fields,lengthLine):
    printMean = False
    k=0
    if printMean:
        timer=[]
    for char in string:
        if printMean:        
            startTime = time.time()
        if char == "1":
            fields[k%lengthLine][int(k/lengthLine)].setAlive()
            k+=1
        elif char == "0":
            fields[k%lengthLine][int(k/lengthLine)].setDead()
            k+=1
        if printMean:
            now = time.time()-startTime
            timer.append(now)
    if printMean:
        print('MEAN: Converted string to fields in',round((sum(timer)/float(len(timer)))*len(string)*1000,4),'ms.')
    return fields
