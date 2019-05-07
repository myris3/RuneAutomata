import os
import time


#Do a hand crafted series of clicks
#Remember to zoom all the way out, using RuneLite
#Also TODO: make coordinates general, scale to resolution
#     TODO: Make a login script, logging in is tedious
#Tuned for mining iron 
delay_click_iron = 4
delay_click_coal = 13
dx = 40
dy = 35
base = (1693, 775)
small_delay = 0.13
walk_delay = 2.5
# TODO: make clicker functions go through a list of coords, then click each one
# Make functions more general

#Custom coords, relative to character
coord_top = (940, 526)
coord_right = (970, 558)
coord_left = (910, 554)
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
def add_tuple(tuple1, tuple2):
    return (tuple1[0]+tuple2[0], tuple1[1]+tuple2[1])

def wait(delay):
    time.sleep(delay)

def mine_guild_iron(delay_click, back_to_station):
    if(back_to_station): 
        #Walk to iron ores
            #Coords: (1281, 586)
        click((1281, 586))
        wait(10)
    else:
        count = 0
        while count<28:
            count = count + 2
            click(coord_top)
            wait(delay_click)
            click(coord_bottom)
            wait(delay_click)

        #Walk to ladder
        #Ladder coords: (524, 502)
        
        click((524, 502))
        wait(12)

def mine_guild_coal(delay_click, back_to_station):
    if(back_to_station):
        click((1486,717))
        wait(15)
    else:
        
        count = 0
        while count<28:
            count = count + 4
            click(coord_top)
            wait(delay_click)
            click(coord_bottom)
            wait(delay_click)
            
            #temp = (coord_left[0]-40, coord_left)
            click(add_tuple(coord_left,(-35, 0)))
            wait(walk_delay)
            #click(coord_left)
            wait(delay_click)
           
            #temp = (coord_right[0]+80, coord_right[1])
            click(add_tuple(coord_right, (70, 0)))
            wait(walk_delay)
            #click(coord_right)
            wait(walk_delay)
            #click(coord_right)
            wait(walk_delay)
            
            #temp = (coord_left[0]-40, coord_left[1])
            click(coord_bottom)
            wait(delay_click)
            click(add_tuple(coord_left,(-35, 0)))
            wait(walk_delay)
            #click(coord_left)
            wait(walk_delay)

        #Walk to ladder
        #Ladder coords: (406, 382)

        click((406, 382))
        wait(15)

def mine_guild():
    while True:
        #Start mining top and bottom deposits
            #Top coords: (946, 526)
            #Bottom coords: (943, 586)
        mine_guild_coal(delay_click_coal, False)
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
        wait(1)
        #Walk back to guild entrance
            #Coords: (1812, 200)
        click((1812, 200))
        wait(32)
        #Click ladder
            #Coords: (867, 518)
        click((867, 514))
        wait(6)
        mine_guild_coal(delay_click_coal, True)
        #back to start


time.sleep(2)
#empty_inventory()
#mine_inventory()
mine_guild()

