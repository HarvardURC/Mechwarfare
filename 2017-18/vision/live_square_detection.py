# USAGE
# python picamera_fps_demo.py
# python picamera_fps_demo.py --display 1
'''
NEXT STEPS:
DETECTION: Up to 15 feet away, even for large angles/varying angles, distance to target based on area, thresholding based on color, modify exposure settings,
Varying solidity of contour/patterns, halfsize contour plates, identify largest target plate
current: 2.5 feet, 30 degrees
'''
# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video.fps import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    xmom=[]
    ymom=[]
    thrs=50
    maxar=0
    maxsquare=[]
    for gray in range(1):
        gray=cv2.split(img)[gray]
        _retval, bin = cv2.threshold(gray, thrs, 120, cv2.THRESH_BINARY)
        bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = 4*np.sqrt(cv2.contourArea(cnt))
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv2.contourArea(cnt) > 10:
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
                    cnt_area=cv2.contourArea(cnt)
                    if cnt_area>maxar:
                        maxsquare=[]
                        
                        maxsquare.append(cnt)
                        maxar=cnt_area
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    xmom.append(cx)
                    ymom.append(cy)
                    if len(squares)>=2:
                        squares=maxsquare
                        return squares, xmom, ymom
            
    return squares, xmom, ymom


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
        help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
        help="Whether or not frames should be displayed")
args = vars(ap.parse_args())


# initialize the camera and stream
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
stream = camera.capture_continuous(rawCapture, format="bgr",
        use_video_port=True)


# allow the camera to warmup and start the FPS counter
print("[INFO] sampling frames from `picamera` module...")
time.sleep(0.2)
fps = FPS().start()

# loop over some frames
for (i, f) in enumerate(stream):
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        frame = f.array
        frame = imutils.resize(frame, width=400)
        
        squares, x, y = find_squares(frame)
        print(repr(squares))
        cv2.drawContours( frame, squares, -1, (0, 255, 0), 3 )

        # check to see if the frame should be displayed to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame and update
        # the FPS counter
        rawCapture.truncate(0)
        fps.update()

        # check to see if the desired number of frames have been reached
        if i == args["num_frames"]:
                break
            
        break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()


# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        squares, x, y = find_squares(frame)
        print(len(squares))
        print(repr(squares))
        cv2.drawContours( frame, squares, -1, (0, 255, 0), 3 )

        # check to see if the frame should be displayed to our screen
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # update the FPS counter
        fps.update()
##      print("fps: " + fps.fps())

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
