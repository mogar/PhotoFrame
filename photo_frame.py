#!/usr/bin/env python3

import sys, getopt
import os, random
import tkinter
from PIL import Image, ImageTk

def get_random_img(dir_path):
    """
    Randomly select an image filename within `dir_path` and all subdirs
    """
    # randomly get a file
    # /media/photos/409.jpeg

    img_files = []

    # see also
    # https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            img_files.append(os.path.join(path, name))

    return random.choice(img_files)

def display_img(img_fname, canvas):
    """
    display an image stored at img_fname, taking up the whole canvas
    """
    try:
        # open the image
        im = Image.open(img_fname)

        # display image
        # mostly thanks to
        # https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
        

        w = canvas.cget("width")
        h = canvas.cget("height")
        imgWidth, imgHeight = im.size
        if imgWidth > w or imgHeight > h:
            ratio = min(w/imgWidth, h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            im = im.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(im)
        imagesprite = canvas.create_image(w/2,h/2,image=image)

        return True
    except:
        return False

def slideshow(path, canvas):
    """
    Run a slideshow of random images from the specified location
    """
    # get and display img
    imgname = get_random_img(path)
    if (display_img(imgname, canvas)):
        # TODO: buttons for "don't show" and "like"
        # wait for a random amount of time (2 to 5 minutes per image)
        delay_time = random.randrange(2*60, 5*60)*1000
    else:
        # if we didn't successfully display an image, delay should be 0
        print("not a good image: " + imgname)
        delay_time = 1 # super short
    canvas.after(delay_time, slideshow, path, canvas)

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

    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')

    slideshow(imgpath, canvas)

    root.mainloop()
