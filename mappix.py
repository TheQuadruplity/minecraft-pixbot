from PIL import Image
import mouse
import keyboard
import time
import win32api

# Pick Image
B = Image.open("suya2.png")

# Constants
UIDELAY = 0.06
BLOCKDELAY = 0.5
INVENTORY_LOC = 556
COLUMN_LOC = 814
HOTBAR_LOC = 672
SHULKER_LOC = 556-128

# Preprocessed constants
colormap = "pink magenta purple blue black gray lblue cyan white lime green sand lgray yellow orange brown red".split()
inventory = [(COLUMN_LOC+36*i, INVENTORY_LOC) for i in range(9)] + [(COLUMN_LOC+36*i, INVENTORY_LOC+36) for i in range(9)]
hotbar = [(COLUMN_LOC+36*i, HOTBAR_LOC) for i in range(9)]
shulker = [(COLUMN_LOC+36*i, SHULKER_LOC) for i in range(9)] + [(COLUMN_LOC+36*i, SHULKER_LOC+36) for i in range(9)]
cache = hotbar[1:7]

for i in B.getcolors():
    print(colormap[i[1]], i[0], sep="\t")

# hotbar:
# elytra/armor, rocket, c1, c2, c3, c4, c5, netherrack, pickaxe
# c initially placeholder
# item data: [count, cacheloc, chance]
# cache rank: [0, scrambled 1-5] (more low index, more unimportant)
# cache item: [none or item index]

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
#11 sand (birch pressure plate)
#12 lgray
#13 yellow
#14 orange
#15 brown
#16 red

run = True
pos = 0
print("pos", 0)

def clickloc(pos):
    win32api.SetCursorPos(pos)
    time.sleep(UIDELAY)
    mouse.click()
    time.sleep(UIDELAY)

def presskey(key):
    keyboard.press_and_release(key)
    time.sleep(UIDELAY)

def click(button = "left"):
    mouse.click(button)
    time.sleep(UIDELAY)

while run:
    press = keyboard.read_event()
    if press.name == "\\" and press.event_type == "down": # exit program
        run = False
    elif press.name == "[" and press.event_type == "down": # move position back
        pos -= 1
        print("pos", pos)
    elif press.name == "]" and press.event_type == "down": # move position up
        pos += 1
        print("pos", pos)
    elif press.name == "'" and press.event_type == "down": # start row/col
        # build pixel data
        pixel = [B.getpixel((i,pos)) for i in range(B.size[0])] 
        if pos%2:
            pixel.reverse()
        
        # build item/cache data
        item_data = [[64, 0, 0] for i in range(17)] # [count, cacheloc, chance]
        cache_item = [None]*6
        cache_rank = list(range(6))
        before = None

        for i in pixel:
            if keyboard.is_pressed(";"): # exit row/col (kill switch)
                break
            if before != None and item_data[before][0] == 0: # refill
                # switch netherrack to shulker box
                presskey("e")
                clickloc(hotbar[7])
                clickloc((COLUMN_LOC+36*item_data[before][2], INVENTORY_LOC+72))
                clickloc(hotbar[7])
                presskey("e")
                # open shulker box
                presskey("8")
                click('right') # maybe block delay
                click('right') # maybe block delay
                time.sleep(0.5)
                # refill item to cache
                clickloc(shulker[before])
                clickloc(cache[item_data[before][1]])
                # return netherrack
                clickloc((COLUMN_LOC+36*item_data[before][2], INVENTORY_LOC+72))
                clickloc(hotbar[7])
                presskey("e")
                # break shulker box
                presskey("9")
                mouse.hold()
                time.sleep(0.4)
                mouse.release()
                # update data
                item_data[before][0] = 64
                item_data[before][2] += 1
            if not item_data[i][1]: # item not in cache
                # switch item to cache
                presskey("e")
                clickloc(inventory[i])
                clickloc(cache[cache_rank[1]]) # (picked old item or placeholder)
                if cache_item[cache_rank[1]] != None: # remove low rank cache (old item)
                    clickloc(inventory[cache_item[cache_rank[1]]])
                    item_data[cache_item[cache_rank[1]]][1] = None
                clickloc(inventory[i]) # (item in hand: placeholder)
                # update data
                item_data[i][1] = cache_rank[1]
                cache_item[cache_rank[1]] = i
                presskey("e")
            # place netherrack
            presskey("8")
            click("right")
            # place carpet in cache
            presskey(str(item_data[i][1]+2))
            click("right")
            # move forward
            keyboard.press('w')
            time.sleep(0.3)
            keyboard.release('w')
            # break netherrack
            presskey("9")
            click()
            # update data
            cache_rank.remove(item_data[i][1])
            cache_rank.append(item_data[i][1])
            item_data[i][0] -= 1
            before = i
        # finish row/col
        presskey("e")
        for i in cache_item:
            if i == None: continue
            clickloc(inventory[i])
            clickloc(cache[item_data[i][1]])
            clickloc(inventory[i])
        presskey("e")
        pos += 1
        print("pos", pos)
