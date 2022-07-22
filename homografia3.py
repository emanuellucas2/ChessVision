import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import numpy as np

def find_pixels(img):
    #img = cv2.imread('homog.png')
    #cv2.imshow('image',img)
    #cv2.waitKey(0)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.medianBlur(hsv ,7)

    #black
    lower = np.array([0,0,15])
    upper = np.array([188,85,29])

    mask1 = cv2.inRange(blur, lower, upper)

    #green dark
    lower_dark = np.array([40,30,70])
    upper_dark = np.array([121,105,168])

    #green light
    lower_white = np.array([63,6,132])
    upper_white = np.array([135,40,221])

    mask2 = cv2.inRange(blur, lower_dark, upper_dark)
    mask3 = cv2.inRange(blur, lower_white, upper_white)

    #white
    lower_w = np.array([0,11,142])
    upper_w = np.array([177,23,255])

    mask4 = cv2.inRange(blur, lower_w, upper_w)

    mask = mask1 + mask2 + mask3 + mask4

    kernel = np.ones((100,100), np.uint8)

    mask = cv2.erode(mask,np.ones((10,10), np.uint8), iterations=1)
    mask = cv2.dilate(mask,np.ones((10,10), np.uint8), iterations=1)

    cv2.imshow('image',mask)
    cv2.waitKey(0)

    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(mask, low_threshold, high_threshold)

    cv2.imshow('image',mask)
    cv2.waitKey(0)

    cdst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)

    points = []

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]

            #a = math.cos(theta)
            #b = math.sin(theta)
            #x0 = a * rho
            #y0 = b * rho
            #pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
            #pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
            #cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

            a = -math.tan(theta)
            b = rho/math.cos(theta)

            pt1 = (int(b - 2000*(a)), -2000)
            pt2 = (int(b + 2000*(a)), 2000)
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
            points.insert(0,[a,b])


    cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv2.waitKey(0)

    points2 = []
    m = 10000000000
    for i in range(0,4):
        for j in range(i,4):
            
            if i!=j:
                if points[j][1] > points[i][1]:
                    x = int((points[j][1] - points[i][1])/(points[i][0] - points[j][0]))
                    y = int( points[j][0]*x + points[j][1])
                else:
                    x = int((points[j][1] - points[i][1])/(points[i][0] - points[j][0]))
                    y = int( points[i][0]*x + points[i][1])
                    
                if x>=0 and y>=0 and x<= cdst.shape[0] and y<= cdst.shape[1]: 
                    
                    if((x*x + y*y) < m):
                        points2.insert(0,[x,y])
                        m =  (x^2 + y^2)

                    else:
                        points2.append([x,y])
     
    m = 10000 
    for j in range(1,4):
        if(points2[j][0] < m):
            m = points2[j][0]
            p = j

    po = points2[1]
    points2[1] = points2[p]
    points2[p] = po

    m = 10000 
    for j in range(2,4):
        if(points2[j][1] < m):
            m = points2[j][1]
            p = j

    po = points2[2]
    points2[2] = points2[p]
    points2[p] = po

    pts_src = np.array([[points2[0][1], points2[0][0]], [points2[1][1], points2[1][0]], [points2[2][1], points2[2][0]],[points2[3][1], points2[3][0]]])

    cv2.imshow('image',edges)
    cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv2.waitKey(0)

    return pts_src

def homografia(pts_src, table):

    pts_dst = np.array([[0, 0],[800, 0],[0, 800],[800, 800]])
    h, status = cv2.findHomography(pts_src, pts_dst)
    im_out = cv2.warpPerspective(table, h, (800,800))

    #cv2.imshow("Warped Source Image", im_out)
    #cv2.waitKey()

    return im_out