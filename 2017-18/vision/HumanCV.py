import cv2
import os
'''
HumanCV takes a directory of images and displays them 1 by 1--at each image the user can select approximate target centers by clicking,
clear prior selections with the 'r' key, save their selections and move onto the next image with 'c', and state that
there are no targets with 'n'.
Once this is done, the program encodes target coordinates into the filename of the image, clones it, and saves the clone
as an image file with that filename.
'''

root="C:/Users/leorf/PycharmProjects/Mechwarfare/images" #replace with path to your image directory here
files=os.listdir(root)

refPt = []
targetsel = False
circlesel=0
print(str(files))
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, targetsel, circlesel

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate the selected location with a circle
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        targetsel = True
        cv2.circle(image, refPt[circlesel], 2, (0, 255, 0), 2)
        circlesel+=1
    elif event==cv2.EVENT_LBUTTONUP:
        pass
for x in range(len(files)):
    refPt = []
    targetsel = False
    circlesel = 0
    image=files[x]
    image=root+"\\"+image
    image=image.replace("\\", "\\\\")
    image = cv2.imread(image)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()
            refPt=[]
            circlesel=0
        #if n is pressed, there is no target, move on
        if key==ord("n"):
            refPt=[]
            circlesel=0
            break

        # if the 'c' key is pressed and a target or more has been selected, break from the loop
        elif key == ord("c") and len(refPt)>0:
            break
    #generate filename holding target coordinates
    if len(refPt) ==0:
        filename="img"+str(x+1) + "-NaN.jpg"
    elif len(refPt)==1:
        filename="img"+ str(x+1) + "-" + str(refPt[0][0]) + "x" + str(refPt[0][1])+".jpg"
        print(filename)
    else:
        filename="img"+ str(x+1) + "-"
        for coord in refPt:
            filename+=str(coord[0]) + "x" + str(coord[1]) + "_"
        filename+=".jpg"
    cv2.imwrite(filename, clone)
    cv2.destroyAllWindows()
