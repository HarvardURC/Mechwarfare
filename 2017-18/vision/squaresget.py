import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
def findsquares(img, threshold1=110, threshold2=255, colsplit=1):
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    img=cv2.imread(img)
    squares = []
    xmom = []
    ymom = []
    thrs = threshold1
    thrs2=threshold2
    maxcoslim=0.4
    contapprox=0.08
    centdist=100
    maxsquare = []
    maxcx=0
    maxcy=0
    for gray in range(1):
        gray = cv2.split(img)[colsplit]
        _retval, bin = cv2.threshold(gray, thrs, thrs2, cv2.THRESH_BINARY)
        bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = 4 * np.sqrt(cv2.contourArea(cnt))
            cnt = cv2.approxPolyDP(cnt, contapprox * cnt_len, True)
            if len(cnt) == 4 and cv2.contourArea(cnt) > 10:
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                if max_cos < maxcoslim:
                    squares.append(cnt)
                    cnt_area = cv2.contourArea(cnt)
                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])


                    for i in range(len(xmom)):
                        #print(xmom[i]-cx)
                        #print(ymom[i]-cy)
                        if abs(xmom[i]-cx)<centdist and abs(ymom[i]-cy)<centdist:
                            coords=(cx, cy)
                            #print(str(coords))
                            return [cnt], cx, cy
                        else: pass
                    xmom.append(cx)
                    ymom.append(cy)


    return 0, -1, -1