###---------------------------------------------------------------------
## The Argorithm about Cacluation of Distortion, Python version
# Author: Yibo 
# Date: 2020 July
#=========Word Explain
#RCS =Relative Coordinates System
#map = the theoretical point position 
#v= virtual ,means include negative number
#spot= the true point in the picture
#img= the tru picture
#golden 9 spots =the spots beside the true center spot in photo
#unit= the length of side of center square
#star=golden 9 spots
#=======================================================================
from PIL import Image
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import isnan
import const
import sys
import Take1Photo
# import math 


######Settings############
Settings_path ="C:\\dotchart\\f5\\UVC175.jpg"# "C:\\dotchart\\f5\\f5im2.bmp"
Settings_output_picture='C:/Users/YY/Desktop/photos/'
Settings_pixel_size=1.55
Settings_EFL_mm=2.5
Settings_PTR_star_offset=3 #
Settings_font = cv2.FONT_HERSHEY_SIMPLEX
################################

img_length=0
img_width=0
img_center_x=0
img_center_y=0

spot_center_x=0
spot_center_y=0
spot_deviation=100
spot_G9_deviation=0
spot_count=0
spot_G9_list=[[] for i in range(2)] 
spot_Unit=0
spot_dia=0

map_Row_cnt=0
map_Column_cnt=0
map_offset_x=0
map_offset_y=0
map_theta=0.0
map_count=0
fmap=[]
All_dots=[] #real all spots in photo

draw_cycle_dia=4
standard_chart_dia=12.34
min_detected_dot=int(round(standard_chart_dia-standard_chart_dia*.55,0))
max_detected_dot=int(round(standard_chart_dia+standard_chart_dia*.55,0))
const.DEBUG=1


class cdot_map:
    def __init__(self):
        # self.row=0
        # self.column=0
        self.num=0
        self.x=0
        self.y=0
class dot_pos:
    def __init__(self):
        # self.row=0
        # self.column=0        
        self.x=0
        self.y=0
class vdot_pos:
    def __init__(self):
        # self.row=0
        # self.column=0        
        self.x=0.0
        self.y=0.0
class cRCS:
     def __init__(self):
        # self.row=0
        # self.column=0
        self.rcs_x=0.0
        self.rcs_y=0.0
        self.x=0
        self.y=0

class cDT:
     def __init__(self):
        # self.row=0
        # self.column=0
        self.rcs_x=0.0
        self.rcs_y=0.0
        self.distortion=0.0
class cRelation_map:
    def __init__(self):
        self.map_num=0
        self.spot_num=0
        

Star_Up=dot_pos()
Star_Down=dot_pos()
Star_Left=dot_pos()
Star_Right=dot_pos()

Star_LU=dot_pos()
Star_RU=dot_pos()
Star_LD=dot_pos()
Star_RD=dot_pos()


PTR_Up=dot_pos()
PTR_Down=dot_pos()
PTR_Left=dot_pos()
PTR_Right=dot_pos()
PTR_LU=dot_pos()
PTR_RU=dot_pos()
PTR_LD=dot_pos()
PTR_RD=dot_pos()

def DEBUG_PRINT(*kwargs):

    if(const.DEBUG):

        print(*kwargs)

def error_report(str):
    print("\r\n\r\n\r\n\r\n")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Error:",str)     
    print("\r\n\r\n\r\n\r\n")    

def ispos(ix,sx,iy,sy,xdmv,ydmv):
    if ix<(sx+xdmv) and ix>(sx-xdmv):
        if iy<(sy+ydmv) and iy>(sy-ydmv):
            return True
        else:
            return False
    else:
        return False
def isValue(ix,sx,xm):
    if ix<(sx+xm) and ix>(sx-xm):
        return True
    else:
        return False   
def Get_Average(list):
    sum=0
    for item in list :
        sum+=item
    return sum/len(list) 

def getUnit():
    golden_unit_temp=[]
    global spot_G9_list
    for i in range(9):
      x1=spot_G9_list[0][i]
      y1=spot_G9_list[1][i]    
      for j in range(9):
          x2=spot_G9_list[0][j]
          y2=spot_G9_list[1][j]
          #print(x1,x2,y1,y2)
          xd=0
          yd=0
          x1=int(x1)
          x2=int(x2)
          y1=int(y1)
          y2=int(y2)
          distance=(((x1-x2)**2+(y1-y2)**2)**0.5)
          #print("distance",distance)
          if distance != 0:
                golden_unit_temp.append(distance)

    golden_unit_temp.sort(reverse=False)
    MiniValue=golden_unit_temp[0]
   # print(golden_unit_temp)
    
    #set  (square root 2) as deviataion
    sr2_dev=0.271828*MiniValue#0.414 is hypotenuse 
    #Get all golden unit and calculate the average one
    golden_unit_temp2=[]
    for i in range(len(golden_unit_temp)):
        if(isValue(MiniValue,golden_unit_temp[i],sr2_dev)):
            golden_unit_temp2.append(golden_unit_temp[i])
    # print("golden_unit_temp2",golden_unit_temp2)
    return Get_Average(golden_unit_temp2)


def abs_value(a):
    
    if a >= 0:
        a = a
    else:
        a = -a
    return a


def get_distance(x1,y1,x2,y2):
    return (((float(x1)-float(x2))**2+(float(y1)-float(y2))**2)**0.5)   

def detect_direct(x0,y0,x1,y1,dotUnit,sin_t):
    global spot_dia
    if dotUnit==0: #or sin_t==0:
        print("!!!Error input error at >>Detect_Direct<<")
    if(get_distance(x0,y0,x1,y1)>(1.414*dotUnit)) or (x0==x1 and y0==y1):
        return 0
    else:
        if (y1<(y0+sin_t*dotUnit) and y1>(y0-sin_t*dotUnit)):#Sin(5 degree)=0.087 
            if x1>x0 :
                return 4
            else:
                return 3

        if  (x1<(x0+sin_t*dotUnit) and x1>(x0-sin_t*dotUnit)):#Sin(5 degree)=0.087
            if y1>y0:
                return 2
            else:
                return 1

#get some basic parameters
# print("=========Test Component==========")

# Take1Photo.Capture(Settings_output_picture)

# sys.exit()
print("=========Start==========")

img = Image.open(Settings_path)

img_length=img.width
img_width=img.height
img_center_x=round(img_length/2,0)
img_center_y=round(img_width/2,0)
  ##check
print("w=",img_length,"l=",img_width,"cx=",img_center_x,"cy=",img_center_y)

#S0. Find the center point
imgcv = cv2.imread(Settings_path)
GrayImage= cv2.cvtColor(imgcv,cv2.COLOR_BGR2GRAY)
GrayImage= cv2.medianBlur(GrayImage,5)
ret,th1 = cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,  
                    cv2.THRESH_BINARY,3,5)  
th3 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  
                    cv2.THRESH_BINARY,3,5)

kernel = np.ones((5,5),np.uint8)

# cv2.imshow("257",th2)
# cv2.waitKey(0) #35

# erosion = cv2.erode(th2,kernel,iterations=1)
# dilation = cv2.dilate(erosion,kernel,iterations=1)
# imgray=cv2.Canny(erosion,30,100)#(erosion,1,30) 30 100

imgray=cv2.Canny(th1,30,100)#(erosion,1,30) 30 100


# cv2.imshow("257",imgray)
# cv2.waitKey(0) #35
# circles = cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,1,30,
#                             param1=50,param2=30,minRadius=5,maxRadius=60)
# circles = cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,1,30,
                            # param1=50,param2=10,minRadius=min_detected_dot,maxRadius=max_detected_dot)
circles = cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,1,10,
                            param1=1,param2=10,minRadius=32,maxRadius=39)
cc=0
circles = np.uint16(np.around(circles))

# print f
#print(circles)
ct=0
for cp in circles[0,:]: 
    ct+=1
    cv2.circle(imgcv,(cp[0],cp[1]),5,(0,255,255))

#Optimize redundancy point
# 
# cv2.imshow(" ",imgray)
# cv2.waitKey(0) #35

# cv2.imwrite("C:\\dotchart\\f5\\UVC0ttt.jpg",imgcv)
# cv2.imshow("274",imgcv)
# cv2.waitKey(0) #35


# print("Detected cycle:")
# print(ct)   
# sys.exit()
#Find the centry spot
spot_deviation=0
goldSpot_cnt=0
print("-----174----")
for i in range(200):
    spot_deviation= i
   
    goldSpot_cnt=0
    for cp in circles[0,:]: 
          
        if(ispos(cp[0],img_center_x,cp[1],img_center_y,spot_deviation,spot_deviation)) :
            goldSpot_cnt+=1
            #print(goldSpot_cnt)

    if goldSpot_cnt == 1:
        print("spot_Center_deviation=",spot_deviation)
        break
##get spot center
if goldSpot_cnt==1:       
    for cp in circles[0,:]:
        spot_count=spot_count+1
        if(ispos(cp[0],img_center_x,cp[1],img_center_y,spot_deviation,spot_deviation)) :
            spot_center_x=cp[0]
            spot_center_y=cp[1]
            spot_dia=cp[2]*2
            print("\r\n\r\n")
            print("==Found Center Spot :",spot_center_x,spot_center_y,spot_dia)
           
            print("Image center:",img_center_x,img_center_y)
            cv2.circle(imgcv,(cp[0],cp[1]),draw_cycle_dia,(0,0,255))
        # else:
        #     cv2.circle(imgcv,(cp[0],cp[1]),draw_cycle_dia,(255,255,0))
else:
    sgtr="Canot found Center Spot  "
    error_report(sgtr)

print("==>Detected spots :" ,spot_count)
#Find Golden 9 spots

for i in range(200):
    spot_G9_deviation=0
    goldSpot_cnt=0
    spot_G9_deviation=spot_deviation+i*5
    # print(i)
    for cp in circles[0,:]:       
        if(ispos(cp[0],img_center_x,cp[1],img_center_y,spot_G9_deviation,spot_G9_deviation)) :
            goldSpot_cnt+=1

    # print("gsc:",goldSpot_cnt)

    if goldSpot_cnt == 9:       
        print("spot_G9_deviation=",spot_G9_deviation)
        break

for cp in circles[0,:]:
    
    if(ispos(cp[0],img_center_x,cp[1],img_center_y,spot_G9_deviation,spot_G9_deviation)) :
        #print(cp[0],cp[1])
        # cv2.circle(imgcv,(cp[0],cp[1]),draw_cycle_dia,(0,0,255))
        spot_G9_list[0].append(cp[0])
        spot_G9_list[1].append(cp[1])

#print(spot_G9_list)        
# cv2.imshow(" ",imgcv)
# cv2.waitKey(0) #35        
   
#S1. Get Spot Unit

spot_Unit=int(round(getUnit(),0))

print("=spot_Unit",spot_Unit)

# print("Unit is :",spot_Unit)

#S2. Draw the theroy spot map
#eg R=1 C=1 Pos=(x,y),set up 2-dimensional array
    
#img_length  img_width
#  Get Row & Column Count
map_Row_cnt=int(img_width/spot_Unit)
map_Column_cnt=int(img_length/spot_Unit)


# print("r=",map_Row_cnt,"c=",map_Column_cnt)

#Get the theory map
#cv2.circle(imgcv,(img_center_x,img_center_y),draw_cycle_dia,(0,0,255))

#old algorathm
# # map_offset_x=int(round(spot_center_x-img_center_x,0))
# # map_offset_y=int(round(spot_center_y-img_center_y,0))

# # print("offset x=",map_offset_x,"offset y=",map_offset_y)
# # #cdot_map
# # maps=[]
# # for j in range(0,map_Row_cnt):##+2
# #     for i in range(0,map_Column_cnt):  ##+2
# #         spott=cdot_map()
# #         spott.row=j ##
# #         spott.column=i
# #         spott.x=int(i*spot_Unit)+ map_offset_x  ##
# #         spott.y=int(j*spot_Unit)+ map_offset_y
# #         maps.append(spott)
#check
# for i in maps:
#     #print (i.x,i.y)
#     cv2.circle(imgcv,(i.x,i.y),draw_cycle_dia,(0,0,255))
# S2.0 set Map center point
map_x=[]
map_y=[]

for i in range(0,int(map_Column_cnt/2)+3):
    ox=spot_center_x+i*spot_Unit
    if ox<=img_length:
        map_x.append(ox)
    ox=spot_center_x-i*spot_Unit
    if ox>=0:
        map_x.append(ox)

# Draw Cross of Center
for i in range(0,int(map_Row_cnt/2)+3):
    oy=spot_center_y+i*spot_Unit
    if oy<=img_width:
        map_y.append(oy)
    oy=spot_center_y-i*spot_Unit
    if oy>=0:
        map_y.append(oy)     

#S2.1 Get PTR Dots_cross
#Settings_PTR_star_offset spot_center_y

#S2.1.2 Get Star_Up Star_Down Star_Left Star_Right
PTRoffset=Settings_PTR_star_offset*spot_Unit
Star_Up.x=spot_center_x
Star_Up.y=spot_center_y-PTRoffset

Star_Down.x=spot_center_x
Star_Down.y=spot_center_y+PTRoffset

Star_Left.x=spot_center_x-PTRoffset
Star_Left.y=spot_center_y

Star_Right.x=spot_center_x+PTRoffset
Star_Right.y=spot_center_y
#check
# cv2.circle(imgcv,(Star_Up.x,Star_Up.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(Star_Down.x,Star_Down.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(Star_Left.x,Star_Left.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(Star_Right.x,Star_Right.y),draw_cycle_dia,(0,0,255))


PTR_deviation=spot_dia*1.618## 2.1 TBD

print("PTR deviation",PTR_deviation)
# print("===Star UP :",Star_Up.x,Star_Up.y)
for cp in circles[0,:]:
    #print("detected cycle:",cp[0],cp[1])
    if(ispos(cp[0],Star_Up.x,cp[1],Star_Up.y,PTR_deviation,PTR_deviation)) :
        PTR_Up.x=cp[0]
        PTR_Up.y=cp[1]
       
    if(ispos(cp[0],Star_Down.x,cp[1],Star_Down.y,PTR_deviation,PTR_deviation)) :
        PTR_Down.x=cp[0]
        PTR_Down.y=cp[1]    

    if(ispos(cp[0],Star_Left.x,cp[1],Star_Left.y,PTR_deviation,PTR_deviation)) :
        PTR_Left.x=cp[0]
        PTR_Left.y=cp[1]    

    if(ispos(cp[0],Star_Right.x,cp[1],Star_Right.y,PTR_deviation,PTR_deviation)) :
        PTR_Right.x=cp[0]
        PTR_Right.y=cp[1]   

##check
# cv2.circle(imgcv,(PTR_Up.x,PTR_Up.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(PTR_Down.x,PTR_Down.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(PTR_Left.x,PTR_Left.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(PTR_Right.x,PTR_Right.y),draw_cycle_dia,(0,0,255))
###
Star_LU.x=int((PTR_Up.x-PTRoffset+PTR_Left.x)/2)
Star_LU.y=int((PTR_Up.y+PTR_Left.y-PTRoffset)/2)

# print(Star_LU)
Star_LD.x=int((PTR_Down.x-PTRoffset+PTR_Left.x)/2)
Star_LD.y=int((PTR_Down.y+PTR_Left.y+PTRoffset)/2)

Star_RU.x=int((PTR_Up.x+PTRoffset+PTR_Right.x)/2)
Star_RU.y=int((PTR_Up.y+PTR_Right.y-PTRoffset)/2)

Star_RD.x=int((PTR_Down.x+PTRoffset+PTR_Right.x)/2)
Star_RD.y=int((PTR_Down.y+PTR_Right.y+PTRoffset)/2)
if  Star_LU.x==0 or Star_LD.x==0 or Star_RD.x==0 or Star_RU.x==0 :
    sgtr="Can't find PTR point\r\n"
    sgtr+=" Star_LUx:"+str(Star_LU.x)+" Star_LUy:"+str(Star_LU.y)+"\r\n"
    sgtr+=" Star_LDx:"+str(Star_LD.x)+" Star_LDy:"+str(Star_LD.y)+"\r\n"
    sgtr+=" Star_RUx:"+str(Star_RU.x)+" Star_RUy:"+str(Star_RU.y)+"\r\n"
    sgtr+=" Star_RD:"+str(Star_RD.x)+" Star_RDy:"+str(Star_RD.y)+"\r\n"
    error_report(sgtr)
# ##check
# cv2.circle(imgcv,(Star_LU.x,Star_LU.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(Star_LD.x,Star_LD.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(Star_RU.x,Star_RU.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(Star_RD.x,Star_RD.y),draw_cycle_dia,(0,0,255))


for cp in circles[0,:]: 
    cdot=dot_pos()
    cdot.x=cp[0]
    cdot.y=cp[1]
    All_dots.append(cdot)
    if(ispos(cp[0],Star_LU.x,cp[1],Star_LU.y,PTR_deviation,PTR_deviation)) :
        PTR_LU.x=cp[0]
        PTR_LU.y=cp[1]
       # print("eeeee",PTR_LU.x,PTR_LU.y)
    if(ispos(cp[0],Star_LD.x,cp[1],Star_LD.y,PTR_deviation,PTR_deviation)) :
        PTR_LD.x=cp[0]
        PTR_LD.y=cp[1]    

    if(ispos(cp[0],Star_RU.x,cp[1],Star_RU.y,PTR_deviation,PTR_deviation)) :
        PTR_RU.x=cp[0]
        PTR_RU.y=cp[1]    

    if(ispos(cp[0],Star_RD.x,cp[1],Star_RD.y,PTR_deviation,PTR_deviation)) :
        PTR_RD.x=cp[0]
        PTR_RD.y=cp[1]   
if  PTR_LU.x==0 or PTR_LD.x==0 or PTR_RU.x==0 or PTR_RD.x==0 :
    sgtr="Can't find PTR point\r\n"
    sgtr+=" PTR_LUx:"+str(PTR_LU.x)+" LUy:"+str(PTR_LU.y)+"\r\n"
    sgtr+=" PTR_LDx:"+str(PTR_LD.x)+" PTR_LDy:"+str(PTR_LD.y)+"\r\n"
    sgtr+=" PTR_RUx:"+str(PTR_RU.x)+" PTR_RUy:"+str(PTR_RU.y)+"\r\n"
    sgtr+=" PTR_RDx:"+str(PTR_RD.x)+" PTR_RDy:"+str(PTR_RD.y)+"\r\n"
    error_report(sgtr)
# ##check
# cv2.circle(imgcv,(PTR_LU.x,PTR_LU.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(PTR_LD.x,PTR_LD.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(PTR_RU.x,PTR_RU.y),draw_cycle_dia,(0,0,255))
# cv2.circle(imgcv,(PTR_RD.x,PTR_RD.y),draw_cycle_dia,(0,0,255))

##TBD Calculate PTR
##
## Need To Filled
##
##
##S2.4 Get theta
Delta_x=0.0
Delta_x=float(PTR_LU.x)-float(PTR_LD.x)
#Delta_x=((float(PTR_LU.x)-float(PTR_LD.x))+float(PTR_Up.x)-float(PTR_Down.x)+float(PTR_RU.x)-float(PTR_RD.x))/3

Delta_y=0.0
Delta_y=float(PTR_LU.y)-float(PTR_RU.y)
#Delta_y=((float(PTR_LU.y)-float(PTR_RU.y))+(float(PTR_LD.y)-float(PTR_RD.y)))/3


# Tan_Theta_x=Delta_y/(PTRoffset*2)
# Theta_x=np.degrees(np.arctan(Tan_Theta_x))
#Follow the Bari Agorithm
# print(PTR_LU.x,PTR_LU.y,PTR_LD.x,PTR_LD.y)
Minute_A=get_distance(float(PTR_LU.x),float(PTR_LU.y),float(PTR_LD.x),float(PTR_LD.y))
#print(Minute_A)
theory_LU=dot_pos()
theory_LU.x=PTR_LD.x
theory_LU.y=PTR_LD.y-PTRoffset*2
LA=get_distance(float(PTR_LU.x),float(PTR_LU.y),float(theory_LU.x),float(theory_LU.y))
Sin_x=LA/Minute_A
#print(LA)
Theta_x=np.degrees(np.arcsin(Sin_x))



Minute_B=get_distance(float(PTR_LD.x),float(PTR_LD.y),float(PTR_RD.x),float(PTR_RD.y))
#print(Minute_A)
theory_RD=dot_pos()
theory_RD.x=PTR_LD.x+PTRoffset*2
theory_RD.y=PTR_LD.y

LB=get_distance(float(PTR_RD.x),float(PTR_RD.y),float(theory_RD.x),float(theory_RD.y))
#print(LA)
Sin_y=LB/Minute_B

Theta_y=np.degrees(np.arcsin(LB/Minute_B))
map_theta=(Theta_x+Theta_y)/2
# map_theta=5
if PTR_LU.y > PTR_RU.y:
    
    map_theta=0-map_theta # is PTR 's R !!

else:

    map_theta= map_theta# is PTR 's R !!
#pixel_size=1.55
#EFL_mm=2.5
#pan = Math.Atan(((cx - FULLSIZE_WIDTH/2) * IQTester.Properties.Settings.Default.Pixel_size_um) / (IQTester.Properties.Settings.Default.EFL_mm * 1000)) * 180 / Math.PI;
tanPan=((spot_center_x-img_center_x)*Settings_pixel_size)/Settings_EFL_mm
Pan=np.degrees(np.arctan(tanPan))

tanTilt=((spot_center_y-img_center_y)*Settings_pixel_size)/Settings_EFL_mm
Tilt=np.degrees(np.arctan(tanTilt))

print("\r\n\r\n\r\n")  
print(">>>>>>>tanPan:",Pan)
print(">>>>>>>tanTilt:",Tilt)
print(">>>>>>>Rotation:",map_theta)
print("\r\n\r\n\r\n")
#Draw all map

Cos_theta=np.cos(map_theta*np.pi/180)
Sin_theta=np.sin(map_theta*np.pi/180)
print("cos",Cos_theta,"sin",Sin_theta)
# Cos_theta=np.cos(5*np.pi/180)##only for debug
# Sin_theta=np.sin(5*np.pi/180)##only for debug
#print (map_x)
# #check
# for i in map_x:
#     #print (i.x,i.y)
#     cv2.circle(imgcv,(i,spot_center_y),draw_cycle_dia,(0,0,255))
# for i in map_y:s
#     #print (i.x,i.y)
#     cv2.circle(imgcv,(spot_center_x,i),draw_cycle_dia,(0,0,255))



#S2.5 Draw All Map
#   
# 
#cdot_map
#fmap=[]
#up part
for j in range(0,int(map_Row_cnt/2)+3):
    # ycenter=dot_pos()

    vycenter=vdot_pos()

    vycenter.y=float(spot_center_y)-float(j*spot_Unit*Cos_theta)
    if  vycenter.y>-float(3*spot_Unit*Cos_theta):
        
        vycenter.x=float(spot_center_x)+float(j*spot_Unit*Sin_theta)
    else:
        break

    for i in range(0,int(map_Column_cnt/2)+3):
        oRow=dot_pos()
        oRow.x=int(vycenter.x+i*spot_Unit*Cos_theta)
        if oRow.x<=img_length:
            oRow.y=int(vycenter.y+i*spot_Unit*Sin_theta)
            fmap.append(oRow)
        else:
            break

    for i in range(1,int(map_Column_cnt/2)+3):  
        oRow=dot_pos()    
        oRow.x=int(vycenter.x-i*spot_Unit*Cos_theta)
        if oRow.x>0:
            oRow.y=int(vycenter.y-i*spot_Unit*Sin_theta)
            fmap.append(oRow)
        else:
            break
#down part
for j in range(1,int(map_Row_cnt/2)+3):
    vycenter=vdot_pos()

    vycenter.y=float(spot_center_y)+float(j*spot_Unit*Cos_theta)
    
    if  vycenter.y<=float(img_width)+3*spot_Unit*Cos_theta:
        vycenter.x=float(spot_center_x)-j*spot_Unit*Sin_theta
    else:
        break

    for i in range(0,int(map_Column_cnt/2)+3):
        oRow=dot_pos()
        oRow.x=int(vycenter.x+i*spot_Unit*Cos_theta)
        if oRow.x<=img_length:
            oRow.y=int(vycenter.y+i*spot_Unit*Sin_theta)
            fmap.append(oRow)
        else:
            break

    for i in range(1,int(map_Column_cnt/2)+3):  
        oRow=dot_pos()    
        oRow.x=int(vycenter.x-i*spot_Unit*Cos_theta)
        if oRow.x>0:
            oRow.y=int(vycenter.y-i*spot_Unit*Sin_theta)
            fmap.append(oRow)
        else:
            break



map_count=1
for i in fmap:
   # print (i.x,i.y)
    map_count+=1
    # cv2.circle(imgcv,(i.x,i.y),draw_cycle_dia,(0,0,255))
print("==>Map spot Count:", map_count) 
# spott=cdot_map()
# maps=[]
# map_index=0
# for i in map_x:
#     for j in map_y:        
#         spott=cdot_map()
#         spott.num=map_index
#         spott.x=i
#         spott.y=j
#         maps.append(spott)
#         map_index+=1


#check
# for i in maps:
#     cv2.circle(imgcv,(i.x,i.y),draw_cycle_dia,(0,0,255))

#####Distorion 2nd Phase
#Map -->fmap
#all dots--> All_dots
#S2.6 Avoid Redundancy fmap
#check redundancy
rc=0
for i in fmap:
        rct=0
        for j in fmap:
            if i.x==j.x and i.y==j.y:
                rct+=1
        if rct>1:
            rc+=rct
if rc>0:
    print ("?? Redundancy data have been found:",rc)

##2.7 Build RCS (Relative Coordinates System)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2.7.1 Build Dot_RCS center is (0,0) left one is (-1,0) up one is (0,-1)
#cRCS
RCS_Spots=[]
goldenRow=[]
#Setup ZERO position
tr=cRCS()
tr.rcs_x=0
tr.rcs_y=0
tr.x=spot_center_x
tr.y=spot_center_y
RCS_Spots.append(tr)
goldenRow.append(tr)
RCS_Spots_index=0

# Find  center Row
for i in  range(1,int(map_Column_cnt/2)+3):  #find right arrow

    for c in All_dots: 
        tr=cRCS() 
        tr.rcs_y=0  
        #print(i,":",len(RCS_Spots))
        if(detect_direct(RCS_Spots[RCS_Spots_index].x,RCS_Spots[RCS_Spots_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==4 ):
            RCS_Spots_index+=1        
            tr.rcs_x=i
            tr.x=c.x
            tr.y=c.y
            RCS_Spots.append(tr)
            goldenRow.append(tr)
            break

for i in  range(1,int(map_Column_cnt/2)+3):  #find left arrow

    for c in All_dots: 
        tr=cRCS() 
        tr.rcs_y=0  
        #print(i,":",len(RCS_Spots))
        if(i==1):
            if(detect_direct(RCS_Spots[0].x,RCS_Spots[0].y,c.x,c.y,spot_Unit,Sin_theta*2)==3 ):
                RCS_Spots_index+=1        
                tr.rcs_x=-i
                tr.x=c.x
                tr.y=c.y
                RCS_Spots.append(tr)
                goldenRow.append(tr)
                break

        else:
            if(detect_direct(RCS_Spots[RCS_Spots_index].x,RCS_Spots[RCS_Spots_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==3 ):
                RCS_Spots_index+=1        
                tr.rcs_x=-i
                tr.x=c.x
                tr.y=c.y
                RCS_Spots.append(tr)
                goldenRow.append(tr)
                break


           
###Make whole RCS map
for inputc in goldenRow:
    #find column

    # inputc.rcs_x=RCS_Spots[0].rcs_x
    # inputc.rcs_y=RCS_Spots[0].rcs_y
    # inputc.x=RCS_Spots[0].x
    # inputc.y=RCS_Spots[0].y

    for j in range(1,int(map_Row_cnt/2)+3):# down
        for c in All_dots:
            tr=cRCS() 
            tr.rcs_x=inputc.rcs_x 
            #print(i,":",len(RCS_Spots))
            if(j==1):
                if(detect_direct(inputc.x,inputc.y,c.x,c.y,spot_Unit,Sin_theta*2)==2 ):
                    RCS_Spots_index+=1        
                    tr.rcs_y=j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Spots.append(tr)
                    break

            else:
                if(detect_direct(RCS_Spots[RCS_Spots_index].x,RCS_Spots[RCS_Spots_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==2):
                    RCS_Spots_index+=1        
                    tr.rcs_y=j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Spots.append(tr)
                    break

    for j in range(1,int(map_Row_cnt/2)+3): #up
        for c in All_dots:
            tr=cRCS() 
            tr.rcs_x=inputc.rcs_x 
            #print(i,":",len(RCS_Spots))
            if(j==1):
                if(detect_direct(inputc.x,inputc.y,c.x,c.y,spot_Unit,Sin_theta*3)==1 ):
                    RCS_Spots_index+=1        
                    tr.rcs_y=-j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Spots.append(tr)
                    break

            else:
                if(detect_direct(RCS_Spots[RCS_Spots_index].x,RCS_Spots[RCS_Spots_index].y,c.x,c.y,spot_Unit,Sin_theta*3)==1):
                    RCS_Spots_index+=1        
                    tr.rcs_y=-j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Spots.append(tr)
                    break
                         
                        
# # # # #check
# # # for check_point in RCS_Spots:
# # #     cv2.circle(imgcv,(check_point.x,check_point.y),draw_cycle_dia,(0,0,255))
# # #     texts="("+str(check_point.rcs_x)+","+str(check_point.rcs_y)+")"
# # #     cv2.putText(imgcv, texts, (check_point.x,check_point.y), Settings_font, 0.4, (180, 185, 185), 1)

# S2.7.2 Get Whole RCS_map
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#fmap[]
RCS_Map=[]
goldenRow_map=[]
#Setup ZERO position
tr=cRCS()
tr.rcs_x=0
tr.rcs_y=0
tr.x=spot_center_x
tr.y=spot_center_y
RCS_Map.append(tr)
goldenRow_map.append(tr)
RCS_Map_index=0

# Find  center Row
for i in  range(1,int(map_Column_cnt/2)+3):  #find right arrow

    for c in fmap: 
        tr=cRCS() 
        tr.rcs_y=0  
        #print(i,":",len(RCS_Map))
        if(detect_direct(RCS_Map[RCS_Map_index].x,RCS_Map[RCS_Map_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==4 ):
            RCS_Map_index+=1        
            tr.rcs_x=i
            tr.x=c.x
            tr.y=c.y
            RCS_Map.append(tr)
            goldenRow_map.append(tr)
            break

for i in  range(1,int(map_Column_cnt/2)+3):  #find left arrow

    for c in fmap: 
        tr=cRCS() 
        tr.rcs_y=0  
        #print(i,":",len(RCS_SpRCS_Mapots))
        if(i==1):
            if(detect_direct(RCS_Map[0].x,RCS_Map[0].y,c.x,c.y,spot_Unit,Sin_theta*2)==3 ):
                RCS_Map_index+=1        
                tr.rcs_x=-i
                tr.x=c.x
                tr.y=c.y
                RCS_Map.append(tr)
                goldenRow_map.append(tr)
                break

        else:
            if(detect_direct(RCS_Map[RCS_Map_index].x,RCS_Map[RCS_Map_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==3 ):
                RCS_Map_index+=1        
                tr.rcs_x=-i
                tr.x=c.x
                tr.y=c.y
                RCS_Map.append(tr)
                goldenRow_map.append(tr)
                break


           
###Make whole RCS map
for inputc in goldenRow_map:
   ##find column

    # inputc.rcs_x=RCS_Map[0].rcs_x
    # inputc.rcs_y=RCS_Map[0].rcs_y
    # inputc.x=RCS_Map[0].x
    # inputc.y=RCS_Map[0].y

    for j in range(1,int(map_Row_cnt/2)+3):# down
        for c in fmap:
            tr=cRCS() 
            tr.rcs_x=inputc.rcs_x 
            #print(i,":",len(RCS_Map))
            if(j==1):
                if(detect_direct(inputc.x,inputc.y,c.x,c.y,spot_Unit,Sin_theta*2)==2 ):
                    RCS_Map_index+=1        
                    tr.rcs_y=j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Map.append(tr)
                    break

            else:
                if(detect_direct(RCS_Map[RCS_Map_index].x,RCS_Map[RCS_Map_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==2):
                    RCS_Map_index+=1        
                    tr.rcs_y=j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Map.append(tr)
                    break

    for j in range(1,int(map_Row_cnt/2)+3): #up
        for c in fmap:
            tr=cRCS() 
            tr.rcs_x=inputc.rcs_x 
            #print(i,":",len(RCSRCS_Map_Spots))
            if(j==1):
                if(detect_direct(inputc.x,inputc.y,c.x,c.y,spot_Unit,Sin_theta*2)==1 ):
                    RCS_Map_index+=1        
                    tr.rcs_y=-j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Map.append(tr)
                    break

            else:
                if(detect_direct(RCS_Map[RCS_Map_index].x,RCS_Map[RCS_Map_index].y,c.x,c.y,spot_Unit,Sin_theta*2)==1):
                    RCS_Map_index+=1        
                    tr.rcs_y=-j
                    tr.x=c.x
                    tr.y=c.y
                    RCS_Map.append(tr)
                    break
#check
# # for check_point in RCS_Map:
# #     cv2.circle(imgcv,(check_point.x,check_point.y),draw_cycle_dia,(0,0,255))
# #     texts="("+str(check_point.rcs_x)+","+str(check_point.rcs_y)+")"
# #     cv2.putText(imgcv, texts, (check_point.x,check_point.y), Settings_font, 0.4, (180, 185, 185), 1)


#########
##S3 Calculating Distortion
#RCS_Map & RCS_Spots
######
#S3.1 get all distortion
Dt=[]
Dt_v=[]
dbg_count=0
for sp in RCS_Spots:
    tr=cDT()
    tr.rcs_x=sp.rcs_x
    tr.rcs_y=sp.rcs_y
    for pMap in RCS_Map:
        if(sp.rcs_x==pMap.rcs_x) and (sp.rcs_y==pMap.rcs_y):
            if(pMap.x!=spot_center_x)and(pMap.y!=spot_center_y):
                AD=get_distance(spot_center_x,spot_center_y,sp.x,sp.y)
                PD=get_distance(spot_center_x,spot_center_y,pMap.x,pMap.y)
                tr.distortion=(AD-PD)*100/PD
                tr.distortion=abs_value(tr.distortion)
                Dt_v.append(tr.distortion)
                Dt.append(tr)

# Dt.sort(reverse=True)
print(Dt_v)
Dt_v.sort(reverse=True)
Dt_Max=Dt_v[0]

print(">>>>>Distortion Max:",Dt_Max)

for dts in Dt:

    if isValue(dts.distortion,Dt_Max,0.01) :
        px=0
        py=0
        for sp in RCS_Spots:
            if(dts.rcs_x==sp.rcs_x) and (dts.rcs_y==sp.rcs_y):
                px=sp.x
                py=sp.y
                break

        cv2.circle(imgcv,(px,py),draw_cycle_dia,(0,255,0))
        texts="Max <"+str(dts.distortion)+">"
        cv2.putText(imgcv, texts, (px,py), Settings_font, 0.4, (80, 85, 185), 1)

#get avg

dt_avg=Get_Average(Dt_v)
print(">>>>>Distortion AVG:",dt_avg)
cv2.imshow(" ",imgcv)
cv2.waitKey(0) #35   