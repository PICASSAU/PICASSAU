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
        self.state = 0  #state representing the display status
                        # 0 = setup state (Take Picture, Continue)
                        # 1 = "are you sure" state
        self.ser = serial.Serial('/dev/ttyUSB0', timeout=10) #9600 Baud, 8 data bits, No parity, 1 stop bit
        self.ser.flushInput()

    def initPic(self):

        self.xmax = 506
        self.ymax = 379
        self.cropConstant = (20.0/26.0)
        self.croppedX = int(self.ymax*self.cropConstant)
        self.box = (0, 0, self.croppedX, self.ymax)
#        box = (0, 0, 291, 379)

        self.parent.title("PICASSAU GUI")

        img = self.takePicture()

    	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    	print "displaying image"
    	pil_img = Image.fromarray(img)

        imgCropped = pil_img.crop(self.box)

        filteredImage = ImageTk.PhotoImage(imgCropped)
        return filteredImage

    def setGeometry(self, root, image, str1, str2):

        self.buttonText = Tk.Label(root, text= str1 + " >\n\n\n\n\n\n" + str2 + " >", font=("Helvetica", 32, "bold"), fg="black", bg = "white", justify="right", width=15, anchor='e')
        self.buttonText.grid(row = 2, column = 2)


        #set image geometry
        self.labelImage = Tk.Label(image=image, background='white')

        #self.labelImage.image = image
        self.labelImage.grid(row = 2, column = 1, rowspan= 5)
        self.image = image  #must save in global var to make sure that
            #garbage collection doesn't clean it out

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='white')

        dummyText = Tk.Label(root, text = '    ', bg = 'white')
        dummyText.grid(row = 0, column = 0)

        dummyText2 = Tk.Label(root, text = '    ', bg = 'white')
        dummyText2.grid(row = 1, column = 0)

    def changeImage(self, image):
        self.labelImage.config(image = image )
        self.image = image #must save in global var to make sure that
            #garbage collection doesn't clean it out
    
    def changeText(self, str1, str2):
        self.buttonText.config( text = str1 + " >\n\n\n\n\n\n" + str2 + " >" )

    def takePicture(self):
        imgCounter = 0
        cam = cv2.VideoCapture(0)
        while imgCounter < 3:
            ret, frame = cam.read()
            imgCounter += 1
        return frame

    def checkArduino(self):
        #start talking to Arduino
        #print "Start talking to Arduino"

        arduinoMessage = self.readFromArduino()
        if arduinoMessage == 'T':
            self.sendToArduino('T\n')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                if self.state == 0:
                    #do the "take picture" stuff
                    pass
                else:
                    self.state = 0
                    self.changeText("Take Picture", "Continue")
                    #self.changeImage(dummyImage)
        elif arduinoMessage == 'C':
            self.sendToArduino('C\n')
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                if self.state == 0:
                    self.areYouSure()
                else:
                    self.endArduinoComm()
        elif arduinoMessage[0] == 'D':
            self.sendToArduino(arduinoMessage)
            nextByte = self.readFromArduino()
            if nextByte == 'G':
                if self.state == 0:
                    # self.threshold1 = arduinoMessage.split(',')[1]
                    # self.threshold2 = arduinoMessage.split(',')[2]
                    # self.threshold3 = arduinoMessage.split(',')[3]
                    pass
        else:
            pass

        self.parent.after(100, self.checkArduino)

    def readFromArduino(self):
        self.ser.flush()
        ardCheck = self.ser.readline().rstrip()
        
        print "Got: " + ardCheck
        return ardCheck

    def sendToArduino(self, message):
        serOut = str(message) + '\n'
        self.ser.write(serOut)
        return serOut

    def endArduinoComm(self):
        self.sendToArduino('X')
        firstByte = self.readFromArduino()
        if firstByte == 'X':
            self.sendToArduino('G')
            if secondByte == 'G':
                #start painting!!!!! 
                pass

    def close(self):
        self.parent.destroy()

    def areYouSure(self):
        ays = Image.open("AreYouSure.png")
        ays = ImageTk.PhotoImage(ays)
        self.changeImage(ays)
        self.changeText("Go back", "Paint now")
        self.state = 1

def main():

    root = Tk.Tk()

    ex = myGUI(root)
    image = ex.initPic()

    root.overrideredirect(1)  #this hides the title bar in the GUI

    ex.setGeometry(root, image, "Take Picture", "Continue")

    #root.after(4000, ex.areYouSure)

    root.after(60000, ex.close)
    root.after(100, ex.checkArduino)
    root.mainloop()



if __name__ == '__main__':
    main()
