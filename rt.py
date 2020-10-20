
import cv2
import numpy as np
fd = open(r"C:\workspace\Raw\f50.bin", 'rb')
rows =3040 # 3040
cols =4056 # 4096
f = np.fromfile(fd, dtype=np.uint16,count=rows*cols)
im = f.reshape((rows, cols)) #notice row, column format

cv2.imwrite('./f50.bmp', im)
fd.close()

# import cv2
# from PIL import Image as im
# import numpy as np  

# class pyOpenCvTest():


#     rawPath = r"C:\workspace\Raw\RAW.bin"
#     imgSize = (3040,4056)#(3072,4096) # (2160,4096)
#     def cvTest():
        
#         #step1：
#         rawData = np.fromfile(pyOpenCvTest.rawPath,dtype = 'uint16')
#         print(np.shape(rawData)) #1920000
        
#         #step2：
#         reshapeRawData = np.reshape(rawData,pyOpenCvTest.imgSize)

#         #step3：
#         for i in range(reshapeRawData.shape[0]):
#             for j in range(reshapeRawData.shape[1]):
#                 #将10bit数转成8bit
#                 val = np.round(reshapeRawData[i][j] >> 2)
#                 if val >= 255:
#                     reshapeRawData[i][j] = 255
#                 elif val <= 0:
#                     reshapeRawData[i][j] = 0
#                 else:
#                     reshapeRawData[i][j] = val

#         print(reshapeRawData.max())#200
#         print(reshapeRawData.min())#3

#         img = im.fromarray(reshapeRawData)
     
#         img.show()
# print("stest")
# pyOpenCvTest.cvTest()