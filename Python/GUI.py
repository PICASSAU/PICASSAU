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

    def __init__(self, parent, image):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.initPic(image)
#        self.ser = serial.Serial('/dev/ttyUSB0') #9600 Baud, 8 data bits, No parity, 1 stop bit

    def initPic(self, img):

#        imageName = "../imageFiltering/webcam2.png"

        self.xmax = 506
        self.ymax = 379
        self.cropConstant = (20.0/26.0)
        self.croppedX = int(self.ymax*self.cropConstant)
        box = (0, 0, self.croppedX, self.ymax)

        self.parent.title("PICASSAU GUI")

#        self.img = Image.open(imageName)

	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	print "displaying image"
	pil_img = Image.fromarray(img)

        imgCropped = pil_img.crop(box)

        filteredImage = ImageTk.PhotoImage(imgCropped)
        labelImage = Tk.Label(image=filteredImage, background='white')

        labelImage.image = filteredImage
        labelImage.grid(row = 2, column = 1, rowspan= 5)

    def setGeometry(self, root):

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='white')


    def checkArduino(self):

        #start talking to Arduino
        print "Start talking to Arduino"

        arduinoMessage = self.readFromArduino()
        if arduinoMessage == 'T':
            self.sendToArduino('T')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                #do the "take picture" stuff
                pass
        elif arduinoMessage == 'C':
            self.sendToArduino('C')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                #do the "continue" stuff
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

def main():

    root = Tk.Tk()
    imgCounter = 0
    cam = cv2.VideoCapture(0)
    while imgCounter < 3:
        ret, frame = cam.read()
	imgCounter += 1
    ex = myGUI(root, frame)

    root.overrideredirect(1)  #this hides the title bar in the GUI

    text1 = Tk.Label(root, text= "    Take Picture >", font=("Helvetica", 32, "bold"), fg='black', bg = 'white')
    text1.grid(row = 2, column = 2)

    text2 = Tk.Label(root, text= "         Continue >", font=("Helvetica", 32, "bold"), fg='black', bg = 'white')
    text2.grid(row = 6, column = 2)
    ex.setGeometry(root)

    dummyText = Tk.Label(root, text = '    ', bg = 'white')
    dummyText.grid(row = 0, column = 0)

    dummyText2 = Tk.Label(root, text = '    ', bg = 'white')
    dummyText2.grid(row = 1, column = 0)

    root.after(5000, ex.close)
    root.after(100, ex.checkArduino)
    root.mainloop()

if __name__ == '__main__':
    main()
