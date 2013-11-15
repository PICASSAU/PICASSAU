import cv2
import cv
import numpy as np
import time
import datetime
import potrace
import os

kernel = np.array( [[0,0,1,1,1,0,0],
                    [0,1,1,1,1,1,0],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [0,1,1,1,1,1,0],
                    [0,0,1,1,1,0,0]], dtype = np.uint8)

tinyKernel = np.array( [[0,1,0],[1,1,1],[0,1,0]], dtype = np.uint8)

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
        
        canvasX = 20.0
        canvasY = 26.0
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
        self.xCoords0.append(int(self.scaleFactorX*points[0,0]+0.5))
        self.yCoords0.append(int(self.scaleFactorY*points[0,1]+0.5))
        
        index = 1
        while( index < points.shape[0] ):
            self.commands0.append('L')
            self.xCoords0.append(int(self.scaleFactorX*points[index,0]+0.5))
            self.yCoords0.append(int(self.scaleFactorY*points[index,1]+0.5))
            index = index+1
            
    def addArray1(self, points):
        #do some error checking:
        if (points.shape[1] != 2): #should be 2 wide (x and y)
            return    #do nothing
        if (points.shape[0] < 2): #see if there are at least two points
            return    #do nothing
        
        #append the first point as an 'M'
        self.commands1.append('M')
        self.xCoords1.append(int(self.scaleFactorX*points[0,0]+0.5))
        self.yCoords1.append(int(self.scaleFactorY*points[0,1]+0.5))
        
        index = 1
        while( index < points.shape[0] ):
            self.commands1.append('L')
            self.xCoords1.append(int(self.scaleFactorX*points[index,0]+0.5))
            self.yCoords1.append(int(self.scaleFactorY*points[index,1]+0.5))
            index = index+1

    def addArray2(self, points):
        #do some error checking:
        if (points.shape[1] != 2): #should be 2 wide (x and y)
            return    #do nothing
        if (points.shape[0] < 2): #see if there are at least two points
            return    #do nothing
        
        #append the first point as an 'M'
        self.commands2.append('M')
        self.xCoords2.append(int(self.scaleFactorX*points[0,0]+0.5))
        self.yCoords2.append(int(self.scaleFactorY*points[0,1]+0.5))
        
        index = 1
        while( index < points.shape[0] ):
            self.commands2.append('L')
            self.xCoords2.append(int(self.scaleFactorX*points[index,0]+0.5))
            self.yCoords2.append(int(self.scaleFactorY*points[index,1]+0.5))
            index = index+1
            
    def writeToFile(self, file, list):
        file.write("[")
        strList = [str(i) for i in list]
        file.write(','.join(strList))
        file.write("]\n")
        
    def traceBin(self, imgBin, color):
        #tiny erosion reduces color overlap and 
        #gets rid of tiny points that can occur on middle layers
        imgBin = cv2.erode(imgBin,tinyKernel)

        while True:
            bmp = potrace.Bitmap(imgBin)    #bitmap in preparation for potrace
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
            
            imgBin = cv2.erode(imgBin, kernel) #go one layer deeper

        
    def trace(self, img):
        imBin1 = np.zeros_like(img)
        imBin2 = np.zeros_like(img)
        imBin3 = np.zeros_like(img)
        
        #break into binary images
        imBin1[img == 170] = 255
        imBin2[img == 85] = 255
        imBin3[img == 0] = 255

        self.traceBin( imBin1, 0 )
        self.traceBin( imBin2, 1 )
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
        self.imPost = cv2.morphologyEx(self.imPost,cv2.MORPH_OPEN,kernel)
        self.imPost = cv2.morphologyEx(self.imPost,cv2.MORPH_CLOSE,kernel)

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
    

def main():
    imProc = ImgProcessor()
    myTracer = Tracer()
    
    imProc.camAutoAdjust()
    imProc.takePicture()
    
    while True:
        cv2.imshow("test",imProc.getDisplayImage())
        
        key = cv2.waitKey(30)
        if key != -1:
            key = key & 0xff

        if key == 27: #ESC
            break
            
        if key == 32: #this is space... bar
            imProc.takePicture()

        if key == 10: #enter
            myTracer.trace(imProc.getPaintImage())
            myTracer.writeFile('../MATLAB/pythonOutput3.txt')
            cv2.imwrite("../MATLAB/outputPic.png",imProc.getDisplayImage())
            break

if __name__ == "__main__":
    main()
