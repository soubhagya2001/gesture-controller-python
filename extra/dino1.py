#chatgpt rectified but still all functions are not working in pygame

import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import keyboard

detector = HandDetector(detectionCon=0.8, maxHands=2)

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

sleep_duration = 0.1

while True:
    ret, frame = video.read()

    hands, img = detector.findHands(frame, draw=False)

    if hands:
        for hand in hands:
            lmlist = hand["lmList"]
            x10, y10 = lmlist[10][0], lmlist[10][1]
            x20, y20 = lmlist[20][0], lmlist[20][1]
            x4, y4 = lmlist[4][0], lmlist[4][1]
            x8, y8 = lmlist[8][0], lmlist[8][1]
            x12, y12 = lmlist[12][0], lmlist[12][1]
            x5, y5 = lmlist[5][0], lmlist[5][1]

            # Check if hand is open (fingers extended)
            if y12 < y10:
                # Press the space bar
                keyboard.press('space')
                print("space bar pressed")
                keyboard.release('space')
                time.sleep(sleep_duration)
            
            elif abs(x5 - x4) > 70:
                # Press the left arrow key
                keyboard.press('left')
                print("Left arrow key pressed")
                # Release the right arrow key (if pressed before)
                keyboard.release('right')
                time.sleep(sleep_duration)

            # Check if pinky finger is opened (landmark 4 and 8 are above landmark 12)
            elif y10 > y20:
                # Press the right arrow key
                keyboard.press('right')
                print("Right arrow key pressed")
                # Release the left arrow key (if pressed before)
                keyboard.release('left')
                time.sleep(sleep_duration)
            
            else:
                # Release all keys
                keyboard.release('space')
                keyboard.release('right')
                keyboard.release('left')
                time.sleep(sleep_duration)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
