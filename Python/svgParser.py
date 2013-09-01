#-------------------------------------------------------------------------------
# Name:        svgParser
# Purpose:
#
# Author:      Kayla
#
# Created:     30/08/2013
# Copyright:   (c) Kayla 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys
import re
from xml.dom import minidom



def readInFile(file):
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

def parsePaths(svgStr):
    '''
    Given a string, presumably the text from the SVG file,
    it will strip out the paths and put them into an array.

    '''
    doc = minidom.parseString(svgStr)
    pathStrings = [path.getAttribute('d') for path in
                    doc.getElementsByTagName('path')]
    doc.unlink()
    return pathStrings

def evalCurveEqtn(t, PArray):
    Pt = pow((1-t),3)*PArray[0] + 3*pow(1-t,2)*t*PArray[1] + 3*(1-t)*pow(t,2)*PArray[2] + pow(t,3)*PArray[3]
    return Pt

def splitStrXY(str):
    x = int(0.5+(float(str.split(',')[0])))
    y = int(0.5+(float(str.split(',')[1])))
    return x,y

def capFirstLetOnly(str)
     if str[0].islower:
        str = str[0].upper() + str[1:]

def main():

    #load in file - here I'm doing it manually
    file = "C:\Users\Kayla\Documents\School\Fall 2013\Senior Design\svgParser\curvySVG.txt"

    #instantiate some arrays we'll use
    commands = []
    xCoords = []
    yCoords = []

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
    svgStr = readInFile(file)
    pathStrings = parsePaths(svgStr)


    #iteratively run through the paths, correct letters, and reorganize
    #into the different arrays
    for path in pathStrings:
        path = capFirstLetOnly(path) #we want to make sure the first letter is capitalized
        elements = path.split(' ') #split the elements based on spaces
        pathFirstCoordFlag = True #raise the falg to say it's the first coord of the path

        #iterate through each element of the path i.e. each letter or number set
        for element in elements:
            #check to see if the element is an acceptable letter
            if re.match("[mlzcMLZC]", element):
                if re.match("[zZ]", element):
                   #if the letter is Z, then we need to close the loop by drawing
                   #back to the first coordinate of the path.  To do this, add a
                   #"L" to the command array, and put the initial x and y coords
                   #into the x and y arrays.
                   commands.append('L')
                   xCoords.append(pathFirstXCoord)
                   yCoords.append(pathFirstYCoord)
                   lastElemLet = True
                   lastComm = 'zZ'

                elif re.match("[cC]", element):
                    #if the letter is C, then just set the right flags, and we'll
                    #take care of it when we get to the actual numbers (see below)
                    if re.match("[c]", element):
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
                        commands.append(element.upper())
                    #if the letter isn't lowercase, change the flag and  add the
                    #element to the commands
                    else:
                        lastCaseUp = True
                        commands.append(element)
                    lastElemLet = True
                    lastComm = 'mMlL'

            #if the element isn't a letter...(it's a number)
            else:
                #this section will go through calculating a curve
                if lastComm is ('c' or 'C'):
                    if Ccount  is 0: #this is a counter to gather the curve coords
                        #the first point used to calucalte the curve is the previous point
                        PXArray.append(lastXCoord)
                        PYArray.append(lastYCoord)
                    Ccount += 1

                    #add the current coordinates to the PX and PY arrays
                    PXArray.append(splitStrXY(element)[0])
                    PYArray.append(splitStrXY(element)[1])
                    if Ccount is 3: #when you've got 4 points...

                        #Actual Points = P(i/N), so iteratively solve for these
                        for i in range(N):
                            commands.append('L') #each move requires drawing a line
                            tempx = evalCurveEqtn((i/N), PXArray)
                            tempy = evalCurveEqtn((i/N), PYArray)
                            if lastComm is 'c': #if c is lowercase, it's relative to the 1st point
                                tempx += PXArray[0]
                                tempy += PYArray[0]
                            xCoords.append(tempx)
                            yCoords.append(tempy)

                        #the last point on the curve is the last point given from the file
                        commands.append('L')
                        tempx = PXArray[3]
                        tempy = PXArray[3]
                        if lastComm is 'c': #again, if c is lowercase, it's relative
                            tempx += PXArray[0]
                            tempy += PYArray[0]
                        xCoords.append(tempx)
                        yCoords.append(tempy)
                        Ccount = 0 #reset the count in case you have another curve


                else:
                    if not lastElemLet:
                        #if the last command was an M or L, any non-explicit instru-
                        #ctions will be "L's" so we add that to the commands
                        commands.append('L')

                    #split the element: before the comma is the x element, after is the y
                    tempx, tempy = splitStrXY(element)

                    #if the last case was lower, we need to translate relative coords
                    #to absolute by adding them to the previous absolute coordinates
                    if not lastCaseUp:
                        tempx += lastXCoord
                        tempy += lastYCoord

                    #add the coordinates to teh corresponding arrays
                    xCoords.append(tempx)
                    yCoords.append(tempy)

                    #save the current x and y coordinates
                    lastXCoord = tempx
                    lastYCoord = tempy

                    #check to see if it's the first coordinate of the path
                    if pathFirstCoordFlag:
                        pathFirstXCoord = lastXCoord
                        pathFirstYCoord = lastYCoord
                        pathFirstCoordFlag = False

                    lastElemLet = False

    print commands
    print xCoords
    print yCoords

if __name__ == '__main__':
    main()