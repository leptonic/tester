import cv2

def Capture(pathstr):
    cap=cv2.VideoCapture(0)
    i=0
    # while(1):
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(1, 10.0)
    ret ,frame = cap.read()

    k=cv2.waitKey(1)
    #path='C:/Users/YY/Desktop/photos/'
    cv2.imwrite(pathstr+'1.jpg',frame)

    cap.release()
    # cv2.destroyAllWindows()

# cv2.imwrite("C:\\Users\\YY\\Desktop\\photos\\fangjian2.jpeg", frame)
# cap.release()
# cv2.destroyAllWindows()
