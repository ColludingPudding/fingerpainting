import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

folderPath = "C:/Users/naoh1/Downloads/Header"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f"{folderPath}/{imPath}")
    overlayList.append(image)


header = overlayList[0]
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detection_confidence=0.85)
xp = 0
yp = 0

imgCanvas = np.zeros((720,1280,3),np.uint8)

while True:
    
    #Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find Hand Landmark
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)

    if len(lmList) != 0:

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()

        # Selection mode - 2 fingers
        brushsize = 20
        color = (255,0,0)
        if fingers[1] and fingers[2]:
            if y1<125: 
                if 250 < x1 < 450:
                    header = overlayList[1]
                    
                    pencil_color = (0,0,0)
                elif 550 < x1 < 750:
                    header = overlayList[2]

                elif 800 < x1 < 950:
                    header = overlayList[3]
                elif 1050 < x1 < 1200:
                    header = overlayList[4]
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,0,255),cv2.FILLED)
        # Drawing mode - index
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)


            xp, yp = x1, y1
            
            cv2.line(img, (xp, yp), (x1,y1), color,brushsize)
            cv2.line(imgCanvas, (xp, yp), (x1,y1), color,brushsize)
    # Setting header image
    img[0:125, 0:1280] = header
    cv2.imshow("Image",img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)