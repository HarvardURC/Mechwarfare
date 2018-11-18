

import numpy as np
import cv2
import time

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    xmom=[]
    ymom=[]
    thrs=50
    for gray in range(1):
        gray=cv2.split(img)[gray]
        _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
        bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = 4*np.sqrt(cv2.contourArea(cnt))
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv2.contourArea(cnt) > 1000:
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    xmom.append(cx)
                    ymom.append(cy)
                    if np.size(squares)>=2:
                        return squares, xmom, ymom
            
    return squares, xmom, ymom

fn='test640x480.jpg'
t0=time.time()
img = cv2.imread(fn)

squares, x, y = find_squares(img)
print(repr(x))
print(repr(y))
print(repr(squares))


cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
cv2.imshow('squares', img)
t1=time.time()
print(t1-t0)
cv2.waitKey()