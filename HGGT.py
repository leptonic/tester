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
def get_Min_value(data):
    min_v=data[0]
    for p in data:
        if p<min_v:
            min_v=p
    return min_v
