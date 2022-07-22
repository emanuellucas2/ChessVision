import cv2
import matplotlib.pyplot as plt
import numpy as np

def squares(table,k,ti,matrix):


	tf = np.empty((8,8), dtype=str)
	count = 0

	for i in range(8):
		for j in range(8):

			#image= table[20:780,20:780]

			#cv2.imshow('image',image)
			#cv2.waitKey()

			img = table[int(100*i):int(100*(i+1)),int(100*j):int(100*(j+1))]

			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			blur = cv2.medianBlur(hsv ,7)
			
			#black
			lower = np.array([0,0,6])
			upper = np.array([165,191,28])

			mask = cv2.inRange(blur, lower, upper)

			#green dark
			lower_dark = np.array([63,46,127])
			upper_dark = np.array([108,101,184])

			#green light
			lower_white = np.array([85,1,168])
			upper_white = np.array([161,39,245])

			mask1 = cv2.inRange(blur, lower_dark, upper_dark)
			mask2 = cv2.inRange(blur, lower_white, upper_white)


			mask3 = mask1 + mask2

			kernel = np.ones((19,19), np.uint8)
			
			#mask3 = cv2.erode(mask3, kernel, iterations=1)
			#mask3 = cv2.dilate(mask3, kernel, iterations=1)
			
			mask3 = cv2.dilate(mask3, kernel, iterations=1)
			mask3 = cv2.erode(mask3, kernel, iterations=1)

			mask3 = 255-mask3

			#cv2.imshow('image',mask)
			#cv2.waitKey()

			if mask.any():
				cv2.imwrite("squares" + str(k) + "/" + str(i) + str(j) + "preta.png",mask3)
			elif mask3[20:80,20:80].any():
				cv2.imwrite("squares" + str(k) + "/" + str(i) + str(j) + "branca.png",mask3)
			else:
				cv2.imwrite("squares" + str(k) + "/" + str(i) + str(j) + "vazia.png",mask3)

			if mask.any():
				tf[i][j] = "black"
			elif mask3[20:80,20:80].any():
				tf[i][j] = "white"
			else:
				tf[i][j] = "blank"

			if(ti[i][j] != tf[i][j]):
				count += 1

	if(count == 0):
		return tf
	elif(count == 2):
		
		for i in range(8):
			for j in range(8):
				if(ti[i][j] != tf[i][j]):
					if(tf[i][j]!="blank"):
						old_piece = matrix.t[i][j]
						matrix.t[i][j] = Square("None","None")
					else:
						x = i
						y = j

		matrix.t[i][j] = old_piece
		return tf
	elif(count == 3):

		return tf	

def init_squares(table,k):


	tf = np.empty((8,8), dtype=str)

	for i in range(8):
		for j in range(8):

			#image= table[20:780,20:780]

			#cv2.imshow('image',image)
			#cv2.waitKey()

			img = table[int(100*i):int(100*(i+1)),int(100*j):int(100*(j+1))]

			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			blur = cv2.medianBlur(hsv ,7)
			
			#black
			lower = np.array([0,0,6])
			upper = np.array([165,191,28])

			mask = cv2.inRange(blur, lower, upper)

			#green dark
			lower_dark = np.array([63,46,127])
			upper_dark = np.array([108,101,184])

			#green light
			lower_white = np.array([85,1,168])
			upper_white = np.array([161,39,245])

			mask1 = cv2.inRange(blur, lower_dark, upper_dark)
			mask2 = cv2.inRange(blur, lower_white, upper_white)


			mask3 = mask1 + mask2

			kernel = np.ones((19,19), np.uint8)
			
			#mask3 = cv2.erode(mask3, kernel, iterations=1)
			#mask3 = cv2.dilate(mask3, kernel, iterations=1)
			
			mask3 = cv2.dilate(mask3, kernel, iterations=1)
			mask3 = cv2.erode(mask3, kernel, iterations=1)

			mask3 = 255-mask3

			#cv2.imshow('image',mask)
			#cv2.waitKey()

			if mask.any():
				cv2.imwrite("squares" + str(k) + "/" + str(i) + str(j) + "preta.png",mask3)
			elif mask3[20:80,20:80].any():
				cv2.imwrite("squares" + str(k) + "/" + str(i) + str(j) + "branca.png",mask3)
			else:
				cv2.imwrite("squares" + str(k) + "/" + str(i) + str(j) + "vazia.png",mask3)

			if mask.any():
				tf[i][j] = "black"
			elif mask3[20:80,20:80].any():
				tf[i][j] = "white"
			else:
				tf[i][j] = "blank"

	return tf	