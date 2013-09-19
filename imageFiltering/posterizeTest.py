import cv2
import cv
import numpy as np

def nothing(*args):
	pass

#cv2.namedWindow("original")
cv2.namedWindow("posterized")
vc = cv2.VideoCapture(0)
cv.CreateTrackbar("Red","posterized",128,255,nothing)
#cv.CreateTrackbar("Blue","posterized",1,50,nothing)
#cv.CreateTrackbar("Green","posterized",0,3,nothing)

strKey = "-1"

if vc.isOpened():
	rval, frame = vc.read()
else:
	rval = False

while rval:
	rBar = cv2.getTrackbarPos("Red","posterized")
	#gBar = cv2.getTrackbarPos("Green","posterized")
	#bBar = cv2.getTrackbarPos("Blue","posterized")
	blurAmt = 11

	imPost = np.copy(frame)
	imPost = cv2.medianBlur(imPost,blurAmt)
	
	imPost[imPost >= rBar] = 255
	imPost[imPost < rBar]  = 0


	cv2.putText(frame, strKey, (400,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cv.Scalar(255,255,255), 1)

	#cv2.imshow("original", frame)
	cv2.imshow("posterized",imPost)
	rval, frame = vc.read()
	key = cv2.waitKey(30)
	if key != -1:
		strKey = str(key)

	if key == 1048603: #ESC
		break
