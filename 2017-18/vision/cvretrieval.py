import os
import cv2
import re
import squaresget as sq

root="C:/Users/leorf/PycharmProjects/Mechwarfare/storedcoords"
files=os.listdir(root)
found=False
wrong=0.
right=0.
for file in files:
    found=False
    potentialcoords= []
    numberclauses=re.findall(r"\d+x\d+", file)
    for numberclause in numberclauses:
        beginning, end=numberclause.split('x')
        beginning=int(beginning)
        end=int(end)
        potentialcoords.append((beginning, end))
    image = root + "\\" + file
    image = image.replace("\\", "\\\\")
    squares, x, y=sq.findsquares(image)
    for coord in potentialcoords:
        if abs(x-coord[0])>10. or abs(y-coord[1])>10.:
            pass
        else:
            found=True
            print(coord)
            break
    if not found:
        wrong+=1.
    else:
        right+=1.
print(right/(wrong+right))

print(str(potentialcoords))
