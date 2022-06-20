import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#table = cv2.imread('photo1.png')
#plt.imshow(table)
#plt.show()

white = [210 , 238 , 238]
green = [86 ,  150 , 118]


w, h = 4096, 4096
data = np.zeros((h, w, 3), dtype=np.uint8)

for i in range(8):
	for j in range(8):
		if (i+j)%2 == 0:
			data[int(w/8*i):int(w/8*(i+1)), int(h/8*j):int(h/8*(j+1))] = white
		else:
			data[int(w/8*i):int(w/8*(i+1)), int(h/8*j):int(h/8*(j+1))] = green

img = Image.fromarray(data, 'RGB')
img.save('my.png')
#img.show()