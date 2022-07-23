import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

def find_pixels(img):
	#img = cv2.imread('homog.png')

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	blur = cv2.medianBlur(hsv ,7)

	#red
	lower = np.array([102,82,69])
	upper = np.array([202,204,121])

	mask = cv2.inRange(blur, lower, upper)

	kernel = np.ones((15,15), np.uint8)

	mask = cv2.dilate(mask, kernel, iterations=1)
	mask = cv2.erode(mask, kernel, iterations=1)

	cv2.imshow('image',mask)
	cv2.imwrite("mask_homog.png", mask)
	cv2.waitKey(0)

	cv2.imshow('image',mask)
	cv2.waitKey(0)

	output = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
	centroids = output[3]
	centroids = [centroids[1],centroids[4],centroids[2],centroids[3]]
	print(centroids)
	pts_src = np.array([[int(centroids[0][0]), int(centroids[0][1])], [int(centroids[1][0]), int(centroids[1][1])], [int(centroids[2][0]), int(centroids[2][1])],[int(centroids[3][0]), int(centroids[3][1])]])

	return pts_src

def homografia(pts_src, table):

    pts_dst = np.array([[0, 0],[800, 0],[0, 800],[800, 800]])
    h, status = cv2.findHomography(pts_src, pts_dst)
    im_out = cv2.warpPerspective(table, h, (800,800))

    cv2.imshow("Warped Source Image", im_out)
    cv2.waitKey()

    return im_out
