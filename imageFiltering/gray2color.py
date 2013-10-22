import cv
import cv2
import numpy as np
import os

colorPalette = [[0,165,255],[255,118,72],[128,0,0]]

filePath = "./grayscale/"
fileNameBase = "testPicMorphed"
#fileNameEnd = "20130920-150353.png"
fileSavePath = "colored/"
fileSaveBase = "testPicColorized"

#fileName = filePath + fileNameBase + fileNameEnd
#fileSave = fileSavePath + fileSaveBase + fileNameEnd

for dirpath, dnames, fnames in os.walk(filePath):
	for f in fnames:
		if f[:14] == fileNameBase :
			fileNameEnd = f[14:]
			imMorphed = cv2.imread(os.path.join(dirpath,f),cv.CV_LOAD_IMAGE_GRAYSCALE)
			imColorize = np.zeros((imMorphed.shape[0],imMorphed.shape[1],3),dtype=np.uint8)

			imColorize[imMorphed == 0] = colorPalette[2]
			imColorize[imMorphed == 85] = colorPalette[1]
			imColorize[imMorphed == 170] = colorPalette[0]
			imColorize[imMorphed == 255] = [255,255,255]

			fileSave = fileSavePath + fileSaveBase + fileNameEnd
			cv2.imwrite(fileSave,imColorize)

