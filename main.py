from grabscreen import grab_screen
import cv2
import numpy as np
import pyautogui
import win32gui
import utils
import math
import time
from pynput.keyboard import Key, Controller as KeyboardController
# TODO pick up modify for full inventory
# TODO solve cannot pick up when stack in an object
# TODO if out of range more than 5 times then run to towards closest enemy 

#  

# inital window size 0, 40, 1020,720
WINDOW = (0, 40, 810, 647)

HERO = (896,643)
MAP = (704, 522, 784, 602)
# MAP = (856, 603, 936, 683)


keyboard = KeyboardController()
 
# tracking many

# relative positioning()

# action class(name, button )

# window-capture class(color, cordinates, )

# diffrent landscape will have diffrent distance on the map, hence a better measure should be in place

# check the color of image
def get_color_at():
    mouse_position = pyautogui.position()
    grab_position = (mouse_position.x, mouse_position.y, mouse_position.x, mouse_position.y)
    grab = grab_screen(region=(grab_position))
    print(f'{list(grab)} color at {mouse_position}' )
    

# check for color in certain region
""" 
    lower_tresh: array of color,
    higher_tresh: arry of color,
    coordinates: array of [x, y]
"""
def color_definer(lower_tresh = [97, 107,  32],higher_tresh = [130, 157,  72], coordinates = None):
    cord = (coordinates[0], coordinates[1], coordinates[0], coordinates[1])
    map1 = grab_screen(cord)
    # the tresholds
    lower_treshold = np.array(lower_tresh)
    upper_treshold = np.array(higher_tresh)

    mask = cv2.inRange(map1, lower_treshold, upper_treshold)

    # res shows the diffrence in pixels from captured pic and set pic
    # if pictures are same returns treshold amount in array form
    # if picture is diffrent from treshold returns [0,0,0]
    res = cv2.bitwise_and(map1, map1, mask=mask)
    # indic checks where res is not [0]
    # or where color is similar
    indic = np.where(res > [10])
    indic = np.transpose(indic)
    # if res is bigger than [0] than indic becomes array of [0,1,0,1]
    # returns True if color is the same otherwise returns false
    if np.sum(np.nonzero(indic)) > 0 :
        # print('found monster')
        return True 
    else:
        return False



# find the mosnter

    

# problem with closest monster being too far
def attacking():
    buttons = utils.Custom_Button()
    buttons.attack_pattern()

def hunting():
    keyboard.press('d')
    monster = Monster()
    hero = Hero()
    buttons = utils.Custom_Button()
    hero.update_health()
    print(f"heros mana is {hero.health}")
    if hero.health <= 50:
        print('heal')
        hero.heal()
        return
    hero.update_mana()
    print(f"heros mana is {hero.mana}")
    if hero.mana <= 25:
        print('regening mana')
        hero.regen_mana()
        return
    time.sleep(0.15)
    hero.update_alive()
    distance = utils.find_closest()
    
    print(distance)
    keyboard.release('d')
    buttons.TAB()
    time.sleep(0.15)
    monster.update_found()
    print(monster.found)
    # if monster found 
    if monster.found:
        # check if it close for shot 
        time.sleep(0.3)
        in_range = utils.monster_in_range()
        print('checking in range')
        if in_range:
            print('starting attack')
            time.sleep(0.3)
            
            while True:
                monster.update_alive()
                if monster.alive == False:
                    break
                attacking()
               
                monster.update_damaged()
                print(f"mosnter is damaged: {monster.damaged}")
                if monster.damaged == False:
                    return 
            print('monster killed')
            time.sleep(0.3)
            # monster.pick_up()
            time.sleep(0.3)
            
            
            # Check health if low heal if heal on coldown sit until hp is 75 
            # 

        else:
            return
    else:
        return
        

class Monster():
    def __init__(self, *args, **kwargs):
        self.damaged = False
        self.alive = True
        self.found = False
        self.buttons = utils.Custom_Button()
        self.distance = 100

    def update_found(self):
        if color_definer([100, 80,  45],[110,  100,  100], coordinates=[332,65]) == True:
            self.found = True
            return
        else:
            self.found = False
            return

    def update_damaged(self):
        if color_definer([80,  5, 51], [100,  5, 51],coordinates=[437,66]):
            self.damaged = True
            return
        else:
            self.damaged = False
            return

    def update_alive(self):
        if utils.check_color(position=[339,66], color=[90,  5, 50]) == True:
            print('dead')
            self.alive = False
            return
        else:
            print('alive')
            self.alive = True
            return

    def pick_up(self):
        self.buttons.attack_buttons(6,1)
        
        while True:
            self.update_found()
            if self.found == False:
                break
                  
        

class Hero():
    def __init__(self, *args, **kwargs):
        self.health = 100 # [217  59  52]
        self.mana = 100
        self.alive = True
        self.closest = None
        self.buttons = utils.Custom_Button()
    
    def update_health(self):
        if color_definer([  1, 213, 205],[  1, 213, 205],coordinates = [207, 601]) == True:
            
            self.health = 100
            
        if color_definer([110, 123,  56],[110, 123,  56], coordinates=[181,602] ) == True:
            self.health = 75
             
        if color_definer([109, 127,  56],[109, 127,  56],coordinates=[161,602]) == True:
            self.health = 50    
             
        if color_definer([110, 123,  56], [110, 123,  56],coordinates=[126,601]) == True:
            self.health = 25
             
        
        
    def update_mana(self):
        if color_definer(coordinates = [174,612]) == True:
            self.mana = 75
             
        if color_definer(coordinates = [151,612]) == True:
            self.mana = 50
             
        if color_definer(coordinates = [125,612]) == True:
            self.mana = 25
             
        

    def update_alive(self):
        if color_definer( coordinates = [99, 602]) == True:
            self.alive = False
            return 
        
        return 
    def heal(self):
        # check for potion here
        if self.buttons.heal_cooldown() == True:
            # then sit
            self.buttons.attack_buttons(10,1)
        else:
            # heal 
            self.buttons.attack_buttons(1,3)
            time.sleep(4)
        
        return

    def regen_mana(self):
        if self.buttons.mana_cooldown() == True:
            # then sit
            self.buttons.attack_buttons(10,1)
        else:
            # heal 
            self.buttons.attack_buttons(2,3)
            time.sleep(4)
        
        return



def main():
    handle = win32gui.FindWindow(None, "AION Client")
    win32gui.SetForegroundWindow(handle)
    
    time.sleep(0.5)
    win32gui.MoveWindow(handle, -7, 0,810,647, False )
    # keyboard.press('d ')
    win32gui.SetForegroundWindow(handle)
    
    while True:
        # print('looping')
        hunting()
        # cv2.imshow('hi',  grab_screen(MAP))
        # print(pyautogui.position())
        # buttons = utils.Custom_Button()
        # print(buttons.mana_cooldown())
        # buttons.all_reload_checker()
        # for i in range(14):
        #     if i == 0:
        #         continue
        #     buttons.attack_buttons(i,1)
        #     buttons.attack_buttons(i,2)
        #     buttons.attack_buttons(i,3)
        # get_color_at()
        # print()
        # print(f'Monster Found: {monster.found}, Monster Damaged: {monster.damaged}, Monster Alive: {monster.alive}')
        
    
        # monster_dist = monster_distance()
        

        
    if cv2.waitKey(33) == ord('a') & 0xFF:
        return False

main()

# Point(x=335, y=696)