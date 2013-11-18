#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        GUI.py
# Purpose:
#
# Author:      PICASSAU
#
# Created:     04/11/2013
# Copyright:   (c) Kayla 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk
import Tkinter as Tk
import serial
import cv2
import cv
import numpy as np
import time
import datetime
import potrace
import os

#the comm port:
portName = "/dev/ttyUSB0"
#do you want to save the vector coordinates in a text file?
recordOutputCoordinateFile = False
#if so, where?
outputCoordinateFileName = "../MATLAB/pythonOutput.txt"
#do you want to save the processed image file?
recordOutputImageFile = True
#if so, where? (should be .png extension)
outputImageFileName = "../MATLAB/outputPic.png"




#the kernels used in the image processing and tracing
kernel9 = np.array( [[0,0,1,1,1,1,1,0,0],
                     [0,1,1,1,1,1,1,1,0],
                     [1,1,1,1,1,1,1,1,1],
                     [1,1,1,1,1,1,1,1,1],
                     [1,1,1,1,1,1,1,1,1],
                     [1,1,1,1,1,1,1,1,1],
                     [1,1,1,1,1,1,1,1,1],
                     [0,1,1,1,1,1,1,1,0],
                     [0,0,1,1,1,1,1,0,0]], dtype = np.uint8)

kernel7 = np.array( [[0,0,1,1,1,0,0],
                    [0,1,1,1,1,1,0],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [0,1,1,1,1,1,0],
                    [0,0,1,1,1,0,0]], dtype = np.uint8)

kernel5 = np.array( [[0,1,1,1,0],
                    [1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],
                    [0,1,1,1,0]], dtype = np.uint8)

kernel3 = np.array( [[0,1,0],[1,1,1],[0,1,0]], dtype = np.uint8)

class GUI(Tk.Frame):

    def __init__(self, parent, imProc, myTracer, paintComm):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.imProc = imProc
        self.myTracer = myTracer
        self.paintComm = paintComm
        self.state = 0  #state representing the display status
                        # 0 = setup state (Take Picture, Continue)
                        # 1 = "are you sure" state
        self.ser = serial.Serial(portName, timeout=1) #9600 Baud, 8 data bits, No parity, 1 stop bit
        self.ser.flushInput()

    def initPic(self):

        self.xmax = 506
        self.ymax = 379
        self.cropConstant = (20.0/26.0)
        self.croppedX = int(self.ymax*self.cropConstant)
        self.box = (0, 0, self.croppedX, self.ymax)
#        box = (0, 0, 291, 379)

        self.parent.title("PICASSAU GUI")

        img = self.takePicture()

    	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    	print "displaying image"
    	pil_img = Image.fromarray(img)

        imgCropped = pil_img.crop(self.box)

        filteredImage = ImageTk.PhotoImage(imgCropped)
        return filteredImage

    def setGeometry(self, root, image, str1, str2):

        self.buttonText = Tk.Label(root, text= str1 + " >\n\n\n\n\n\n" + str2 + " >", font=("Helvetica", 32, "bold"), fg="black", bg = "white", justify="right", width=15, anchor='e')
        self.buttonText.grid(row = 2, column = 2)


        #set image geometry
        self.labelImage = Tk.Label(image=image, background='white')

        #self.labelImage.image = image
        self.labelImage.grid(row = 2, column = 1, rowspan= 5)
        self.image = image  #must save in global var to make sure that
            #garbage collection doesn't clean it out

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='white')

        dummyText = Tk.Label(root, text = '    ', bg = 'white')
        dummyText.grid(row = 0, column = 0)

        dummyText2 = Tk.Label(root, text = '    ', bg = 'white')
        dummyText2.grid(row = 1, column = 0)

    def changeImage(self, image):
        self.labelImage.config(image = image )
        self.image = image #must save in global var to make sure that
            #garbage collection doesn't clean it out
    
    def changeText(self, str1, str2):
        self.buttonText.config( text = str1 + " >\n\n\n\n\n\n" + str2 + " >" )

    def takePicture(self):
        imgCounter = 0
        cam = cv2.VideoCapture(0)
        while imgCounter < 3:
            ret, frame = cam.read()
            imgCounter += 1
        return frame

    def checkArduino(self):
        #start talking to Arduino
        #print "Start talking to Arduino"

        arduinoMessage = self.readFromArduino()
        if arduinoMessage == 'T':
            self.sendToArduino('T\n')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                if self.state == 0:
                    #do the "take picture" stuff
                    self.imProc.takePicture()
                    self.changeImage(ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.imProc.getDisplayImage(),cv2.COLOR_BGR2RGB))))
                else:
                    #go back to the main screen
                    self.state = 0
                    self.changeText("Take Picture", "Continue")
                    self.changeImage(ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.imProc.getDisplayImage(),cv2.COLOR_BGR2RGB))))
        elif arduinoMessage == 'C':
            self.sendToArduino('C\n')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                if self.state == 0:
                    #go to the confirmation screen
                    self.areYouSure()
                else:
                    #go the the painting stuff
                    self.endArduinoComm()
                    #then start over
                    self.state = 0
                    #self.imProc.takePicture()
                    self.changeText("Take Picture", "Continue")
                    self.changeImage(ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.imProc.getDisplayImage(),cv2.COLOR_BGR2RGB))))
        elif arduinoMessage[0] == 'D':
            self.sendToArduino(arduinoMessage)
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                if self.state == 0:
                    try:
                        thresh1 = int(arduinoMessage.split(',')[1])
                        thresh2 = int(arduinoMessage.split(',')[2])
                        thresh3 = int(arduinoMessage.split(',')[3])
                        self.imProc.setKnobs(thresh1, thresh2, thresh3)
                        self.imProc.processPicture()
                        self.changeImage(ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.imProc.getDisplayImage(),cv2.COLOR_BGR2RGB))))
                    except ValueError:
                        print "Error converting D command: " + arduinoMessage
                #no need to do anything if in state 1
        else:
            pass

        self.parent.after(100, self.checkArduino)

    def readFromArduino(self):
        self.ser.flush()
        ardCheck = self.ser.readline().rstrip()
        
        print "Got: " + ardCheck
        return ardCheck

    def sendToArduino(self, message):
        serOut = str(message) + '\n'
        self.ser.write(serOut)
        return serOut

    def endArduinoComm(self):
        self.sendToArduino('X')
        firstByte = self.readFromArduino()
        while firstByte != 'X': #keep trying
            self.sendToArduino('X')
            firstByte = self.readFromArduino()
        
        self.sendToArduino('G')
        self.ser.flush() #wait for it to finish sending
        self.ser.close() #release the port
        painting()
        
    def painting(self):
        self.myTracer.trace(imProc.getPaintImage())
        if (recordOutputCoordinateFile):
            self.myTracer.writeFile(outputCoordinateFileName)
        if (recordOutputImageFile):
            cv2.imwrite(outputImageFileName,self.imProc.getDisplayImage())
        self.paintComm.sendCoordsToArduino( self.myTracer.getArrays() )
            

    def close(self):
        self.parent.destroy()

    def areYouSure(self):
        ays = Image.open("AreYouSure.png")
        ays = ImageTk.PhotoImage(ays)
        self.changeImage(ays)
        self.changeText("Go back", "Paint now")
        self.state = 1


class Tracer():
    def __init__(self):
        self.commands0 = ['C']
        self.xCoords0 = [0]
        self.yCoords0 = [0]

        self.commands1 = ['C']
        self.xCoords1 = [1]
        self.yCoords1 = [0]

        self.commands2 = ['C']
        self.xCoords2 = [2]
        self.yCoords2 = [0]
        
        canvasX = 18.0#20.0
        canvasY = 14.0#26.0
        imgX = 369.0
        imgY = 480.0
        ardDist = (200/8.25)
        
        self.scaleFactorX = canvasX*ardDist/imgX
        self.scaleFactorY = canvasY*ardDist/imgY
        
    
    #addArray takes an array of points and its it to the command and
    # coordinate arrays.    
    #It assumes the first point should be an 'M'. 
    def addArray0(self, points):
        #do some error checking:
        if (points.shape[1] != 2): #should be 2 wide (x and y)
            return    #do nothing
        if (points.shape[0] < 2): #see if there are at least two points
            return    #do nothing
        
        #append the first point as an 'M'
        self.commands0.append('M')
        self.xCoords0.append(int(self.scaleFactorX*(points[0,0]-1)+0.5))
        self.yCoords0.append(int(self.scaleFactorY*(points[0,1]-1)+0.5))
        
        index = 1
        while( index < points.shape[0] ):
            self.commands0.append('L')
            self.xCoords0.append(int(self.scaleFactorX*(points[index,0]-1)+0.5))
            self.yCoords0.append(int(self.scaleFactorY*(points[index,1]-1)+0.5))
            index = index+1
            
    def addArray1(self, points):
        #do some error checking:
        if (points.shape[1] != 2): #should be 2 wide (x and y)
            return    #do nothing
        if (points.shape[0] < 2): #see if there are at least two points
            return    #do nothing
        
        #append the first point as an 'M'
        self.commands1.append('M')
        self.xCoords1.append(int(self.scaleFactorX*(points[0,0]-1)+0.5))
        self.yCoords1.append(int(self.scaleFactorY*(points[0,1]-1)+0.5))
        
        index = 1
        while( index < points.shape[0] ):
            self.commands1.append('L')
            self.xCoords1.append(int(self.scaleFactorX*(points[index,0]-1)+0.5))
            self.yCoords1.append(int(self.scaleFactorY*(points[index,1]-1)+0.5))
            index = index+1

    def addArray2(self, points):
        #do some error checking:
        if (points.shape[1] != 2): #should be 2 wide (x and y)
            return    #do nothing
        if (points.shape[0] < 2): #see if there are at least two points
            return    #do nothing
        
        #append the first point as an 'M'
        self.commands2.append('M')
        self.xCoords2.append(int(self.scaleFactorX*(points[0,0]-1)+0.5))
        self.yCoords2.append(int(self.scaleFactorY*(points[0,1]-1)+0.5))
        
        index = 1
        while( index < points.shape[0] ):
            self.commands2.append('L')
            self.xCoords2.append(int(self.scaleFactorX*(points[index,0]-1)+0.5))
            self.yCoords2.append(int(self.scaleFactorY*(points[index,1]-1)+0.5))
            index = index+1
            
    def writeToFile(self, file, list):
        file.write("[")
        strList = [str(i) for i in list]
        file.write(','.join(strList))
        file.write("]\n")
        
    def traceBin(self, imgBin, color):
        #tiny erosion reduces color overlap and 
        #gets rid of tiny points that can occur on middle layers
        imgBin = cv2.erode(imgBin,kernel5)

        size = np.shape(imgBin)

        #pad a border around the binary image. This will allow the erosions to
        #erode away from the edge of the canvas
        imgBinPadded = zeros((size[0]+2, size[1]+2), dtype=np.uint8)
        imgBinPadded[1:-1,1:-1] = imgBin

        while True:
            bmp = potrace.Bitmap(imgBinPadded)    #bitmap in preparation for potrace
            path = bmp.trace()  #trace it
            if (path.curves == []): #check for blank
                break
            for curve in path:
                #tessellate aka break into line segments
                #yes, their function is mispelled
                tessellation = curve.tesselate() #uses the default 'adaptive' interpolation
                #and now put coords into the array
                if (color == 0):
                    self.addArray0(tessellation)
                elif (color == 1):
                    self.addArray1(tessellation)
                else:
                    self.addArray2(tessellation)
            
            imgBin = cv2.erode(imgBinPadded, kernel9) #go one layer deeper

        
    def trace(self, img):
        imBin1 = np.zeros_like(img)
        imBin2 = np.zeros_like(img)
        imBin3 = np.zeros_like(img)
        
        #break into binary images
        imBin1[img == 170] = 255
        imBin2[img == 85] = 255
        imBin3[img == 0] = 255

        self.traceBin( imBin2, 0 )
        self.traceBin( imBin1, 1 )
        self.traceBin( imBin3, 2 )
        
    def clearArrays(self):
        self.commands0 = ['C']
        self.xCoords0 = [0]
        self.yCoords0 = [0]

        self.commands1 = ['C']
        self.xCoords1 = [1]
        self.yCoords1 = [0]

        self.commands2 = ['C']
        self.xCoords2 = [2]
        self.yCoords2 = [0]
        
    def getArrays(self):
        return self.commands0, self.xCoords0, self.yCoords0, self.commands1, self.xCoords1, self.yCoords1, self.commands2, self.xCoords2, self.yCoords2
        
    def writeArray(self, file, list):
        file.write("[")
        strList = [str(i) for i in list]
        file.write(','.join(strList))
        file.write("]\n")
    
    def writeFile(self, fileName):
        if os.path.isfile(fileName):
            os.remove(fileName)
        file = open(fileName, 'w')

        file.write("commands0 = ")
        self.writeToFile(file, self.commands0)
        file.write("xcoords0 = ")
        self.writeToFile(file, self.xCoords0)
        file.write("ycoords0 = ")
        self.writeToFile(file, self.yCoords0)
        
        file.write("commands1 = ")
        self.writeToFile(file, self.commands1)
        file.write("xCoords1 = ")
        self.writeToFile(file, self.xCoords1)
        file.write("yCoords1 = ")
        self.writeToFile(file, self.yCoords1)
        
        file.write("commands2 = ")
        self.writeToFile(file, self.commands2)
        file.write("xCoords2 = ")
        self.writeToFile(file, self.xCoords2)
        file.write("yCoords2 = ")
        self.writeToFile(file, self.yCoords2)
        
        file.close()
        

class ImgProcessor():
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.thresh = (64,128,192)
        self.blurAmount = 7
        self.colorPalette = [[0,165,255],[255,118,72],[128,0,0]]
        
        self.takePicture()
        self.processPicture()
    
    def camAutoAdjust(self):    #let the camera auto-adjust itself by taking a bunch of pictures
        cnt = 0
        while cnt < 10:
            r, f = self.cam.read()
            cnt += 1
    
    def takePicture(self):
        self.camAutoAdjust()
        ret, frame = self.cam.read()
        #if not ret:
        #    print "aslfdsdalkbgjlsdakbvjsdalfj"
        frameCrop = frame[:,135:504,:]
        self.imColor = np.zeros_like(frameCrop)
        self.imBlur = cv2.cvtColor(frameCrop, cv.CV_BGR2GRAY)
        self.imBlur = cv2.medianBlur(self.imBlur,self.blurAmount)
        self.processPicture()
        
    def processPicture(self):
        
        self.imPost = np.copy(self.imBlur)
        self.imPost[self.imBlur >= self.thresh[2]] = 255
        self.imPost[(self.imBlur >= self.thresh[1]) & (self.imBlur < self.thresh[2])] = 170
        self.imPost[(self.imBlur >= self.thresh[0]) & (self.imBlur < self.thresh[1])] = 85
        self.imPost[self.imBlur < self.thresh[0]]  = 0
        self.imPost = cv2.morphologyEx(self.imPost,cv2.MORPH_OPEN,kernel7)
        self.imPost = cv2.morphologyEx(self.imPost,cv2.MORPH_CLOSE,kernel7)

        self.imColor = np.zeros_like(self.imColor)
        self.imColor[self.imPost == 0] = self.colorPalette[2]
        self.imColor[self.imPost == 85] = self.colorPalette[1]
        self.imColor[self.imPost == 170] = self.colorPalette[0]
        self.imColor[self.imPost == 255] = [255,255,255]

        self.displayImage = cv2.resize(self.imColor, (291,379))
        
    def getDisplayImage(self):
        return self.displayImage
        
    def getPaintImage(self):
        return self.imPost
        
    def setKnobs(self, A, B, C):
        temp = A
        if B < A:   #check A and B and make A lower
            temp = B
            B = A
            A = temp
        if C < B:   #check B and C and make B lower
            temp = C
            C = B
            B = temp
            if B < A:   #if need be, check the new B and A
                temp = B
                B = A
                A = temp
        
        self.thresh = (A, B, C)
        

# Only does the painting comm, not the GUI comm
# (GUI comm is handled by GUI class)
class ArduinoComm():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0') #9600 Baud, 8 data bits, No parity, 1 stop bit
    
    def close():
        self.ser.close()    #close the comm port
    
    def sendCoordsToArduino(self, (c0, x0, y0, c1, x1, y1, c2, x2, y2)):
        print "Start talking to Arduino"
        self.sendSingleColor(c0, x0, y0)
        self.sendSingleColor(c1, x1, y1)
        self.sendSingleColor(c2, x2, y2)
        readyByte = self.ser.read() #read 1 byte from Arduino
        while readyByte is not 'R':
            readyByte = self.ser.read() #wait for the ready signal from the Arduino #wait for the ready signal from the Arduino
        print "got ready signal"
        self.ser.write('D\n')
        ardCheck = self.readFromArduino()
        while 'D' not in ardCheck:
            ardCheck = self.readFromArduino()
            self.ser.write('D\n')
        self.ser.write('G\n')
        print "done"
        
    def sendSingleColor(self, c, x, y):
        index = 0
        for eachComm in c:
            serOut = None
            ardCheck = None
            
            readyByte = self.ser.read() #read 1 byte from Arduino
            while readyByte is not 'R':
                readyByte = self.ser.read() #wait for ready signal
            print "got ready signal"
            serOut = self.sendCoord(c, x, y, index) #send coordinate
            print "serOut: "
            ardCheck = self.readFromArduino()   #check for echo
            print "ardCheck: " + ardCheck
            if '\n' in ardCheck: #sometimes the check is just a new line character
                                 #if this is the case, read it again
                ardCheck = self.readFromArduino()
                print ardCheck
            while(serOut != ardCheck): #we're looking for our output to match the check
                                        #so keep sending/reading until they match
                serOut = self.sendCoord(c, x, y, index)
                ardCheck = self.readFromArduino()
                print "serOut: " + serOut
                print "ardCheck: " + ardCheck
            self.ser.write('G\n')#when you get the instructions to match, send out a
                                   #go signal and wait for the Arduino to be ready again
            print 'G'
            index += 1
            readyByte = None
        #Next command...    
            
    def sendCoord(self, c, x, y, i):
        serOut = str(c[i]) + ' ' + str(x[i]) + ',' + str(y[i]) + '\n'
        self.ser.write(serOut)
        return serOut
    
    def readFromArduino(self):
        self.ser.flush()
        ardCheck = self.ser.readline()
        return ardCheck
        
        
def main():

    root = Tk.Tk()
    
    imProc = ImgProcessor()
    myTracer = Tracer()
    myArduino = ArduinoComm()

    imProc.camAutoAdjust()
    imProc.takePicture()

    myGUI = GUI(root, imProc, myTracer, myArduino)

    root.overrideredirect(1)  #this hides the title bar in the GUI

    
    image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(imProc.getDisplayImage(),cv2.COLOR_BGR2RGB)))

    myGUI.setGeometry(root, image , "Take Picture", "Continue")

    #root.after(60000, myGUI.close) #used in debugging to make it close after 60sec
    root.after(100, myGUI.checkArduino)
    root.mainloop()



if __name__ == '__main__':
    main()
