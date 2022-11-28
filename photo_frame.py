#!/usr/bin/env python3

import sys, getopt
import os, random
import tkinter
from PIL import Image, ImageTk
from signal import signal, SIGINT


class PhotoFrame:
    def __init__(self, imgpath):
        self.dir_path = imgpath

        self.root = tkinter.Tk()
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.focus_set()    
        self.root.bind_all("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.root.bind_all("<Control-c>", self.safe_quit)
        self.canvas = tkinter.Canvas(self.root,width=self.w,height=self.h)
        self.canvas.pack()
        self.canvas.configure(background='black')

        self.root.after(500, self.check_quit)

    def check_quit(self):
        """
        Needed to improve UI responsivity when hitting ctl^c
        """
        self.root.after(500, self.check_quit)

    def safe_quit(self):
        self.root.destroy()
        print("destroyed tk root")

    def get_random_img(self):
        """
        Randomly select an image filename within `dir_path` and all subdirs
        """
        # randomly get a file
        # /media/photos/409.jpeg

        img_files = []

        # see also
        # https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
        for path, subdirs, files in os.walk(self.dir_path):
            for name in files:
                img_files.append(os.path.join(path, name))

        self.img_fname = random.choice(img_files)

    def display_img(self):
        """
        display an image stored at img_fname, taking up the whole canvas
        """
        try:
            # open the image
            im = Image.open(self.img_fname)

            # display image
            # mostly thanks to
            # https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
            
            imgWidth, imgHeight = im.size
            if imgWidth > self.w or imgHeight > self.h:
                ratio = min(self.w/imgWidth, self.h/imgHeight)
                imgWidth = int(imgWidth*ratio)
                imgHeight = int(imgHeight*ratio)
                im = im.resize((imgWidth,imgHeight), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(im)
            imagesprite = self.canvas.create_image(self.w/2,self.h/2,image=self.image)

            return True
        except:
            return False

    def slideshow(self):
        """
        Run a slideshow of random images from the specified location
        """
        # get and display img
        self.get_random_img()
        print("Attempting to show: " + self.img_fname)
        if (self.display_img()):
            # TODO: buttons for "don't show" and "like"
            # wait for a random amount of time (2 to 5 minutes per image)
            delay_time = random.randrange(2*60, 5*60)*1000
        else:
            # if we didn't successfully display an image, delay should be 0
            print("not a good image: " + self.img_fname)
            delay_time = 1 # super short
        self.root.after(delay_time, self.slideshow)

    def run_show(self):
        self.slideshow()
        self.root.mainloop()

def show_usage(scriptname):
    print(scriptname + " -p path/to/imgs")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", ["imgpath="])
    except getopt.GetoptError:
        show_usage(sys.argv[0])
        sys.exit(2)

    imgpath = ""
    for opt, arg in opts:
        if opt in ("-p", "--imgpath"):
            imgpath = arg
        else:
            show_usage(sys.argv[0])
            sys.exit(2)

    if imgpath == "":
        show_usage(sys.argv[0])
        sys.exit(2)

    print("looking for images in: " + imgpath)

    pf = PhotoFrame(imgpath)
    pf.run_show()
