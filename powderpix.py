from PIL import Image
A = Image.open("color.png")
B = Image.open("oki momen.png")
UIDELAY = 0.06
BLOCKDELAY = 0.5

start = (968, 556)

colormap = "pink magenta purple blue black gray lblue cyan white lime green sand lgray yellow orange brown red".split()
location = [(start[0]+36*i, start[1]) for i in range(9)] + [(start[0]+36*i, start[1]+36) for i in range(9)]
item = (1258, 674)

for i in B.getcolors():
    print(colormap[i[1]], i[0], sep="\t")


#0 pink
#1 magenta
#2 purple
#3 blue
#4 black
#5 gray
#6 lblue
#7 cyan
#8 white
#9 lime
#10 green
#11 sand
#12 lgray
#13 yellow
#14 orange
#15 brown
#16 red

import mouse
import keyboard
import time
import win32api

run = True
pos = 0
print("pos", 0)

def clickloc(pos):
    win32api.SetCursorPos(pos)
    time.sleep(UIDELAY)
    mouse.click()
    time.sleep(UIDELAY)

while run:
    press = keyboard.read_event()
    if press.name == "\\" and press.event_type == "down":
        run = False
    elif press.name == "[" and press.event_type == "down":
        pos -= 1
        print("pos", pos)
    elif press.name == "]" and press.event_type == "down":
        pos += 1
        print("pos", pos)
    elif press.name == "'" and press.event_type == "down":
        pixel = [B.getpixel((pos,B.size[1]-1-i)) for i in range(B.size[1])]
        before = None
        for i in pixel:
            if keyboard.is_pressed(";"):
                break
            if before != i:
                keyboard.press_and_release("e")
                keyboard.press('shift')
                time.sleep(UIDELAY)
                if before != None:
                    clickloc(item)
                clickloc(location[i])
                keyboard.release('shift')
                keyboard.press_and_release("e")
                time.sleep(UIDELAY)
            mouse.click("right")
            time.sleep(BLOCKDELAY)
            before = i
        keyboard.press_and_release("e")
        time.sleep(UIDELAY)
        clickloc(item)
        clickloc(location[before])
        keyboard.press_and_release("e")
        time.sleep(UIDELAY)
        pos += 1
        print("pos", pos)
