import cv2
import cv
cv2.namedWindow("asdf")
while(1):
	key = cv2.waitKey(30)
	if key != -1:
		strKey = str(key&0xff)
		print(strKey)
