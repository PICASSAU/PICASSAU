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

def main():
    #instantiate some arrays we'll use
    commands = []
    xCoords = []
    yCoords = []

    #instantiate some flags

    #remember the last element: letter = True, number = False
    lastElemLet = None

    #remember the last case used: upper = True, lower = False
    lastCaseUp = None

    #remember the value of the last x and y coordinates
    lastXCoord = 0
    lastYCoord = 0

    #remember the first coordinate of each path
    pathFirstCoordFlag = None
    pathFirstXCoord = 0
    pathFirstYCoord = 0

    #load in file - here I'm doing it manually
    file = "C:\Users\Kayla\Documents\School\Fall 2013\Senior Design\svgParser\Kaylassvg.txt"

    #read in the file and parse out the paths into an array of strings
    svgStr = readInFile(file)
    pathStrings = parsePaths(svgStr)


    #iteratively run through the paths, correct letters, and reorganize
    #into the different arrays
    for path in pathStrings:
        if path[0].islower:
            path = path[0].upper() + path[1:]
        elements = path.split(' ')
        pathFirstCoordFlag = True


        #iterate through each element of the path i.e. each letter or number set
        for element in elements:
            #check to see if the element is an acceptable letter
            if re.match("[mlzcMLZC]", element):
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

                lastElemLet = True #for the next element, we'll know we last had a letter

            #if the element isn't a letter...(it's a number)
            else:
                if not lastElemLet: #if the last element wasn't a letter, we need
                                 #to add an "L" to the command array
                    commands.append('L')

                lastElemLet = False

                #split the element: before the comma is the x element, after is the y
                tempx = int(0.5+(float(element.split(',')[0])))
                tempy = int(0.5+(float(element.split(',')[1])))

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

if __name__ == '__main__':
    main()