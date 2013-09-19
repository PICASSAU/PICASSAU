import cv2
import cv
import numpy as np

cv2.namedWindow("preview")
cv2.namedWindow("thresh")
vc = cv2.VideoCapture(0)

lowerThresh = np.array([100,100,100])
upperThresh = np.array([200,200,200])

palette = np.array([ [0,0,0],[255,153,1] ], dtype=np.uint8)

if vc.isOpened():
	rval, frame = vc.read()
	imgSize = frame.shape
	colorImgThresh = np.zeros((imgSize[0],imgSize[1],3), dtype=np.uint8)
else:
	rval = False

while rval:
	cv2.putText(frame,"Cool kid:", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, cv.Scalar(0,255,0),2)
	imgThresh = cv2.inRange(frame, lowerThresh, upperThresh)
	imgThresh.dtype=np.uint8
	
	colorImgThresh[0:imgSize[0],0:imgSize[1],0]=palette[1,0]*imgThresh
	colorImgThresh[0:imgSize[0],0:imgSize[1],1]=palette[1,1]*imgThresh
	colorImgThresh[0:imgSize[0],0:imgSize[1],2]=palette[1,2]*imgThresh
	
	#text for displaying the color code
	#strColorDebug = "(B,G,R)=(" + str(palette[1,0]) + "," + str(palette[1,1]) + "," + str(palette[1,2]) + ")"
	#cv2.putText(colorImgThresh, strColorDebug, (400,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cv.Scalar(255,255,255), 1)

	cv2.imshow("preview", frame)
	cv2.imshow("thresh",colorImgThresh)
	rval, frame = vc.read()
	key = cv2.waitKey(20)
	if key == 27:
		break
	if key == ord('q'):
		palette[1,0]+=1

