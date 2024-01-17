import cv2
from cvzone.HandTrackingModule import HandDetector
import keyboard

detector = HandDetector(detectionCon=0.8, maxHands=2)

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    # Create a white screen at the bottom 20% of the frame
    height, width, _ = frame.shape
    white_screen = frame.copy()
    white_screen[int(0.8 * height):, :] = (0, 0, 0)

    # Display the heading on the white screen
    heading_text = "Show hand in car steering holding form , show left thumb for brake ,"
    cv2.putText(
        white_screen, heading_text, (10, int(0.9 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
    )
    
    # Display description under the heading
    description_text = "right thumb for accelerator , Press 'q' to close"
    cv2.putText(
        white_screen, description_text, (10, int(0.95 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA
    )


    # Find hands in the frame
    hands, img = detector.findHands(frame,draw=False)

    if len(hands) >= 2:
        # Sort hands based on x-coordinate of landmark 10
        hands.sort(key=lambda hand: hand["lmList"][10][0])

        left_hand = hands[0]
        right_hand = hands[1]

        left_y10 = left_hand["lmList"][10][1]
        right_y10 = right_hand["lmList"][10][1]

        thumb_open = (right_hand["lmList"][6][1] - right_hand["lmList"][3][1]) > 60
        if thumb_open:
            keyboard.press('up')
            print("Up button pressed")
        else:
            keyboard.release('up')

        left_thumb_open = (left_hand["lmList"][6][1] - left_hand["lmList"][3][1]) > 60
        if left_thumb_open:
            keyboard.press('down')
            print("Down button pressed")
        else:
            keyboard.release('down')

        if (right_y10 - left_y10) > 110:
            keyboard.press('right')
            print("Right button clicked")
        else:
            keyboard.release('right')

        if (left_y10 - right_y10) > 150:
            keyboard.press('left')
            print("Left button pressed")
        else:
            keyboard.release('left')

    else:
        keyboard.release('left')
        keyboard.release('right')
        keyboard.release('up')
        keyboard.release('down')

    # Display the white screen with heading and description
    frame = cv2.addWeighted(frame, 1, white_screen, 1, 0)

    cv2.imshow("Steering", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all windows
video.release()
cv2.destroyAllWindows()
