import cv2
import cv
import numpy as np

cv2.namedWindow("preview")
cv2.namedWindow("thresh")
vc = cv2.VideoCapture(0)

thresh0 = np.array([0,0,0])
thresh1 = np.array([100,100,100])
thresh2 = np.array([200,200,200])
thresh3 = np.array([255,255,255])

palette = np.array([ [0,0,0],[255,153,1],[100,250,250] ], dtype=np.uint8)
strKey = "-1"

if vc.isOpened():
	rval, frame = vc.read()
	imgSize = frame.shape
	orangeImgThresh = np.zeros((imgSize[0],imgSize[1],3), dtype=np.uint8)
	blueImgThresh = np.zeros((imgSize[0],imgSize[1],3), dtype=np.uint8)
	colorImgThresh = np.zeros((imgSize[0],imgSize[1],3), dtype=np.uint8)
else:
	rval = False

while rval:
	cv2.putText(frame,"SNARF", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, cv.Scalar(0,255,0),2)
	
	imgThresh = cv2.inRange(frame, thresh1, thresh2)
	#imgThresh.dtype=np.uint8
	
	orangeImgThresh[0:imgSize[0],0:imgSize[1],0]=palette[1,0]*imgThresh
	orangeImgThresh[0:imgSize[0],0:imgSize[1],1]=palette[1,1]*imgThresh
	orangeImgThresh[0:imgSize[0],0:imgSize[1],2]=palette[1,2]*imgThresh

	imgThresh2 = cv2.inRange(frame, thresh0, thresh1)
	
	blueImgThresh[0:imgSize[0],0:imgSize[1],0]=palette[2,0]*imgThresh2
	blueImgThresh[0:imgSize[0],0:imgSize[1],1]=palette[2,1]*imgThresh2
	blueImgThresh[0:imgSize[0],0:imgSize[1],2]=palette[2,2]*imgThresh2

	colorImgThresh = cv2.add(blueImgThresh, orangeImgThresh)

	#text for displaying the color code
	strDebug1 = "thresh1=(" + str(thresh1[0]) + "," + str(thresh1[1]) + "," + str(thresh1[2]) + ")"
	strDebug2 = "thresh2=(" + str(thresh2[0]) + "," + str(thresh2[1]) + "," + str(thresh2[2]) + ")"
	cv2.putText(colorImgThresh, strDebug1, (400,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cv.Scalar(255,255,255), 1)
	cv2.putText(colorImgThresh, strDebug2, (400,70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cv.Scalar(255,255,255), 1)
	
	cv2.putText(colorImgThresh, strKey, (400,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cv.Scalar(255,255,255), 1)

	cv2.imshow("preview", frame)
	cv2.imshow("thresh",colorImgThresh)
	rval, frame = vc.read()
	key = cv2.waitKey(20)
	if key != -1:
		strKey = str(key)

	if key == 1048603: #ESC
		break
	if key == 1048689: #q
		thresh1[0]+=1
		thresh1[1]+=1
		thresh1[2]+=1
	if key == 1048695: #w
		thresh2[0]+=1
		thresh2[1]+=1
		thresh2[2]+=1
	if key == 1048673: #a
		thresh1[0]-=1
		thresh1[1]-=1
		thresh1[2]-=1
	if key == 1048691: #s
		thresh2[0]-=1
		thresh2[1]-=1
		thresh2[2]-=1
