#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        GUI.py
# Purpose:
#
# Author:      PICASSAU
#
# Created:     04/11/2013
# Copyright:   (c) Kayla 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk
import Tkinter as Tk
import serial
import cv2
import numpy as np

class myGUI(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
#        self.ser = serial.Serial('/dev/ttyUSB0') #9600 Baud, 8 data bits, No parity, 1 stop bit

    def initPic(self):

        self.xmax = 506
        self.ymax = 379
        self.cropConstant = (20.0/26.0)
        self.croppedX = int(self.ymax*self.cropConstant)
        box = (0, 0, self.croppedX, self.ymax)

        self.parent.title("PICASSAU GUI")

        img = self.takePicture()

    	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    	print "displaying image"
    	pil_img = Image.fromarray(img)

        imgCropped = pil_img.crop(box)

        filteredImage = ImageTk.PhotoImage(imgCropped)
	return filteredImage

    def setGeometry(self, root, image, str1, str2):

        text1 = Tk.Label(root, text= str1 + " >\n\n\n\n\n\n" + str2 + " >", font=("Helvetica", 32, "bold"), fg='black', bg = 'white', justify='right')
        text1.grid(row = 2, column = 2)


        #set image geometry
        labelImage = Tk.Label(image=image, background='white')

        labelImage.image = image
        labelImage.grid(row = 2, column = 1, rowspan= 5)

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='white')

        dummyText = Tk.Label(root, text = '    ', bg = 'white')
        dummyText.grid(row = 0, column = 0)

        dummyText2 = Tk.Label(root, text = '    ', bg = 'white')
        dummyText2.grid(row = 1, column = 0)

    def takePicture(self):
        imgCounter = 0
        cam = cv2.VideoCapture(0)
        while imgCounter < 3:
            ret, frame = cam.read()
            imgCounter += 1
        return frame

    def checkArduino(self):

        #start talking to Arduino
        print "Start talking to Arduino"

        arduinoMessage = self.readFromArduino()
        if arduinoMessage == 'T':
            self.sendToArduino('T\n')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                #do the "take picture" stuff
                pass
        elif arduinoMessage == 'C':
            self.sendToArduino('C\n')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
               self.areYouSure()
               pass
        elif 'D' in arduinoMessage:
            self.sendToArduino(arduinoMessage)
            if nextByte == 'G':
                self.threshold1 = arduinoMessage.split(',')[1]
                self.threshold2 = arduinoMessage.split(',')[2]
                self.threshold3 = arduinoMessage.split(',')[3]
        else:
            pass

        self.parent.after(100, ex.checkArduino)


    def readFromArduino(self):
        self.ser.flush()
        ardCheck = self.ser.readline()
        return ardCheck


    def sendToArduino(self, message):
        serOut = str(message) + '\n'
        self.ser.write(serOut)
        return serOut


    def close(self):
	self.parent.destroy()

    def areYouSure(self):
    	ays = Image.open("AreYouSure.png")
	ays = ImageTk.PhotoImage(ays)

        self.setGeometry(self.parent, ays, "         Go back", "Paint now")

def main():

    root = Tk.Tk()

    ex = myGUI(root)
    image = ex.initPic()

    root.overrideredirect(1)  #this hides the title bar in the GUI

    ex.setGeometry(root, image, "      Take Picture", "Continue")

    root.after(4000, ex.areYouSure)

    root.after(8000, ex.close)
    root.after(100, ex.checkArduino)
    root.mainloop()



if __name__ == '__main__':
    main()
