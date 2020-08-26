
#encoding:utf-8
'''
Created on 2020 August 25th
@author: Yb
'''
 
import os
import  time
 
def run_imtf(sn,num): 
    Settings_imtf="imtf.exe "
    Settings_out_path="C:\\dotchart\\f4f6\\output\\"


    cmd=Settings_imtf+Settings_out_path+"S"+str(sn)+"_"+str(num)+".bmp"

    acmd = os.popen(cmd)
    contents = acmd.read()
    words = contents.split()
    result=words[5]
    strs=cmd+" : "+result
    # print(strs)
    return result
# os.system(cmd)
#os.system('ping 192.168.1.1')

 
 
