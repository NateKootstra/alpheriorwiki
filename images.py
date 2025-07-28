import cv2
import os
import numpy as np

def scale(folder, size):
    try:
        os.makedirs('static/images/gg/' + folder + '/' + str(size) + 'x' + str(size))
    except:
        pass
    for turret in os.listdir('static/images/gg/' + folder):
        if turret.endswith('.png'):
            img = cv2.imread('static/images/gg/' + folder + '/' + turret, cv2.IMREAD_UNCHANGED)
            small = cv2.resize(img, dsize=(size, size), interpolation=cv2.INTER_AREA)
            cv2.imwrite('static/images/gg/' + folder + '/' + str(size) + 'x' + str(size) + '/' + turret, small)
        
scale('perks', 16)
scale('perks', 32)
scale('perks', 64)
scale('turrets', 16)
scale('turrets', 32)
scale('turrets', 64)