import cv2
import numpy as np

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,i
    if event == cv2.EVENT_LBUTTONDBLCLK:
        ix[i] = x
        iy[i] = y
        i = i + 1

# Create a black image, a window and bind the function to window
table = cv2.imread('chessvision1.png')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

ix = [-1,-1,-1,-1]
iy = [-1,-1,-1,-1]
i = 0

cv2.imshow('image',table)
cv2.waitKey()

pts_src = np.array([[ix[0], iy[0]], [ix[1], iy[1]], [ix[2], iy[2]],[ix[3], iy[3]]])

pts_dst = np.array([[0, 0],[800, 0],[0, 800],[800, 800]])
h, status = cv2.findHomography(pts_src, pts_dst)
im_out = cv2.warpPerspective(table, h, (800,800))

cv2.imshow("Warped Source Image", im_out)
cv2.waitKey()

cv2.imwrite('homografia.png',im_out)
cv2.destroyAllWindows()
