from grabscreen import grab_screen
import cv2
import numpy as np
import pyautogui
import win32gui
import utils
import math
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button,Controller as MouseController
import time
MAP = (704, 522, 784, 602)
# TODO if inventory is full pick doesn't work
# TODO optimizing attacking
    # each button have individual cooldown
    # if button on cooldown skip button
    # 
keyboard = KeyboardController()
mouse = MouseController()


def white():
    map1 = grab_screen(MAP)
    lower_white= np.array([0,0,240])
    upper_white = np.array([0,0,255])
    mask = cv2.inRange(map1, lower_white, upper_white)
    res = cv2.bitwise_and(map1, map1, mask=mask)
    
    
    
    coord=cv2.findNonZero(mask)
    if coord is None:
        return np.empty((60, 1, 2))
        
    return coord
        


def red():
    map1 = grab_screen(MAP)
    lower_red = np.array([0,150,200])
    upper_red = np.array([5,255,255])
    mask = cv2.inRange(map1, lower_red, upper_red)
    res = cv2.bitwise_and(map1, map1, mask=mask)
    
    coord=cv2.findNonZero(mask)
    if coord is None:
        return np.empty((60, 1, 2))
    return coord
    
        
def check_color(position, color):
    grab_position = (position[0], position[1], position[0], position[1])
    grab = grab_screen(region=(grab_position))
    
    if list(grab[0][0]) == color:
        return True 
    else:
        return False

def minmaxloc(num_list):
    try:
        return num_list.index(min(num_list))
    except ValueError:
        return None

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def monster_distance():
    Map = grab_screen(MAP)
    red_indic = red()
    white_indic = white()
    # print(red_indic.shape)
    # print(white_indic.shape)
    # if red_indic is None:
    #     red_indic = monster_distance()
    # if white_indic is None:
    #     white_indic = monster_distance()
    
    
    main_indic = np.concatenate((red_indic, white_indic))
    
    
    x1 = int(Map.shape[0]/2)
    y1 = int(Map.shape[1]/2)
    
    ind_l = []
    
    for i in main_indic:
        x2 = i[0][0]
        y2 = i[0][1]
        # print(f"me on x {x1} monster on x {x2} me on y {y1} monster on y{y2}")
        distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
        ind_l.append(distance)
    
    
    index = utils.minmaxloc(ind_l)
    shortest_distance = ind_l[index]
    # print(shortest_distance)
    
    return shortest_distance
        
    
# measure distance to monster
def find_closest():
    how_long = 2.8
    # print( monster_distance())
    # rotate to find closest target
    start = time.time()
    first_distance = monster_distance()
    if first_distance is None:
        return None
    
        
    time_dist = [utils.round_up(time.time() - start, 1), first_distance]
    while True: 
        keyboard.press('d')
        
        new_distance = monster_distance()
        if new_distance is None:
            return None
        
        if time_dist[1] > new_distance:
            time_dist = [utils.round_up(time.time() - start, 1), new_distance]
            continue
        
        if utils.round_up(time.time() - start, 1) == how_long:
            keyboard.release('d')
            break
        
    # turn to target
    turn_to_closest = time_dist[1]
    
    if time_dist[0] == 0.0:
        print('at begining')
        return time_dist[1]

    second_start = time.time()
    keyboard.press('d')
    
    while True:
        # print(utils.round_up(monster_distance(), 1))
        # print(utils.round_up(turn_to_closest, 1))
        # print(time_dist[0])
        
        print(utils.round_up(time.time() - second_start, 1))
        second_new_distance = monster_distance()
        if second_new_distance is None:
            return None

        if utils.round_up(second_new_distance, 1) == utils.round_up(turn_to_closest, 1):
            print('found')
            time.sleep(0.2)
            keyboard.release('d')
            return time_dist[1]
        if utils.round_up(time.time() - second_start, 1) >= how_long:
            print('not found in time')
            keyboard.release('d')
            return find_closest() 
        
    

def monster_in_range():
    grab_position = (253, 613, 253, 613)
    grab = grab_screen(region=(grab_position))

    # [[[158  29  35]]] color at Point(x=335, y=696)
    
    if list(grab[0][0]) == [150,  29,  35]:
        return False 
    else:
        return True



class Custom_Button():
    def __init__(self, *args, **kwargs):
        pass

    def TAB(self):
        pyautogui.moveTo(546, 548 )
        mouse.press(Button.right)
        time.sleep(0.3)
        mouse.release(Button.right)

    def attack_buttons(self, row, column):
        # provide min collumn of 1
        # provide min row of 1

        x = 27*row + 227
        y = 638 - 27*column 
        
        pyautogui.moveTo(x, y)
        mouse.press(Button.right)
        time.sleep(0.3)
        mouse.release(Button.right)
        time.sleep(0.1)
        # TODO if pressed should go on reload if didn't go on reload was not pressed
        
        pressed = self.all_reload_checker()
        print(pressed)


    def all_reload_checker(self):
        reloading = check_color([498,612], [100,  48,  32])
        return reloading

    def all_reload_checker_loop(self):
        # [[[105  26  78]]] color at Point(x=610, y=695)
        # reloading = check_color([610,695], [105,26,78])
        while True:
            reloading = check_color([498,612], [100,  48,  32])
            if reloading:
                
                pass
            else:
               
                return 

    def attack_pattern(self):
        self.attack_buttons(3,3)
        self.all_reload_checker_loop()
        self.attack_buttons(3,1)
        self.all_reload_checker_loop()
        # check if next attacj possible and old attack still cooldowning
        # infinite loop inside a function here untill possible
        self.attack_buttons(1,1)
        self.all_reload_checker_loop()
        self.attack_buttons(1,1)
        self.all_reload_checker_loop()
        self.attack_buttons(1,1)
        self.all_reload_checker_loop()

        self.attack_buttons(2,1)
        self.all_reload_checker_loop()
        self.attack_buttons(2,1)
        self.all_reload_checker_loop()



        # check if next attacj possible
        self.attack_buttons(4,1)
        self.all_reload_checker_loop()

        # check if next attacj possible
        time.sleep(2)
        self.attack_buttons(4,1)
        self.all_reload_checker_loop() 

        self.attack_buttons(1,1)
        self.all_reload_checker_loop()
        self.attack_buttons(1,1)
        self.all_reload_checker_loop()
        self.attack_buttons(1,1)
        self.all_reload_checker_loop()

        self.attack_buttons(4,1)
        self.all_reload_checker_loop()

        self.attack_buttons(2,1)
        self.all_reload_checker_loop()
        self.attack_buttons(2,1)
        self.all_reload_checker_loop()
        return 

    def heal_cooldown(self):
        if check_color([250,541],[55, 71, 68]):
            return True
        else:
            return False

    def mana_cooldown(self):
        if check_color([277,541],[92, 81, 63]):
            return True
        else:
            return False

    
        
        