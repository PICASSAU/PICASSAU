#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Kayla
#
# Created:     04/11/2013
# Copyright:   (c) Kayla 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PIL import Image, ImageTk
import Tkinter as Tk


class myGUI(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.initPic()
        self.ser = serial.Serial('/dev/ttyUSB0') #9600 Baud, 8 data bits, No parity, 1 stop bit

    def initPic(self):

        imageName = "../imageFiltering/webcam2.png"

        self.xmax = 506
        self.ymax = 379
        self.cropConstant = (20.0/26.0)
        self.croppedX = int(self.ymax*self.cropConstant)
        box = (0, 0, self.croppedX, self.ymax)


        self.parent.title("Label")

        self.img = Image.open(imageName)
        self.imgCropped = self.img.crop(box)
        self.filteredImage = ImageTk.PhotoImage(self.imgCropped)
        labelImage = Tk.Label(image=self.filteredImage, background='white')

        labelImage.image = self.filteredImage
        labelImage.grid(row = 2, column = 1, rowspan= 5)


    def setGeometry(self, root):
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='white')


    def readFromArduino(self):
        self.ser.flush()
        ardCheck = self.ser.readline()
        return ardCheck


    def sendToArduino(self, message):
        serOut = str(message) + '\n'
        self.ser.write(serOut)
        return serOut


def main():

    root = Tk.Tk()
    ex = Example(root)

    root.overrideredirect(1)

    text1 = Tk.Label(root, text= "    Take Picture >", font=("Helvetica", 32, "bold"), fg='black', bg = 'white')
    text1.grid(row = 2, column = 2)

    text2 = Tk.Label(root, text= "         Continue >", font=("Helvetica", 32, "bold"), fg='black', bg = 'white')
    text2.grid(row = 6, column = 2)
    ex.setGeometry(root)

    dummyText = Tk.Label(root, text = '    ', bg = 'white')
    dummyText.grid(row = 0, column = 0)

    dummyText2 = Tk.Label(root, text = '    ', bg = 'white')
    dummyText2.grid(row = 1, column = 0)


    #start talking to Arduino
    print "Start talking to Arduino"

    while(1):
        arduinoMessage = myGUI.readFromArduino()
        if arduinoMessage == 'T':
            myGUI.sendToArduino('T')
            nextByte = myGUI.readFromArduino()
            if nextByte == 'G':
                #do the "take picture" stuff
                pass
        elif arduinoMessage == 'C':
            myGUI.sendToArduino('C')
            nextByte = myGUI.readFromArduino()
            if nextByte == 'G':
                #do the "continue" stuff
                pass
        elif 'D' in arduinoMessage:
            threshold1 = arduinoMessage.split(',')[1]
            threshold2 = arduinoMessage.split(',')[2]
            threshold3 = arduinoMessage.split(',')[3]
        else:
            pass



    root.mainloop()



if __name__ == '__main__':
    main()
