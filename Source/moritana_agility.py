
# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller
from PIL import ImageGrab
import random

# pynput.keyboard is used to watch events of 
# keyboard for start and stop of auto-clicker
from pynput.keyboard import Listener, KeyCode

# four variables are created to 
# control the auto-clicker
delay = 7
start_stop_key = KeyCode(char='z')
stop_key = KeyCode(char='x')
button = Button.left

# zoom level 176, click compass to align screen somewhat
#Agilitycourse x,y sequence
moritania_agility = [(819, 309), (930, 384), (667, 529), (462, 761), (848, 926), (1063, 654), (1681, 533), (945, 376)]

def click_randomiser(coord):
    #click randomly within a 10x10 pixel window of by the coordinate
    offx = random.randint(-7, 7)
    offy = random.randint(-5, 5) 
    print(offx, offy, coord, (coord[0] + offx, coord[1] + offy))
    return (coord[0] + offx, coord[1] + offy)
    
def time_delay_randomiser(range=1):
    if (range<0):
        return 1/random.randint(1, -range+1)
    return 1/random.randint(1, range+1)


# threading.Thread is used 
# to control clicks
class ClickMouse(threading.Thread):
    # delay and button is passed in class 
    # to check execution of auto-clicker
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False


    # method to check and run loop until 
    # it is true another loop will check 
    # if it is set to true or not, 
    # for mouse click it set to button 
    # and delay.
    def run(self):
        while self.program_running:
            current_index = 0
            while self.running:
                time.sleep(time_delay_randomiser(20))
                print("About to try: ", current_index)
                print(mouse.position)
                vector = (- mouse.position[0] + moritania_agility[current_index][0], - mouse.position[1] + moritania_agility[current_index][1]) 
                #vectorRandom1 = click_randomiser(vector)
                #vectorRandom2 = click_randomiser(vector)
                #print("Randoms: ", vectorRandom1, vectorRandom2)
                #mouse.move(vectorRandom1[0], vectorRandom1[1])
                #time.sleep(time_delay_randomiser(10))
                #mouse.move(vectorRandom2[0], vectorRandom2[1])
                mouse.move(vector[0], vector[1])
                time.sleep(time_delay_randomiser(10))
                print(mouse.position, current_index, moritania_agility[current_index])
                current_index = (current_index + 1) % (len(moritania_agility))
                mouse.click(self.button)
                time.sleep(0.1)
                mouse.click(self.button)
                
                time.sleep(self.delay)
            time.sleep(0.1)


# instance of mouse controller is created
mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


# on_press method takes 
# key as argument
def on_press(key):
    
# start_stop_key will stop clicking 
# if running flag is set to true
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()

    # here exit method is called and when 
    # key is pressed it terminates auto clicker
    elif key == stop_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()