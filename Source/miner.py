import os
import time


#Do a hand crafted series of clicks
#Remember to zoom all the way in, using RuneLite
#Also TODO: make coordinates general, scale to resolution

#Tuned for mining tin/copper 
delay_click = 4
dx = 40
dy = 35
base = (1693, 775)
small_delay = 0.13
# Idea: make clicker functions go through a list of coords, then click each one
# Make functions more general
coord_top = (946, 526)
coord_bottom = (943, 586)

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
        time.sleep(small_delay)
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

def click(coord):
    os.system("xdotool mousemove "+str(coord[0])+" "+str(coord[1]))
    time.sleep(small_delay)
    os.system("xdotool click 1")

def wait(delay):
    time.sleep(delay)

def mine_guild_inventory():
    count = 0
    while count<14:
        count = count + 1
        click(coord_top)
        wait(delay_click)
        click(coord_bottom)
        wait(delay_click)
def mine_guild_iron():
    while True:
        #Start mining top and bottom deposits
            #Top coords: (946, 526)
            #Bottom coords: (943, 586)
        mine_guild_inventory()
        #Walk to ladder
            #Ladder coords: (524, 502)
        click((524, 502))
        wait(12)
        #Walk to bank
            #Inside bank coords: (1774, 62)
        click((1774, 62))
        wait(31)
        #Deposit
            #Coords: (1007, 494)
            #then: (761, 562)
        click((1007, 494))
        wait(4)
        click((761, 562))
        #Walk back to guild entrance
            #Coords: (1812, 200)
        click((1812, 200))
        wait(31)
        #Click ladder
            #Coords: (867, 518)
        click((867, 518))
        wait(6)
        #Walk to iron ores
            #Coords: (1281, 586)
        click((1281, 586))
        wait(10)
        #back to start


time.sleep(2)
#empty_inventory()
#mine_inventory()
mine_guild_iron()

