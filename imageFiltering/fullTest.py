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
    def __init__:
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
			return	#do nothing
		if (points.shape[0] < 2): #see if there are at least two points
			return	#do nothing
		
		#append the first point as an 'M'
		self.commands0.append('M')
		self.xcoords0.append(points[0,0])
		self.ycoords0.append(points[0,1])
		
		index = 1
		while( index < points.shape[0] ):
			self.commands0.append('L')
			self.xcoords0.append(points[index,0])
			self.ycoords0.append(points[index,1])
			index = index+1
            
    def addArray1(self, points):
        #do some error checking:
		if (points.shape[1] != 2): #should be 2 wide (x and y)
			return	#do nothing
		if (points.shape[0] < 2): #see if there are at least two points
			return	#do nothing
		
		#append the first point as an 'M'
		self.commands1.append('M')
		self.xcoords1.append(points[0,0])
		self.ycoords1.append(points[0,1])
		
		index = 1
		while( index < points.shape[0] ):
			self.commands1.append('L')
			self.xcoords1.append(points[index,0])
			self.ycoords1.append(points[index,1])
			index = index+1

    def addArray2(self, points):
        #do some error checking:
		if (points.shape[1] != 2): #should be 2 wide (x and y)
			return	#do nothing
		if (points.shape[0] < 2): #see if there are at least two points
			return	#do nothing
		
		#append the first point as an 'M'
		self.commands2.append('M')
		self.xcoords2.append(points[0,0])
		self.ycoords2.append(points[0,1])
		
		index = 1
		while( index < points.shape[0] ):
			self.commands2.append('L')
			self.xcoords2.append(points[index,0])
			self.ycoords2.append(points[index,1])
			index = index+1
            
    def writeToFile(self, file, list):
        file.write("[")
		strList = [str(i) for i in list]
		file.write(','.join(strList))
		file.write("]\n")
        
    def traceBin(self, imgBin, color)
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
                    addArray0(tessellation)
                elif (color == 1):
                    addArray1(tessellation)
                else
                    addArray2(tessellation)
            
            imgBin = cv2.erode(imgBin, kernel) #go one layer deeper

        
    def trace(self, img)
        imBin1 = np.zeros_like(img)
        imBin2 = np.zeros_like(img)
        imBin3 = np.zeros_like(img)
        
        #break into binary images
        imBin1[img == 170] = 255
        imBin2[img == 85] = 255
        imBin3[img == 0] = 255

        traceBin( imBin1, 0 )
        traceBin( imBin2, 1 )
        traceBin( imBin3, 2 )
        
class ImgProcessor():
    def __init__(self):
        self.cam = VideoCapture(0)
        self.thresh = (64,128,192)
        self.blurAmount = 7
        takePicture()
        processPictures()
        
    def takePicture(self):
        ret, frame = cam.read()
        self.frameCrop = frame[:,135:504,:]
        self.imColor = np.zeros_like(frame_crop)
        processPictures()
        
    def processPictures(self):
        self.imBlur = cv2.cvtColor(self.frameCrop, cv.CV_BGR2GRAY)
        self.imBlur = cv2.medianBlur(imBlur,self.blurAmt)
        self.imPost = np.copy(self.imBlur)
        self.imPost[self.imBlur >= thresh[2]] = 255
        self.imPost[(self.imBlur >= thresh[1]) & (self.imBlur < thresh[2])] = 170
        self.imPost[(self.imBlur >= thresh[0]) & (self.imBlur < thresh[1])] = 85
        self.imPost[self.imBlur < thresh[0]]  = 0
        self.imPost = cv2.morphologyEx(self.imPost,cv2.MORPH_OPEN,kernel)
        self.imPost = cv2.morphologyEx(self.imPost,cv2.MORPH_CLOSE,kernel)

        imColor = np.zeros_like(frame_crop)
        imColor[imPost == 0] = colorPalette[2]
        imColor[imPost == 85] = colorPalette[1]
        imColor[imPost == 170] = colorPalette[0]
        imColor[imPost == 255] = [255,255,255]

        self.displayImage = cv2.resize(imColor, (291,379))
        
    def getDisplayImage(self):
        return self.displayImage
        
    def getDisplayImage(self):
        return self.imPost
        
    def setKnobs(self, A, B, C):
        temp = A
        if B < A:
            temp = B
            B = A
            A = temp
        if C < temp2:
            temp3 = temp2
            temp2 = C
        if temp2 < temp1:
           
        
        self.thresh =
    
        
        
        

#cv2.namedWindow("original")
cv2.namedWindow("posterized")
#cv2.namedWindow("morphed")
vc = cv2.VideoCapture(0)
cv.CreateTrackbar("A","posterized",192,255,nothing)
cv.CreateTrackbar("B","posterized",128,255,nothing)
cv.CreateTrackbar("C","posterized",64,255,nothing)

strKey = "-1"
#kernel = np.array( [[0,0,0,1,1,1,0,0,0],
#            [0,0,1,1,1,1,1,0,0],
#            [0,1,1,1,1,1,1,1,0],
#            [1,1,1,1,1,1,1,1,1],
#            [1,1,1,1,1,1,1,1,1],
#            [1,1,1,1,1,1,1,1,1],
#            [0,1,1,1,1,1,1,1,0],
#            [0,0,1,1,1,1,1,0,0],
#            [0,0,0,1,1,1,0,0,0]] , dtype = np.uint8)


colorPalette = [[0,165,255],[255,118,72],[128,0,0]]

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    aBar = cv2.getTrackbarPos("A","posterized")
    bBar = cv2.getTrackbarPos("B","posterized")
    cBar = cv2.getTrackbarPos("C","posterized")
    blurAmt = 7#11

    if aBar < bBar:
        tempBar = aBar
        aBar = bBar
        bBar = tempBar
    if aBar < cBar:
        tempBar = aBar
        aBar = cBar
        cBar = tempBar
    if bBar < cBar:
        tempBar = bBar
        bBar = cBar
        cBar = tempBar
        
    frame_crop = frame[:,135:504,:] #crop the width to get the same
        # aspect ratio as our canvas
        #assumes that the frame starts as 480 x 640

    imCopy = np.copy(frame_crop)
    imColorize = np.zeros_like(frame_crop)
    
    imGray = cv2.cvtColor(imCopy, cv.CV_BGR2GRAY)

    imBlur = cv2.medianBlur(imGray,blurAmt)
    
    imPost = np.copy(imBlur)
    imPost[imPost >= aBar] = 255
    imPost[(imPost >= bBar) & (imPost < aBar)] = 170
    imPost[(imPost >= cBar) & (imPost < bBar)] = 85
    imPost[imPost < cBar]  = 0


    cv2.putText(frame, strKey, (400,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cv.Scalar(255,255,255), 1)

    
    imMorphed = cv2.morphologyEx(imPost,cv2.MORPH_OPEN,kernel)
    imMorphed = cv2.morphologyEx(imMorphed,cv2.MORPH_CLOSE,kernel)

    imColorize[imMorphed == 0] = colorPalette[2]
    imColorize[imMorphed == 85] = colorPalette[1]
    imColorize[imMorphed == 170] = colorPalette[0]
    imColorize[imMorphed == 255] = [255,255,255]

    imResized = cv2.resize(imColorize, (291,379))

    #cv2.imshow("original", frame)
    #cv2.imshow("posterized",imPost)
    #cv2.imshow("morphed",imMorphed)
    cv2.imshow("posterized",imResized)
    rval, frame = vc.read()
    key = cv2.waitKey(30)
    if key != -1:
        key = key & 0xff
        strKey = str(key)

    if key == 27: #ESC
        break
    if key == 32: #this is space... bar
        imageStrEnd = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S') + ".png"
        imBin1 = np.zeros_like(imMorphed)
        imBin2 = np.zeros_like(imMorphed)
        imBin3 = np.zeros_like(imMorphed)
        
        imBin1[imMorphed == 170] = 255
        imBin2[imMorphed == 85] = 255
        imBin3[imMorphed == 0] = 255

        cv2.imwrite(("./binIm/layer1_"+imageStrEnd),imBin1)
        cv2.imwrite(("./binIm/layer2_"+imageStrEnd),imBin2)
        cv2.imwrite(("./binIm/layer3_"+imageStrEnd),imBin3)
        
#        cv2.imwrite(("picOrig"+imageStrEnd), imCopy)
#        cv2.imwrite(("picGray"+imageStrEnd), imGray)
#        cv2.imwrite(("picBlur"+imageStrEnd), imBlur)
#        cv2.imwrite(("picPoster"+imageStrEnd), imPost)
#        cv2.imwrite(("picColor"+imageStrEnd), imColorize)

    if key == 10: #enter
        
