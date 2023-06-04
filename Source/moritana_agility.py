
# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller
from PIL import ImageGrab, Image
import random
import numpy as np
#import cv2

# pynput.keyboard is used to watch events of
# keyboard for start and stop of auto-clicker
from pynput.keyboard import Listener, KeyCode

# four variables are created to
# control the auto-clicker
delay = 7
start_stop_key = KeyCode(char='z')
stop_key = KeyCode(char='x')
button = Button.left
green = (0, 255, 0)
red = (255, 0, 0)
mark_color = (166, 122, 6)

# zoom level 176, click compass to align screen somewhat
# Agilitycourse exit x,y sequence
moritania_agility_exits = [(819, 309),
                           (930, 384),
                           (667, 529),
                           (462, 761),
                           (848, 926),
                           (1063, 654),
                           (1681, 533),
                           (945, 376)]

delay_sequence = [7, 5.5, 5.5, 5.5, 5.5, 6.2, 7, 5]

agility_exits_bounding_boxes = [
    ((800, 280), (820, 300)),
    ((900, 300), (1000, 500)),
    ((600, 400), (800, 600)),
    ((350, 550), (750, 850)),
    ((730, 700), (930, 1000)),
    ((850, 300), (1200, 750)),
    ((1500, 400), (1900, 750)),
    ((900, 300), (1000, 500))
]
mark_bounding_boxes = [((898, 433), (1088, 518)),
                       ((740, 477), (950, 559)),
                       ((587, 564), (935, 827)),
                       ((715, 571), (982, 828)),
                       ((937, 559), (1120, 614)),
                       ((996, 478), (1570, 976)),
                       ((905, 414), (1171, 525)),
                       ((0, 0), (1, 1))] #Dummy element to make the run complete


#Find anything that is red or green on the screen
whole_screen_bounding_box = ((79, 46), (1575, 906))

#When falling of the track at a certain point, the start of the course is not visible
#Hopefully clicking this coordinate will make the entrance visible
center_village_edge_case = (1743, 779)

# click randomly within a 10x10 pixel window of by the coordinate
#TODO something fucked up here, investigate
def click_randomiser(coord):
    offx = random.randint(-7, 7)
    offy = random.randint(-5, 5)
    print(offx, offy, coord, (coord[0] + offx, coord[1] + offy))
    return (coord[0] + offx, coord[1] + offy)


def time_delay_randomiser(range=1):
    time_delay = 0
    if (range < 0):
        time_delay = 1 / random.randint(1, -range + 1)
    else:
        time_delay = 1 / random.randint(1, range + 1)
    #print("Delaying time for: ", time_delay, "seconds")
    return time_delay

def createBbox_from_coordinates(xymin_xymax):
    xymin, xymax = xymin_xymax
    xmin , ymin = xymin
    xmax, ymax = xymax
    return (xmin, ymin, xmax, ymax)

def convertFlatIndexToCoordinate(index, imageWidth):
    return ( index % imageWidth, index//(imageWidth))



# threading.Thread is used
# to control clicks
class MoritaniaClicker(threading.Thread):
    # delay and button is passed in class
    # to check execution of auto-clicker
    def __init__(self, delay, button):
        super(MoritaniaClicker, self).__init__()
        self.delay = delay
        self.button = button
        self.current_index = 0
        self.running = False
        self.program_running = True

    def set_current_index(self, index):
        print("Setting index:", index)
        self.current_index = index

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def moveAndClick(self, coordinates):
        mouse.move(coordinates[0] - mouse.position[0] , coordinates[1] - mouse.position[1] )
        time.sleep(time_delay_randomiser(20))
        mouse.click(self.button)
        time.sleep(0.1)
        mouse.click(self.button)

    def doMarkCheck(self):
        #Check for marks after movement
        print("Starting mark check: ", self.current_index)
        bbox = createBbox_from_coordinates(mark_bounding_boxes[self.current_index])
        screen_grab = ImageGrab.grab(bbox)
        screen_grab.save("./ImageDump/markImageEmpty_" + str(self.current_index) +".png")
        img = list(screen_grab.getdata())
        if self.findBboxAndClick(img, screen_grab.size[0], mark_bounding_boxes[self.current_index][0], mark_color):
                screen_grab.save("./ImageDump/markImageFound_" + str(self.current_index) +".png")
                time.sleep(self.delay/2)
                return
        print("Failed to find mark")
    
    def doExitCheck(self):
        #Check for marks after movement
        print("Starting exit check: ", self.current_index)
        bbox = createBbox_from_coordinates(agility_exits_bounding_boxes[self.current_index])
        screen_grab = ImageGrab.grab(bbox)
        screen_grab.save("./ImageDump/exitImage_" + str(self.current_index) +".png")
        imgFail = list(screen_grab.getdata())
        #Check for green bbox
        if self.findBboxAndClick(imgFail, screen_grab.size[0], agility_exits_bounding_boxes[self.current_index][0], green):
            screen_grab.save("./ImageDump/exitImageGreen_" + str(self.current_index) +".png")
            return
        #Check for red bbox
        if self.findBboxAndClick(imgFail, screen_grab.size[0], agility_exits_bounding_boxes[self.current_index][0], red):
            screen_grab.save("./ImageDump/exitImageRed_" + str(self.current_index) +".png")
            return
        print("Failed to find exit, probably fallen of the track")
        self.doFailureCorrection()
        return
    
    def findBboxAndClick(self, flatImage, imageWidth, offsetCoordinate, color):
        if flatImage.count(color) > 0:
                index = flatImage.index(color)
                x_y = convertFlatIndexToCoordinate(index, imageWidth)
                print("Found pixel sans offset: ", x_y)
                print("Offset is: ", offsetCoordinate)
                x_y_offset = (x_y[0] + offsetCoordinate[0] + 3, x_y[1] + offsetCoordinate[1] + 3)
                print("Found pixel: ", x_y_offset)
                #flatImage[index] = (255, 255, 255)
                #flatImage[index+1] = (255, 255, 255)
                #flatImage[index-1] = (255, 255, 255)
                #flatImage[index-imageWidth] = (255, 255, 255)
                #flatImage[index+imageWidth] = (255, 255, 255)

                #x = np.asarray(flatImage, dtype=np.uint8)
                #Image.fromarray(x).save("./ImageDump/clicked_spot_" + str(self.current_index) +".png")
                self.moveAndClick(x_y_offset)
                return True
        return False
    
    def doFailureCorrection(self):
        print("Starting error handling")
        while self.running:
            bbox_failed = createBbox_from_coordinates(whole_screen_bounding_box)
            screen_grab = ImageGrab.grab(bbox_failed)
            screen_grab.save("./ImageDump/failureImage_" + str(self.current_index) +".png")
            #Runelite agility plugin setting green (0, 255, 0) or red (255, 0, 0) bounding boxes on clickboxes for exits
            #Makes sense, can be changed, but is a nice visual indicator for when marks are dropped
            imgFail = list(screen_grab.getdata())
            
            #Check for green bbox
            if self.findBboxAndClick(imgFail, screen_grab.size[0], whole_screen_bounding_box[0], green):
                self.set_current_index(0)
                return
            #Check for red bbox
            if self.findBboxAndClick(imgFail, screen_grab.size[0], whole_screen_bounding_box[0], red):
                self.set_current_index(0)
                return
            #If got here, no exit is currently visible, try to click edge case coordinate
            print("Could not find an exit, trying to walk a bit to the left to find an entrance")
            self.moveAndClick((center_village_edge_case[0], center_village_edge_case[1]))
            time.sleep(self.delay*1.5)

    def doIteration(self):
        print("Starting iteration: ", self.current_index)
        time.sleep(time_delay_randomiser(20))
        self.doExitCheck()
        print("Sleeping for: ", delay_sequence[self.current_index], " seconds")
        time.sleep(delay_sequence[self.current_index])
        self.doMarkCheck()




    # method to check and run loop until
    # it is true another loop will check
    # if it is set to true or not,
    # for mouse click it set to button
    # and delay.

    def run(self):
        while self.program_running:
            while self.running:
                self.doIteration()
                self.set_current_index((self.current_index + 1) % (len(moritania_agility_exits)))
            time.sleep(0.1)


# instance of mouse controller is created
mouse = Controller()
click_thread = MoritaniaClicker(delay, button)
click_thread.start()


# on_press method takes
# key as argument
def on_press(key):
    # start_stop_key will stop clicking
    # if running flag is set to true
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
            print("Stopping")
        else:
            click_thread.start_clicking()
            print("Starting")
    elif key == KeyCode(char='0'):
        click_thread.set_current_index(0)
    elif key == KeyCode(char='1'):
        click_thread.set_current_index(1)
    elif key == KeyCode(char='2'):
        click_thread.set_current_index(2)
    elif key == KeyCode(char='3'):
        click_thread.set_current_index(3)
    elif key == KeyCode(char='4'):
        click_thread.set_current_index(4)
    elif key == KeyCode(char='5'):
        click_thread.set_current_index(5)
    elif key == KeyCode(char='6'):
        click_thread.set_current_index(6)
    elif key == KeyCode(char='7'):
        click_thread.set_current_index(7)    
    # here exit method is called and when
    # key is pressed it terminates auto clicker
    elif key == stop_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
