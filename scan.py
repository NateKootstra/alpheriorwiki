import numpy as np
import cv2
import time
import mouse

import pyscreenshot as ImageGrab
import pytesseract

def getImage(coords):
    screenshot = np.array(ImageGrab.grab(coords))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    screenshot = cv2.fastNlMeansDenoising(screenshot)
    blur = cv2.GaussianBlur(screenshot, (0, 0), 1)
    # (thresh, screenshot) = cv2.threshold(screenshot, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite("test.png", screenshot)
    return pytesseract.image_to_string(screenshot).strip()

def getWeapon(samples):
    dna = []
    name = []
    desc = []
    dps = []
    dmg = []
    acc = []
    rng = []
    frt = []
    kb = []
    spd = []
    sze = []
    for i in range(samples):
        dna.append(getImage((1300, 180, 1520, 250)))
        name.append(getImage((1100, 230, 1800, 300)))
        desc.append(getImage((1000, 630, 1820, 780)))
        dps.append(getImage((1105, 790, 1210, 840)))
        dmg.append(getImage((1285, 790, 1425, 840)))
        acc.append(getImage((1475, 790, 1580, 840)))
        rng.append(getImage((1665, 790, 1735, 840)))
        frt.append(getImage((1105, 840, 1210, 880)))
        
        spd.append(getImage((1475, 840, 1580, 880)))
        sze.append(getImage((1665, 840, 1735, 880)))
        
        kb.append(getImage((1285, 840, 1425, 880)))
        
        print(str(i+1) + "/" + str(samples))
        
    dna = max(set(dna), key=dna.count)
    name = max(set(name), key=name.count)
    desc = max(set(desc), key=desc.count)
    dps = max(set(dps), key=dps.count)
    dmg = max(set(dmg), key=dmg.count)
    acc = max(set(acc), key=acc.count)
    rng = max(set(rng), key=rng.count)
    frt = max(set(frt), key=frt.count)
    kb = max(set(kb), key=kb.count)
    spd = max(set(spd), key=spd.count)
    sze = max(set(sze), key=sze.count)
    
    print("DNA:  " + dna)
    print("Name: " + name)
    print("Desc: " + desc)
    print("DPS:  " + dps)
    print("DMG:  " + dmg)
    print("ACC:  " + acc)
    print("RNG:  " + rng)
    print("FRT:  " + frt)
    print("KB:   " + kb)
    print("SPD:  " + spd)
    print("SZE:  " + sze)
    
time.sleep(1)
mouse.move(425, 230)
time.sleep(0.1)
mouse.click()
getWeapon(20)