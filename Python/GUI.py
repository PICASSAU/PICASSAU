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


class Example(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.initPic()

    def initPic(self):

        imageName = "../imageFiltering/webcam2.png"

        self.xmax = 506
        self.ymax = 379
        self.ymax = int(self.ymax * 0.9)
        self.cropConstant = (20.0/26.0)
        self.croppedX = int(self.ymax*self.cropConstant)
        box = (0, 0, self.croppedX, self.ymax)


        self.parent.title("Label")

        self.img = Image.open(imageName)
        self.imgCropped = self.img.crop(box)
        self.filteredImage = ImageTk.PhotoImage(self.imgCropped)
        labelImage = Tk.Label(image=self.filteredImage, background='blue')

        labelImage.image = self.filteredImage
        labelImage.grid(row = 0, column = 0, rowspan= 5)


    def setGeometry(self, root):

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='blue')


def main():

    root = Tk.Tk()
    ex = Example(root)
    text1 = Tk.Label(root, text="          Take Picture ", font=("Helvetica", 20, "bold"), fg='orange', bg = 'blue')
    text1.grid(row = 0, column = 2)

    text2 = Tk.Label(root, text="          Continue ", font=("Helvetica", 20, "bold"), fg='orange', bg = 'blue')
    text2.grid(row = 4, column = 2)
    ex.setGeometry(root)

    root.mainloop()



if __name__ == '__main__':
    main()
