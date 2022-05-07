import cv2
import dlib
import numpy as np

#-------------------------------------------
# getting the facial points for reference
#-------------------------------------------

def shape_to_np(shape,dtype="int"):
    coords=np.zeros((68,2),dtype=dtype)
    for i in range(68):
        coords[i]=(shape.part(i).x,shape.part(i).y)
    return coords

def eyeOnMask(mask,side):
    points=[shape[i] for i in side]
    points=np.array(points,dtype=np.int32)
    mask=cv2.fillConvexPoly(mask,points,255)
    return mask

def contouring(thresh,mid,img,right=False):
    cnts,_=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    try:
        cnt=max(cnts,key=cv2.contourArea)
        M=cv2.moments(cnt)
        cx=int(M['m10']/M['m00'])
        cy=int(M['m01']/M['m00'])
        if right:
            cx+=mid
            cv2.circle(img,(cx,cy),4,(0,0,255),2)
    except:
        pass

predictor=dlib.shape_predictor("shape_68.dat")



leftEye=[i for i in range(36,42)]
rightEye=[i for i in range(42,48)]

#----------------------------------------
# getting video feed from camera
#----------------------------------------

cap=cv2.VideoCapture(0)

while(True):

    ret, img=cap.read()
    thresh=img.copy()

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    detector=dlib.get_frontal_face_detector()
    rects=detector(gray)

    for rect in rects:
        shape=predictor(gray,rect)
        shape=shape_to_np(shape)
#---------------------------------------
# finding center of the eyeball
#---------------------------------------

        mask=np.zeros(img.shape[:2],dtype=np.uint8)
        mask=eyeOnMask(mask,leftEye)
        mask=eyeOnMask(mask,rightEye)

        kernel = np.ones((9,9),np.uint8)
        mask=cv2.dilate(mask,kernel,5)
        eyes=cv2.bitwise_and(img,img,mask=mask)
        mask=(eyes == [0,0,0]).all(axis=2)
        eyes[mask]=[255,255,255]
        eyesGray=cv2.cvtColor(eyes,cv2.COLOR_BGR2GRAY)

        _,thresh=cv2.threshold(eyesGray,38,255,cv2.THRESH_BINARY)
        #thresh=cv2.erode(thresh,None,iterations=2)
        #thresh=cv2.dilate(thresh,None,iterations=4)
        thresh=cv2.medianBlur(thresh,3)

        mid=(shape[42][0]+shape[39][0])//2
        thresh=cv2.bitwise_not(thresh)
        contouring(thresh[:0:mid],mid,img)
        contouring(thresh[:,mid:],mid,img,True)

#------------------------------------------
# showing the result
#------------------------------------------

    cv2.imshow("eyes",img)
    cv2.imshow("image",thresh)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
