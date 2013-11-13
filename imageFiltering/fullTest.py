import cv2
import cv
import numpy as np
import time
import datetime
import potrace

def nothing(*args):
    pass

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
kernel = np.array( [[0,0,1,1,1,0,0],
                    [0,1,1,1,1,1,0],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1],
                    [0,1,1,1,1,1,0],
                    [0,0,1,1,1,0,0]], dtype = np.uint8)

tinyKernel = np.array( [[0,1,0],[1,1,1],[0,1,0]], dtype = np.uint8)
#colorPalette = np.array([[0,165,255],[255,118,72],[128,0,0]], dtype = np.uint8)
#colorPalette = 255 - colorPalette
#colorPalette[colorPalette == 0] = 1

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
        imBin1 = np.zeros_like(imMorphed)
        imBin2 = np.zeros_like(imMorphed)
        imBin3 = np.zeros_like(imMorphed)
        
        #break into binary images
        imBin1[imMorphed == 170] = 255
        imBin2[imMorphed == 85] = 255
        imBin3[imMorphed == 0] = 255

        #tiny erosion reduces color overlap and 
        #gets rid of tiny points that can occur on middle layers
        imBin1 = cv2.erode(imBin1,tinyKernel)
        imBin2 = cv2.erode(imBin2,tinyKernel)
        imBin3 = cv2.erode(imBin3,tinyKernel)

        while True:
            bmp = potrace.Bitmap(imBin1)    #bitmap in preparation for potrace
            path = bmp.trace()  #trace it
            if (path.curves == []): #check for blank
                break
            for curve in path:
                #tessellate aka break into line segments
                #yes, their function is mispelled
                tessellation = curve.tesselate() #uses the default 'adaptive' interpolation
                
                #add to array
                #erode
