import cv2
import os
import cvzone.HandTrackingModule as htm

def findNum(list): # find corresponding number to a hand object
    count=list.count(1)
    if count!=1:
        return count
    elif list.index(1)==0:
        return 6
    else:
        return 1

wCam, hCam = 740, 580
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folder_path='num_pic'
pic_name_list=os.listdir(folder_path)
picList=[]
for imPath in pic_name_list:
    image=cv2.imread(f'{folder_path}/{imPath}')
    picList.append(image)

detector=htm.HandDetector(detectionCon=0.75)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)
    
    if hands:
        hand1=hands[0] # imp
        listl=detector.fingersUp(hand1)
        answ=findNum(listl)
        img[:200,:200]=picList[answ-1]
    
    cv2.imshow('image', img)
    if cv2.waitKey(1)==ord('q'):
        break
