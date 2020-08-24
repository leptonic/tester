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
        
 
def ispos(ix,sx,iy,sy,xdmv,ydmv):
    if ix<(sx+xdmv) and ix>(sx-xdmv):
        if iy<(sy+ydmv) and iy>(sy-ydmv):
            return True
        else:
            return False
    else:
        return False       