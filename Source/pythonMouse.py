import uinput
import time
max_x = 20
max_y = 20
device = uinput.Device([
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        #uinput.REL_X,
        #uinput.REL_Y])#,
        uinput.ABS_X+(0, max_x, 0, 0),
        uinput.ABS_Y+(0, max_y, 0, 0)])

#print(uinput.ABS_X)
for i in range(min(max_y, max_x)):
    device.emit(uinput.ABS_X, i)
    device.emit(uinput.ABS_Y, i)
    time.sleep(0.1)
    #print(uinput.REL_X)
    #print(uinput.REL_Y)
