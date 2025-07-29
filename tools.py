import cv2
import os
import numpy as np

from info import turrets, perks

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
        
# scale('perks', 16)
# scale('perks', 32)
# scale('perks', 64)
# scale('turrets', 16)
# scale('turrets', 32)
# scale('turrets', 64)

class Sitemap():
    url = "https://alpherior.wiki"
    text = []
    
    def __init__(self):
        pass
    
    def add(self, page):
        self.text.append(self.url + page + "\n")
        
def update_sitemap():
    sitemap = Sitemap()
    sitemap.add("")
    sitemap.add("/gg")
    sitemap.add("/cc")
    for turret in turrets:
        sitemap.add("/gg/turrets/" + turret.name)
    for perk in perks:
        sitemap.add("/gg/perks/" + perk.name)

    file = open("sitemap.txt", "w")
    file.writelines(sitemap.text)
    file.close()