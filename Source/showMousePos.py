# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller
from PIL import ImageGrab
import random
import numpy as np
import cv2

from pynput.keyboard import Listener, KeyCode

delay = 0.5
start_stop_key = KeyCode(char='z')
stop_key = KeyCode(char='x')

# threading.Thread is used 
# to control clicks
class PrintMousePos(threading.Thread):
    # delay and button is passed in class 
    # to check execution of auto-clicker
    def __init__(self, delay):
        super(PrintMousePos, self).__init__()
        self.delay = delay
        self.running = False
        self.program_running = True

    def start_printing(self):
        print("Starting")
        self.running = True

    def stop_printing(self):
        print("Stopping")
        self.running = False

    def exit(self):
        self.stop_printing()
        self.program_running = False


    # method to check and run loop until 
    # it is true another loop will check 
    # if it is set to true or not, 
    # for mouse click it set to button 
    # and delay.
    def run(self):
        while self.program_running:
            while self.running:
                print(mouse.position)
                time.sleep(self.delay)
            time.sleep(0.1)


# instance of mouse controller is created
mouse = Controller()
print_thread = PrintMousePos(delay)
print_thread.start()


# on_press method takes 
# key as argument
def on_press(key):
    
# start_stop_key will stop clicking 
# if running flag is set to true
    if key == start_stop_key:
        if print_thread.running:
            print_thread.stop_printing()
        else:
            print_thread.start_printing()

    # here exit method is called and when 
    # key is pressed it terminates auto clicker
    elif key == stop_key:
        print_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()