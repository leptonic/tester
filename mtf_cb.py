###---------------------------------------------------------------------
## The Argorithm about Cacluation of Distortion, Python version
# Author: Yibo 
# Date: 2020 August
#=========Word Explain
#cb=checkboard
#=======================================================================

from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import const
import HGGT
######Settings############
Settings_path = "C:\\dotchart\\f4f6\\MTF_offset.bmp"



img_length=0
img_width=0
img_center_x=0
img_center_y=0
const.DEBUG=1

cb_center=HGGT.dot_pos()

def DEBUG_PRINT(*kwargs):

    if(const.DEBUG):

        print(*kwargs)

print("++++MFT Calculator Start ++++")
##S1 get basic paramter
img = Image.open(Settings_path)
img_length=img.width
img_width=img.height
img_center_x=round(img_length/2,0)
img_center_y=round(img_width/2,0)
##check
# strs="("+str(img_center_x)+","+str(img_center_y)+")"
# DEBUG_PRINT(strs)

imgcv = cv2.imread(Settings_path)

imgcv2=cv2.copyTo(imgcv,imgcv)

gray=cv2.cvtColor(imgcv,cv2.COLOR_BGR2GRAY)
dst = cv2.cornerHarris(gray,2,3,0.04)
# cornerimg=cv2.threshold(dst, 0.015, 255,0)
a_cpp=[]
imgcv2[dst>0.01*dst.max()]=[0,0,255]
for i in range(0,img_length-1):
    for j in range(0,img_width-1):        
        if imgcv2[i,j][0]==0 and imgcv2[i,j][1]==0 and imgcv2[i,j][2]==255:
            cpp=HGGT.dot_pos()
            cpp.x=i
            cpp.y=j
            a_cpp.append(cpp)
#ispos(ix,sx,iy,sy,xdmv,ydmv):
sumx=0
sumy=0
isize=0
for ip in a_cpp:
    if HGGT.ispos(ip.x,img_center_x,ip.y,img_center_y,50,50) is True:
        # strs="("+str(ip.x)+","+str(ip.y)+")"
        # DEBUG_PRINT(strs)
        isize+=1 
        sumx+=ip.x
        sumy+=ip.y

cb_center.x=int(round(sumx/isize,0))
cb_center.y=int(round(sumy/isize,0))
##check
# strs="("+str(cb_center.x)+","+str(cb_center.y)+")"
# DEBUG_PRINT(strs)

cv2.imshow(" ",imgcv)
cv2.waitKey(0) #35  