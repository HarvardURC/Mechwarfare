import os
import cv2
import re
import squaresget as sq

root="C:/Users/leorf/PycharmProjects/Mechwarfare/storedcoords"
files=os.listdir(root)
found=False
wrong=0.
right=0.
maxthrs1=0
maxthrs2=0
maxperform=0
for k in range(2):
    for i in range(0, 255, 5):
        for j in range(i+1, 255, 5):
            wrong = 0.
            right = 0.
            for file in files:

                found=False
                potentialcoords= []
                numberclauses=re.findall(r"\d+x\d+", file)
                if 'NaN' in file:
                    potentialcoords=[(-1, -1)]
                for numberclause in numberclauses:
                    beginning, end=numberclause.split('x')
                    beginning=int(beginning)
                    end=int(end)
                    potentialcoords.append((beginning, end))
                image = root + "\\" + file
                image = image.replace("\\", "\\\\")
                squares, x, y=sq.findsquares(image, i, j, k)
                for coord in potentialcoords:
                    #print(str(coord))
                    if abs(x-coord[0])>15. or abs(y-coord[1])>15.:
                        pass
                    else:
                        found=True
                        #print(coord)
                        break
                if not found:
                    wrong+=1.
                    #print(file + " incorrect")
                else:
                    right+=1.
                    #print(file + " correct")
            perform=right/(wrong+right)
            if perform>maxperform:
                maxperform=perform
                maxthrs1=i
                maxthrs2=j
            print(right/(wrong+right))
print((maxperform, maxthrs1, maxthrs2))
#print(str(potentialcoords))
