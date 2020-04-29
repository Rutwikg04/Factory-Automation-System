import pathlib
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2
import PIL
from PIL import Image
import image_slicer
from matplotlib import pyplot as plt

class imageToGraph():
    Tk().withdraw()
    print("Select file")
    src = askopenfilename()
    print(src)
    pathlib.Path('Factory').mkdir(parents=True, exist_ok=True)
    dst = "Factory/factory-map.png"
    image_file = cv2.imread(src)
    blur = cv2.GaussianBlur(image_file,(5,5),0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(dst,gray)

    image = cv2.imread(dst)
    y,x,z=image.shape
    #if x>y: a=x//1800  x//a
    image = cv2.resize(image,(x//50,y//50))
    cv2.imwrite("Factory/factory-map1.png",image)

    im=Image.open("Factory/factory-map1.png")
    pix=im.load()
    w=im.size[0]
    h=im.size[1]
    graph=[]
    fh=open("map","w")
    for i in range(h):
        string=""
        for j in range(w):
            if pix[j,i]==(0,0,0):
                string+="X"
            else:
                string+=" "
        string+="|"
        fh.write(string)
        graph.append(string)
    fh.close()
