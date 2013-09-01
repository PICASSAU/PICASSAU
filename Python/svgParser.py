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
    xCoors = []
    yCoords = []

    #instantiate some flags

    #remember the last case used upper = True, lower = False
    lastCase = None

    #load in file - here I'm doing it manually
    file = "C:\Users\Kayla\Documents\School\Fall 2013\Senior Design\svgParser\complexsvg.txt"

    #read in the file and parse out the paths into an array of strings
    svgStr = readInFile(file)
    pathStrings = parsePaths(svgStr)

    #iteratively run through the paths, correct letters, and reorganize
    #into the different arrays
    for path in pathStrings:
        elements = path.split(' ')

        #iterate through each element of the path i.e. each letter or number set
        for element in elements:

            #check to see if the element is a letter (by checking if its a string)
            if re.match("[mlzcMLZC]", element):

                #if the letter is lowercase, change the lastCase flag and add
                #the uppercase version to the command array
                if element.islower():
                    lastCase = False
                    commands.append(element.upper())
                #if the letter isn't lowercase, change the flag and  add the
                #element to the commands
                else:
                    lastCase = True
                    commands.append(element)

            #if the element isn't a letter...
            else:








if __name__ == '__main__':
    main()