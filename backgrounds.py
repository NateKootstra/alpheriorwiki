import os
import random
import numpy as np
import cv2
from PIL import Image

def extend_image(image: np.ndarray, height: int, color):
    image_extended = np.ndarray((image.shape[0] + height, image.shape[1] + height) + image.shape[2:], dtype=image.dtype)
    image_extended[int(height/2):image.shape[0] + int(height/2), int(height/2):image.shape[1] + int(height/2)] = image
    image_extended[image.shape[0] + int(height/2):int(height/2), image.shape[1] + int(height/2):int(height/2)] = color
    return image_extended

microbeOptions = []

for microbe in os.listdir("static/images/gg/microbes"):
    microbeOptions.append(microbe)


for name in microbeOptions:
    microbe = cv2.imread("static/images/gg/microbes/" + name)

    microbe = extend_image(microbe, 200, [0, 0, 0])

    result = cv2.addWeighted(cv2.cvtColor(microbe, cv2.COLOR_BGR2RGB),
                            0.3,
                            cv2.GaussianBlur(cv2.cvtColor(microbe, cv2.COLOR_BGR2RGB), (0,0), sigmaX=60, sigmaY=60), 1, 0)

    Image.fromarray(result).save("static/images/gg/background_microbes/" + name)