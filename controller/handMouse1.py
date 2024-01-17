from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui

cap = cv2.VideoCapture(0)
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
screen_width, screen_height = pyautogui.size()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False, flipType=False)
    frame_height, frame_width, _ = img.shape

    #  white screen at the bottom 20% of the frame
    height, width, _ = img.shape
    white_screen = img.copy()
    white_screen[int(0.8 * height):, :] = (0, 0, 0)

    
    heading_text = "use right hand to move cursor , left hand for clicking"
    cv2.putText(
        white_screen, heading_text, (10, int(0.9 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
    )
    
    
    description_text = "Touch thumb & little finger for left , thumb & index finger for right click"
    cv2.putText(
        white_screen, description_text, (10, int(0.95 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
    )


    if hands:
        right_hand = None
        left_hand = None

        for hand in hands:
            if hand["type"] == "Right":
                right_hand = hand
            elif hand["type"] == "Left":
                left_hand = hand

        if right_hand:
            
            x, y = right_hand["lmList"][8][0], right_hand["lmList"][8][1]
            index_x = int(screen_width * (x / frame_width))
            index_y = int(screen_height * (y / frame_height))
            pyautogui.moveTo(index_x, index_y)

        if left_hand:
            # Check if the left fist is closed and left click
            # if detector.fingersUp(left_hand).count(1) == 0:
            #     pyautogui.leftClick()

            # Check if landmarks 4 and 8 of the left hand are touched and right click
            point4 = left_hand["lmList"][4]
            point8 = left_hand["lmList"][8]
            point20 = left_hand["lmList"][20]

            if point4 and point8:
                # distance = ((point4[0] - point8[0]) ** 2 + (point4[1] - point8[1]) ** 2) ** 0.5
                distance = point4[0] - point8[0]
                if distance < 20:
                    pyautogui.rightClick()
                # if distance < 30:
                #     pyautogui.rightClick()
                    
            if point4 and point20:
                distance = point4[0] - point20[0]
                if distance < 20:
                    pyautogui.leftClick()

   
    frame = cv2.addWeighted(img, 1, white_screen, 1, 0)
    cv2.imshow("Hand Mouse", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
