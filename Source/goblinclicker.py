#from PIL import Image, ImageFilter, ImageDraw
import os
import time
import numpy as np
import cv2
import random
import pyautogui
import tkinter

#placeholder
centre = (0, 0)
#constants
resize_factor = 0.5
threshold = 20
delay_screengrab = 0.05
delay_sequence = 35
#box_size_threshold = 50
delay_combat = 7

def screenshot():
    #osi.system("import -window root ../ImageDump/temp1.png") 
    image1 = pyautogui.screenshot()
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    return image1

def screengrab():
    #time.sleep(1)
    #os.system("import -window root ../ImageDump/temp1.png")
    image1 = pyautogui.screenshot()
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    #time.sleep(delay_screengrab)
    image2 = pyautogui.screenshot()
    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
    return image1, image2
    #os.system("import -window root ../ImageDump/temp2.png")

def grayscale(tup):
    return int(tup[0]*0.3+tup[1]*0.6+tup[2]*0.1)

def resolution():
 
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    print(width, height)
    return width, height

def boundingbox2(img):
    im = img #lazy fix, TODO fix properly
    #im = np.array(img)
    #imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(im,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append((x, y, x+w, y+h))

    return boxes

def boundingbox(img):
    #img = Image.open(sys.argv[1]).convert('L')
    #img = img.convert('L')
    #im = np.array(img) 
    im = img
    colors = set(np.unique(im))
    colors.remove(0)
    boxes = []
    for color in colors:
        py, px = np.where(im == color)
        boxes.append((px.min(), py.min(), px.max(), py.max()))
        print((px.min(), py.min(), px.max(), py.max()))
    return boxes
def turn_centre_black(im):
    return

def filter_small_boxes(boxes):
    new_boxes = []
    for tup in boxes:
        xdiff = tup[2] - tup[0]
        ydiff = tup[3] - tup[1]

        if xdiff*ydiff > box_size_threshold:
            new_boxes.append(tup)
    return new_boxes

def scale_coordinate(tup): #Eventually get the inverse of resize_factor
    #Adjust for resizing of image, to find actual coordinate on screen
    #multiply centre coordinate with 2?
    return (tup[0]*2, tup[1]*2)

def find_centre(box):
    x1 = box[0]
    y1 = box[1]
    x2 = box[2]
    y2 = box[3]

    xdiff = x2 - x1
    ydiff = y2 - y1
    
    cx = xdiff//2 + x1
    cy = ydiff//2 + y1
    
    return (cx, cy)
def in_combat(img):
    in_combat = False
    ratios = (635/1366, 340/768, 750/1366, 390/768) #TODO this should scale with resolution
    
    width, height = resolution()
    box = (int(ratios[0]*width), int(ratios[1]*height), int(ratios[2]*width), int(ratios[3]*height))

    subimage = img[box[1]:box[3], box[0]:box[2]]
    number_of_pixels = (box[2]-box[0])*(box[3]-box[1])
    prev_was_green = False
    prev_was_red = False
    
    #cv2.imshow("combat", subimage) 
    #cv2.waitKey(0)
    
    for row in range(len(subimage)):
        for col in range(len(subimage[row])):
            is_green = subimage[row][col][1] == 255 and subimage[row][col][0]==0 and subimage[row][col][2]==0 

            if is_green:
                if prev_was_green:

                    print("In combat")
                    return True
                else:
                    prev_was_green = True

            
            
            """ 
            if prev_was_red and subimage[row][col][2] == 255:
                print("In combat") 
                return True
            else:
                prev_was_red = True
            """
    #thresh = number_of_pixels*50
    #green_thresh = number_of_pixels*130

    #if sum_green>thresh or sum_red>thresh:
    #    in_combat = True
    #print("Thresh is ", thresh)
    #print("Greensum is ", sum_green)
    #print("Redsum is ", sum_red)


    return False
    #pixel = img[82][121]
    
    #print(pixel)

def click_centre(box): #Box is a 4 tuple wich describes a square, result is clicking centre
    #box is a tuple with four elements, x1, y1, x2, y2
    #find centre pixel and click this boyo
    #difference between x1, x2 and y1, y2
    coord = find_centre(box)
    os.system("xdotool mousemove "+str(coord[0])+" "+str(coord[1]))
    os.system("xdotool click 1")
    return

def click_point(coord): #Coord should be a tuple, (x,y), moves mouse and clicks at xy
    os.system("xdotool mousemove "+str(coord[0])+" "+str(coord[1])+";xdotool click 1")
    #os.system("xdotool click 1")
    return
def click_random(coord):
    #click randomly within a 10x10 pixel window of by the coordinate
    offx = random.randint(-7, 7)
    offy = random.randint(-5, 5)
    os.system("xdotool mousemove "+str(coord[0]+offx)+" "+str(coord[1]+offy))
    time.sleep(0.1)
    os.system("xdotool click 1")

    return
def find_closest_box(boxes, centre):
    centres = []
    minimum_distance = 100000
    minimum_point = (0, 0)

    for tup in boxes:
        
        point = find_centre(tup)
        x_distance = point[0]-centre[0]
        y_distance = point[1]-centre[1]
        
        dist = ((x_distance**2)+(y_distance**2))**(1/2)
        if dist<minimum_distance:
            minimum_distance = dist
            minimum_point = point
            #print("Minimum so far ", point, "Distance is ", dist)
    return minimum_point
def find_largest_box(boxes):
    maximum_size = 0
    maximum_point = (0, 0)

    for tup in boxes:
        xdiff = tup[2] - tup[0]
        ydiff = tup[3] - tup[1]
        size = xdiff*ydiff
        if size>maximum_size:
            maximum_size = size
            maximum_point = find_centre(tup)
    return maximum_point

def draw_boxes(image, boxes):

    #draw = ImageDraw.Draw(image)
    #for tup in boxes:
    #    draw.line((tup[0], tup[1], tup[2], tup[3]), fill=128)#, width=3)
    #    draw.line((tup[0], tup[3], tup[2], tup[1]), fill=128)#, width=3)
    for tup in boxes:
        image = cv2.line(image,(tup[0],tup[1]),(tup[2],tup[3]),(255,0,0),1)
        image = cv2.line(image,(tup[0],tup[3]),(tup[2],tup[1]),(255,0,0),1)

    return image

#collect all steps for one iteration
def do_one_sequence():
    #time.sleep(2)
    im1, im2 = screengrab()

    
    #Do some resizing, to reduce comp load
    #im1 = im1[176:1084, 121:695]
    #im2 = im2[176:1084, 121:695]
 
    size = (int(im1.shape[1]*resize_factor), int(im1.shape[0]*resize_factor))
    
    im1 = cv2.resize(im1, size,  interpolation = cv2.INTER_AREA)
    im2 = cv2.resize(im2, size, interpolation = cv2.INTER_AREA)
    
    #Set the centre variable, where the middle point of image is
    #centre = (im1.shape[0]//2, im1.shape[1]//2)
    
    #blank black or white image
    #im3 = np.zeros((im1.shape[0], im1.shape[1],), np.uint8)


    #filtering, reduce noise, need to do this
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    im1 = cv2.GaussianBlur(im1,(5,5),cv2.BORDER_DEFAULT)
    im2 = cv2.GaussianBlur(im2,(5,5),cv2.BORDER_DEFAULT)
    #print(im3.shape)

    im3 = cv2.absdiff(im1, im2)

    ret, im3 = cv2.threshold(im3,threshold,255,cv2.THRESH_BINARY)

    boxes = boundingbox2(im3)
    #previous heuristic, find closest box
    #boxes = filter_small_boxes(boxes)
    #coords = find_closest_box(boxes, centre)
    coords = find_largest_box(boxes)
    if not coords == (0,0):
        #print("Centre is ",centre)
        #print("Working with prescaled coord ", coords)
        scaledc = scale_coordinate(coords)
        print("Clicking ", scaledc)
        #click_point(scaledc)
        click_random(scaledc)
    
    #Check if in combat
    time.sleep(delay_combat+random.randint(-2, 2))
    eval_combat = screenshot()
    while in_combat(eval_combat):
        #time.sleep(delay_sequence+random.randint(-5,5))
        time.sleep(5+random.randint(-2, 2))
        eval_combat = screenshot()





    

    #boundingbox2(im3)
    #for each box, draw bounding 
    #draw_boxes(im2, boxes)

    #outfile = "../ImageDump/temp3.png"


    #cv2.imshow("im1", im1)
    #cv2.imshow("im2", im2)
    #cv2.imshow("im3", im3)
    #cv2.waitKey(0)
    return

def sequence_forever():
    while True:
        do_one_sequence()

    
#Replace this with a main entrypoint
time.sleep(2)
#do_one_sequence()
#screenshot()
sequence_forever()
