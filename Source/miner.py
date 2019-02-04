import os
import time


#Do a hand crafted series of clicks
#Remember to zoom all the way in, using RuneLite
#Also TODO: make coordinates general, scale to resolution

#Tuned for mining tin/copper 
delay_click = 5
dx = 40
dy = 35
base = (1693, 775)
small_delay = 0.15

#clicks at some interval, calling check inventory at the end, emptying inventory at intervals
#purpose: just ttrain mining, not a care in the world for the resources we waste
def mine_inventory():
    #(946, 618)
    #(954, 895) zoomed in, rock should be in square directly south of the character
    coord = (954, 895)
    counter = 0
    while check_inventory():
        counter += 1
        os.system("xdotool mousemove "+str(coord[0])+" "+str(coord[1]))
        os.system("xdotool click 1")
        time.sleep(delay_click)
        if counter%28 == 0:
            empty_inventory()

def drop_item(coord):
    #time.sleep(small_delay)
    os.system("xdotool mousemove "+str(coord[0])+" "+str(coord[1])) 
    time.sleep(small_delay)
    os.system("xdotool click 3")
    time.sleep(small_delay)
    os.system("xdotool mousemove "+str(coord[0])+" "+str(coord[1]+dy))
    time.sleep(small_delay)
    os.system("xdotool click 1")
    #time.sleep(small_delay)
    return

#assumes inventory is homogeneous
def empty_inventory():
    #First item, first row (1693, 780)
    #Second item, same row, (1736, 783)
    #First item, next row, (1696, 819)
    #base = (1693, 780)
    #dx = 40
    #dy = 40
    for x in range(0, 4): #inventory is 4x7
        for y in range(0, 7):
           coord = (base[0]+dx*x, base[1]+dy*y)
           drop_item(coord)


#Placeholder, idea is to take a photo of last slot in inventory, check colors, if grey, still space, if not, full
def check_inventory():
    return True



time.sleep(2)
#empty_inventory()
mine_inventory()
