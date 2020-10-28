
# import cv2
# import numpy as np
# fd = open(r"C:\workspace\Raw\f50.bin", 'rb')
# rows =3040 # 3040
# cols =4056 # 4096
# f = np.fromfile(fd, dtype=np.uint16,count=rows*cols)
# im = f.reshape((rows, cols)) #notice row, column format

# cv2.imwrite('./f502.bmp', im)
# fd.close()

# # # # import cv2
# # # # import numpy as np
# # # # fd = open(r"C:\workspace\Raw\f50.bin", 'rb')
# # # # rows =3040 # 3040
# # # # cols =4056 # 4096
# # # # f = np.fromfile(fd, dtype=np.uint16,count=rows*cols)
# # # # im = f.reshape((rows, cols)) #notice row, column format

# # # # cv2.imwrite('./f502.bmp', im)
# # # # fd.close()

import cv2
from PIL import Image as im
import numpy as np  

class pyOpenCvTest():


    rawPath = r"C:\workspace\Raw\RAW_0Rl.bin"
    imgSize =(3040,4056) #(3040,4056)#(3072,4096) # (2160,4096)
    def cvTest():
        
        #step1：
        rawData = np.fromfile(pyOpenCvTest.rawPath,dtype = 'uint16')
        print(np.shape(rawData)) #12330240
        
        #step2：
        reshapeRawData = np.reshape(rawData,pyOpenCvTest.imgSize)


        # BRGB = cv2.cvtColor(reshapeRawData, cv2.COLOR_BayerBG2RGB )
        img_test2 = cv2.resize(reshapeRawData, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        sPic = np.zeros(img_test2.shape, dtype=np.uint16)
        print("--check size")
        print(reshapeRawData.shape[0])
        print(reshapeRawData.shape[1])
        print("--")
        print(img_test2.shape[0])
        print(img_test2.shape[1])
        print("--over")


        for i in range(reshapeRawData.shape[0]-1):
            if i%2==0 :
                continue

            for j in range(reshapeRawData.shape[1]-1):
                if j%2==0:
                    continue
                ii=int((i+1)/4)
                jj=int((j+1)/4)               
                if ii<img_test2.shape[0] and jj<img_test2.shape[1]:                       
                    sPic[ii][jj]=reshapeRawData[i][j]
                else:
                    print("Error:67")
                    print(ii,jj)

        # cv2.mixChannels([reshapeRawData], [hue], [0,0])
        # r= cv2.split(reshapeRawData)
        
        # print(r)
        # 
        # step3：
       

        # for i in range(reshapeRawData.shape[0]):            
        #     for j in range(reshapeRawData.shape[1]):
        #         val=reshapeRawData[i][j]
        #         print(val)
                # val = np.round(reshapeRawData[i][j] >> 2)
                # if val >= 255:
                #     reshapeRawData[i][j] = 255
                # elif val <= 0:
                #     reshapeRawData[i][j] = 0
                # else:
                #     reshapeRawData[i][j] = val

        # img_test2 = cv2.resize(reshapeRawData, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
            
      #  cv2.imwrite('./f502.png', reshapeRawData,[cv2.IMWRITE_PNG_COMPRESSION, 0])

        print("stest")
        cv2.imwrite('./fg.bmp', sPic)
        # print(reshapeRawData.max())#200
        # print(reshapeRawData.min())#3

        # img = im.fromarray(reshapeRawData)
     
        # img.show()

pyOpenCvTest.cvTest()