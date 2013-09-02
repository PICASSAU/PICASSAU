#-------------------------------------------------------------------------------
# Name:        svgParser
# Purpose:
#
# Author:      Kayla Frost
#
# Created:     30/08/2013
# Copyright:   (c) Kayla 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys
import re
import serial
from xml.dom import minidom


class svgParser:
    def __init__(self):

        #instantiate some arrays we'll use
        self.commands = []
        self.xCoords = []
        self.yCoords = []

        self.ser = serial.Serial('COM5') #9600 Baud, 8 data bits, No parity, 1 stop bit


    def readInFile(self, file):
        '''
        Given a file path, this function opens it, reads it,
        and returns its contents as a string.

        '''
        if os.path.isfile(file):
            tempFile = open(file, 'r')
            output = tempFile.read()
            tempFile.close()
            return output
        else:
            return

    def parsePaths(self, svgStr):
        '''
        Given a string, presumably the text from the SVG file,
        it will strip out the paths and put them into an array.

        '''
        doc = minidom.parseString(svgStr)
        pathStrings = [path.getAttribute('d') for path in
                        doc.getElementsByTagName('path')]
        doc.unlink()
        return pathStrings

    def evalCurveEqtn(self, t, PArray):
        Pt = pow((1-t),3)*PArray[0] + 3*pow(1-t,2)*t*PArray[1] + 3*(1-t)*pow(t,2)*PArray[2] + pow(t,3)*PArray[3]
        return Pt

    def splitStrXY(self, str):
        x = int(0.5+(float(str.split(',')[0])))
        y = int(0.5+(float(str.split(',')[1])))
        return x,y

    def capFirstLetOnly(self, str):
         if str[0].islower:
            str = str[0].upper() + str[1:]
         return str

    def matchAny(self, lookingfor, element):
        lookingfor = '[' + lookingfor + ']'
        return re.match(lookingfor, element)

    def talkToArduino(self, i):
        serOut =str(self.commands[i]) + ' ' + str(self.xCoords[i]) + ',' + str(self.yCoords[i])
        self.ser.write(serOut)
        ardCheck = self.ser.read(self.ser.inWaiting())
        return serOut, ardCheck

def main():

    mySVG = svgParser()
    #load in file - here I'm doing it manually
    file = "C:\Users\Kayla\Documents\School\Fall 2013\Senior Design\svgParser\curvySVG2.svg"

    #N sets how many sections curves are divided into
    N = 10
    Ccount = 0
    PXArray = []
    PYArray = []

    #instantiate some flags

    #remember the last element and last command given
    lastElemLet = None
    lastComm = None

    #remember the last case used: upper = True, lower = False
    lastCaseUp = None

    #remember the value of the last x and y coordinates
    lastXCoord = 0
    lastYCoord = 0

    #remember the first coordinate of each path
    pathFirstCoordFlag = None
    pathFirstXCoord = 0
    pathFirstYCoord = 0

    #read in the file and parse out the paths into an array of strings
    svgStr = mySVG.readInFile(file)
    pathStrings = mySVG.parsePaths(svgStr)

    #iteratively run through the paths, correct letters, and reorganize
    #into the different arrays
    for path in pathStrings:
        path = mySVG.capFirstLetOnly(path) #we want to make sure the first letter is capitalized
        elements = path.split(' ') #split the elements based on spaces
        pathFirstCoordFlag = True #raise the falg to say it's the first coord of the path

        #iterate through each element of the path i.e. each letter or number set
        for element in elements:
            #check to see if the element is an acceptable letter
            if mySVG.matchAny('mlzcMLZC', element):
                if mySVG.matchAny('zZ', element):
                   #if the letter is Z, then we need to close the loop by drawing
                   #back to the first coordinate of the path.  To do this, add a
                   #"L" to the command array, and put the initial x and y coords
                   #into the x and y arrays.
                   mySVG.commands.append('L')
                   mySVG.xCoords.append(pathFirstXCoord)
                   mySVG.yCoords.append(pathFirstYCoord)
                   lastElemLet = True
                   lastComm = 'zZ'

                elif mySVG.matchAny("cC", element):
                    #if the letter is C, then just set the right flags, and we'll
                    #take care of it when we get to the actual numbers (see below)
                    if mySVG.matchAny("c", element):
                        lastComm = 'c'
                    else:
                        lastComm = 'C'
                    Ccount = 0
                    lastElemLet = True

                else: #letter is m/M/l/L
                    #if the letter is lowercase, change the lastCaseUp flag and add
                    #the uppercase version to the command array
                    if element.islower():
                        lastCaseUp = False
                        mySVG.commands.append(element.upper())
                    #if the letter isn't lowercase, change the flag and add the
                    #element to the commands
                    else:
                        lastCaseUp = True
                        mySVG.commands.append(element)
                    lastElemLet = True
                    lastComm = 'mMlL'

            #if the element isn't a letter...(it's a number)
            else:
                #this section will go through calculating a curve
                if lastComm is ('c' or 'C'):
                    if Ccount  is 0: #this is a counter to gather the curve coords
                        #the first point used to calucalte the curve is the previous
                        #point, so add the x and y to the corresponding P arrays
                        PXArray.append(lastXCoord)
                        PYArray.append(lastYCoord)
                    Ccount += 1 #increment count because we've got 1 point down

                    #add the current coordinates to the PX and PY arrays
                    tempx = mySVG.splitStrXY(element)[0]
                    tempy = mySVG.splitStrXY(element)[1]
                    if lastComm is 'c':
                        #if c is lowercase, it's relative to the 1st point
                        tempx += PXArray[0]
                        tempy += PYArray[0]
                    PXArray.append(tempx)
                    PYArray.append(tempy)
                    if Ccount is 3: #when you've got 4 points...

                        #Actual Points = P(i/N), so iteratively solve for these
                        for i in range(N):
                            mySVG.commands.append('L') #each move requires drawing a line
                            mySVG.xCoords.append(int(mySVG.evalCurveEqtn((float(i)/N), PXArray)))
                            mySVG.yCoords.append(int(mySVG.evalCurveEqtn((float(i)/N), PYArray)))

                        #the last point on the curve is the last point given from the file
                        mySVG.commands.append('L')
                        tempx = PXArray[3]
                        tempy = PXArray[3]
                        if lastComm is 'c': #again, if c is lowercase, it's relative
                            tempx += PXArray[0]
                            tempy += PYArray[0]
                        mySVG.xCoords.append(tempx)
                        mySVG.yCoords.append(tempy)
                        Ccount = 0 #reset the count in case you have another curve


                else:
                    if not lastElemLet:
                        #if the last command was an M or L, any non-explicit instru-
                        #ctions will be "L's" so we add that to the commands
                        mySVG.commands.append('L')

                    #split the element: before the comma is the x element, after is the y
                    tempx, tempy = mySVG.splitStrXY(element)

                    #if the last case was lower, we need to translate relative coords
                    #to absolute by adding them to the previous absolute coordinates
                    if not lastCaseUp:
                        tempx += lastXCoord
                        tempy += lastYCoord

                    #add the coordinates to teh corresponding arrays
                    mySVG.xCoords.append(tempx)
                    mySVG.yCoords.append(tempy)

                    #save the current x and y coordinates
                    lastXCoord = tempx
                    lastYCoord = tempy

                    #check to see if it's the first coordinate of the path
                    if pathFirstCoordFlag:
                        pathFirstXCoord = lastXCoord
                        pathFirstYCoord = lastYCoord
                        pathFirstCoordFlag = False

                    lastElemLet = False

    print mySVG.commands
    print mySVG.xCoords
    print mySVG.yCoords

    #start talking to Arduino
    index = 0
    for eachComm in mySVG.commands:
        readyByte = mySVG.ser.read() #read 1 byte from Arduino
        while readyByte is not 'R':()
        serOut, ardCheck = mySVG.talkToArduino(index)
        if serOut is ardCheck:
            mySVG.ser.write('G')
        else:
            serOut, ardCheck = mySVG.talkToArduino(index)
            if serOut is not ardCheck:
                print "ERROR" + serOut + ardCheck
                break
            else:
                mySVG.ser.write('G')
        index += 1
        print "serOut"
        readyByte = None
    mySVG.ser.close()

if __name__ == '__main__':
    main()