import cv2
import cvzone
import os
import random
import time
import cvzone.HandTrackingModule as htm

def findNum(list): # find corresponding number to a hand object
    count=list.count(1)
    if count!=1:    # general case
        return count
    elif list.index(1)==0: # thumb is up
        return 6
    else:   # any single finger is up
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
    picList.append(image) # picList contains all pics

detector=htm.HandDetector(detectionCon=0.75)

timer=0
stateResult=False
startGame=False
score=[0,0]


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True, flipType=True)
    blank=cv2.imread(f'{folder_path}/blank.png') # blank stock image

    if startGame: # executes when 's' is pressed
        cv2.putText(img, 'system', (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4)
        cv2.putText(img, 'player', (500, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4)
        # img[:200,:200]=blank

        if stateResult==False:
            timer=time.time()-initialTime
            # game timer
            cv2.putText(img, str(int(timer)), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5) #  right, down

            if timer>3: # only gets executed when time is at 3s
                stateResult=True # do main computation and display stuff
                timer=0 # ready for next itereration

                if hands:
                    hand1=hands[0] # imp
                    listl=detector.fingersUp(hand1)
                    answ=findNum(listl) # answ is actual number
                    # img[:200,-200:]=picList[answ-1]

                    randomNum=random.randint(1,6) # 1 & 6 inclusive
                    imgAI=cv2.imread(f'{folder_path}/{randomNum}.png', cv2.IMREAD_UNCHANGED)
                    img=cvzone.overlayPNG(img, imgAI,(0,0))


    if stateResult: # do this after 3s time frame
        img[:200,-200:]=picList[answ-1] # display user choice
        img=cvzone.overlayPNG(img, imgAI,(0,0)) # display AI choice

        

    # do these always:
    cv2.putText(img, str(score[0]), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5)
    cv2.putText(img, str(score[1]), (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5)
     
    cv2.imshow('image', img)

    key=cv2.waitKey(1)
    if key==ord('q'):
        break
    elif key==ord('s'):
        startGame=True
        initialTime=time.time()
        stateResult=False
