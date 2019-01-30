import subprocess
import time
import random
import os
#import numpy as np
#import imageio
#import matplotlib.pyplot as plt
from PIL import Image
"""
cmd = ['xrandr']
cmd2 = ['grep', '*']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
p.stdout.close()
 
resolution_string, junk = p2.communicate()
resolution = resolution_string.split()[0]
#width, height = resolution.split('x')

"""
"""
while True:
    #cmd = ['xdotool', 'click', '1']
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    
    os.system("xdotool click 1")
    time.sleep(random.randint(5, 7))    

"""

im = Image.open("temp.png")
im.show()


#img = imageio.imread('~/Projects/RuneAutomata/temp.png')
#plt.subplot(1, 2, 1)
#plt.imshow

#plt.subplot(1,2,2)

#plt.imshow(np.uint8(img_tinted))
#plt.show()
