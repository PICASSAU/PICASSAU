import numpy as np
import potrace
import cv2








def main():
	#cats()
	# Make a numpy array with a rectangle in the middle
	layer = cv2.imread("../imageFiltering/binIm/layer1.png",cv2.CV_LOAD_IMAGE_GRAYSCALE)

	# Create a bitmap from the array
	bmp = potrace.Bitmap(layer)

	# Trace the bitmap to a path
	path = bmp.trace()

	# Iterate over path curves
	for curve in path:
		print "start_point =", curve.start_point
		for segment in curve:
			print segment
			end_point_x, end_point_y = segment.end_point
			if segment.is_corner:
				c_x, c_y = segment.c
			else:
				c1_x, c1_y = segment.c1
				c2_x, c2_y = segment.c2


if __name__=="__main__":
	main()
