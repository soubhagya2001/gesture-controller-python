

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

    # white screen at the bottom 20% of the frame
    height, width, _ = frame.shape
    white_screen = frame.copy()
    white_screen[int(0.8 * height):, :] = (0, 0, 0)


    heading_text = "Show closed fist, open thumb for right, open little finger for left"
    cv2.putText(
        white_screen, heading_text, (10, int(0.9 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA
    )
    
    
    description_text = "open fist for spacebar , Press 'q' to close"
    cv2.putText(
        white_screen, description_text, (10, int(0.95 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA
    )

    if hands:
        for hand in hands:
            lmlist = hand["lmList"]
            x10, y10 = lmlist[10][0], lmlist[10][1]
            x20, y20 = lmlist[20][0], lmlist[20][1]
            x4, y4 = lmlist[4][0], lmlist[4][1]
            x8, y8 = lmlist[8][0], lmlist[8][1]
            x12, y12 = lmlist[12][0], lmlist[12][1]
            x5, y5 = lmlist[5][0], lmlist[5][1]
            x0, y0 = lmlist[0][0], lmlist[0][1]

            # Check if hand is open (fingers extended)
            if y12 < y10:
           
                keyboard.press('up')
                print("up button pressed")
                
                time.sleep(sleep_duration)
                keyboard.release('up')
            
            elif abs(x5 - x4) > 70:
             
                keyboard.press('left')
                print("Left arrow key pressed")
             
                
                time.sleep(sleep_duration)
                keyboard.release('left')

   
            elif y10 > y20:
               
                keyboard.press('right')
                print("Right arrow key pressed")
               
                keyboard.release('right')
                time.sleep(sleep_duration)

            elif y12 > y0:
                keyboard.press('down')
                print('Down button pressed')
                keyboard.release('down')
                time.sleep(sleep_duration)
            
            else:
                
                keyboard.release('space')
                keyboard.release('right')
                keyboard.release('left')
                keyboard.release('down')
                time.sleep(sleep_duration)

    # Display the white screen with heading and description
    frame = cv2.addWeighted(frame, 1, white_screen, 1.5, 0)

    cv2.imshow("Runner", frame) 
    k = cv2.waitKey(1) 
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
