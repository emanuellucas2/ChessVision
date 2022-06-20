import cv2
import matplotlib.pyplot as plt
import numpy as np

table = cv2.imread('homografia.png')

for i in range(8):
	for j in range(8):

		img = table[int(100*i):int(100*(i+1)),int(100*j):int(100*(j+1))]

		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		blur = cv2.medianBlur(hsv ,7)
		
		lower = np.array([40,28,2])
		upper = np.array([90,255,12])

		mask = cv2.inRange(blur, lower, upper)

		#green dark
		lower_dark = np.array([40,30,70])
		upper_dark = np.array([121,105,168])

		#green light
		lower_white = np.array([60,2,144])
		upper_white = np.array([124,18,182])

		mask1 = cv2.inRange(blur, lower_dark, upper_dark)
		mask2 = cv2.inRange(blur, lower_white, upper_white)


		mask2 = mask1 + mask2

		kernel = np.ones((15,15), np.uint8)

		mask2 = cv2.dilate(mask2, kernel, iterations=1)
		mask2 = cv2.erode(mask2, kernel, iterations=1)

		mask2 = 255-mask2

		if mask.any():
			cv2.imwrite("squaresMask2/sq" + str(i) + str(j) + "preta.png",mask2)
		elif mask2.any():
			cv2.imwrite("squaresMask2/sq" + str(i) + str(j) + "branca.png",mask2)
		else:
			cv2.imwrite("squaresMask2/sq" + str(i) + str(j) + "vazia.png",mask2)
