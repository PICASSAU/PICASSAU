import numpy as np
import potrace
<<<<<<< HEAD

# Make a numpy array with a rectangle in the middle
data = np.zeros((32, 32), np.uint32)
data[8:32-8, 8:32-8] = 1

# Create a bitmap from the array
bmp = potrace.Bitmap(data)

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
=======
import cv2
import os

class Tracer:
	def __init__(self):
		self.commands = ['C']
		self.xcoords = [0]
		self.ycoords = [1]
	
	#addArray takes an array of points and its it to the command and
	# coordinate arrays.
	#It assumes the first point should be an 'M'.
	def addArray(self, points):
		#do some error checking:
		if (points.shape[1] != 2): #should be 2 wide (x and y)
			return	#do nothing
		if (points.shape[0] < 2): #see if there are at least two points
			return	#do nothing
		
		#append the first point as an 'M'
		self.commands.append('M')
		self.xcoords.append(points[0,0])
		self.ycoords.append(points[0,1])
		
		index = 1
		while( index < points.shape[0] ):
			self.commands.append('L')
			self.xcoords.append(points[index,0])
			self.ycoords.append(points[index,1])
			index = index+1
	########

	def writeToFile(self, file, list):
		file.write("[")
		strList = [str(i) for i in list]
		file.write(','.join(strList))
		file.write("]\n")
	
		
#def curveBreak(start, c1, c2, end, t):
#	pt = pow((1-t),3)*start + 3*pow(1-t,2)*t*c1 + 3*(1-t)*pow(t,2)*c2 + pow(t,3)*end
#	return pt

def main():
	#cats()
	myTracer = Tracer()

	# Make a numpy array with a rectangle in the middle
	layer = cv2.imread("../imageFiltering/binIm/layer1.png",cv2.CV_LOAD_IMAGE_GRAYSCALE)

	# Create a bitmap from the array
	bmp = potrace.Bitmap(layer)

	# Trace the bitmap to a path
	path = bmp.trace()

	for curve in path:
		#tessellate aka break into line segments
		#yes, their function is mispelled
		tessellation = curve.tesselate() #uses the default 'adaptive' interpolation
		myTracer.addArray(tessellation)


	outputFileName = '../MATLAB/pythonOutput2.txt'
	if os.path.isfile(outputFileName):
		os.remove(outputFileName)
	file = open(outputFileName, 'w')

	file.write("commands0 = ")
	myTracer.writeToFile(file, myTracer.commands)
	file.write("xcoords0 = ")
	myTracer.writeToFile(file, myTracer.xcoords)
	file.write("ycoords0 = ")
	myTracer.writeToFile(file, myTracer.ycoords)
	
	file.write("commands1 = [C]")
	#mySVG.writeToFile(file, mySVG.commands1)
	file.write("xCoords1 = [1]")
	#mySVG.writeToFile(file, mySVG.xCoords1)
	file.write("yCoords1 = [0]")
	#mySVG.writeToFile(file, mySVG.yCoords1)
	
	file.write("commands2 = [C]")
	#mySVG.writeToFile(file, mySVG.commands2)
	file.write("xCoords2 = [2]")
	#mySVG.writeToFile(file, mySVG.xCoords2)
	file.write("yCoords2 =[0]")
	#mySVG.writeToFile(file, mySVG.yCoords2)
	
	file.close()



if __name__=="__main__":
	main()
>>>>>>> 4a42e0a1203095dc9c1ebf0642e2a6e407ce2ed3
