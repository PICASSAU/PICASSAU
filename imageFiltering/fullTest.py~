import cv2
import cv
import numpy as np
import time
import datetime
import potrace
import os
import serial

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

def nothing(*args):
    pass
    
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
    imProc = ImgProcessor()
    myTracer = Tracer()
    myArduino = ArduinoComm()
    
    imProc.camAutoAdjust()
    imProc.takePicture()
    
    
    while True:
        cv2.imshow("test",imProc.getDisplayImage())
        
        key = cv2.waitKey(30)
        if key != -1:
            key = key & 0xff

        if key == 27: #ESC
            myArduino.close()
            break
            
        if key == 32: #this is space... bar
            imProc.takePicture()

        if key == 10: #enter
            myTracer.trace(imProc.getPaintImage())
            myTracer.writeFile('../MATLAB/pythonOutput4.txt')
            cv2.imwrite("../MATLAB/outputPic4.png",imProc.getDisplayImage())
            myArduino.sendCoordsToArduino( myTracer.getArrays() )

        if key == ord('q'):
            imProc.setKnobs(imProc.thresh[0]+1,imProc.thresh[1],imProc.thresh[2])
            #imProc.processPicture()
        if key == ord('a'):
            imProc.setKnobs(imProc.thresh[0]-1,imProc.thresh[1],imProc.thresh[2])
            #imProc.processPicture()
        if key == ord('w'):
            imProc.setKnobs(imProc.thresh[0],imProc.thresh[1]+1,imProc.thresh[2])
            #imProc.processPicture()
        if key == ord('s'):
            imProc.setKnobs(imProc.thresh[0],imProc.thresh[1]-1,imProc.thresh[2])
            #imProc.processPicture()
        if key == ord('e'):
            imProc.setKnobs(imProc.thresh[0],imProc.thresh[1],imProc.thresh[2]+1)
            #imProc.processPicture()
        if key == ord('d'):
            imProc.setKnobs(imProc.thresh[0],imProc.thresh[1],imProc.thresh[2]-1)
            #imProc.processPicture()
        if key == ord('r'):
            imProc.processPicture()

if __name__ == "__main__":
    main()
