import cv2
import matplotlib.pyplot as plt
import numpy as np

table = cv2.imread('chessvision1.png')
hsv = cv2.cvtColor(table, cv2.COLOR_BGR2HSV)
blur = cv2.medianBlur(hsv ,7)

#green dark
lower_dark = np.array([40,30,70])
upper_dark = np.array([121,105,168])

#black
#lower_dark = np.array([40,28,2])
#upper_dark = np.array([90,255,12])

#white
#lower_dark= np.array([18,2,125])
#upper_dark = np.array([90,20,173])

#green light
lower_white = np.array([60,2,144])
upper_white = np.array([124,18,182])

mask = cv2.inRange(blur, lower_dark, upper_dark)
mask2 = cv2.inRange(blur, lower_white, upper_white)


mask = mask + mask2

kernel = np.ones((15,15), np.uint8)

mask = cv2.dilate(mask, kernel, iterations=1)
mask = cv2.erode(mask, kernel, iterations=1)

res = cv2.bitwise_and(table,table, mask= mask)

#cv2.imwrite("result.png", res)
plt.imshow(mask)
plt.show()
