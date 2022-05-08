
import cv2
import numpy as np
import face_recognition
import os

path = 'Images'
imag = []
clsNames = []
myList = os.listdir(path)
print (myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    imag.append(curImg)
    clsNames.append(os.path.splitext(cl)[0])

print (clsNames)

def findEncodings(imag):
    encodeList = []
    for img in imag:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeFac = face_recognition.face_encodings(img)[0]
        encodeList.append(encodeFac)
    return encodeList

encodeListKnown = findEncodings(imag)
print ('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)

    for encodeFac,FacLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFac)
        facDis = face_recognition.face_distance(encodeListKnown, encodeFac)

        matchIndex = np.argmin(facDis)
        print(facDis)

        if matches[matchIndex]:
            name = clsNames[matchIndex].upper()
            print (name)
            y1,x2,y2,x1= FacLoc
            y1,x2,y2,x1 = y1*4, x2*4 , y2*4 , x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 255),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
        else:
            print('Unknown')
            y1, x2, y2, x1 = FacLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 255), cv2.FILLED)
            cv2.putText(img, 'Unknown', (x1 + 6, y2 - 6), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)



        cv2.imshow('Webcam',img)
        cv2.waitKey(1)






    




