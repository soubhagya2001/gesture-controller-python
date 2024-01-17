import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # Create a white screen at the bottom 20% of the frame
    height, width, _ = frame.shape
    white_screen = frame.copy()
    white_screen[int(0.8 * height):, :] = (255, 255, 255)

    # Display the heading on the white screen
    heading_text = "Show your hand , move hand to move cursor"
    cv2.putText(
        white_screen, heading_text, (10, int(0.9 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA
    )
    
    # Display description under the heading
    description_text = "close fist for left click , Press 'esc' to close"
    cv2.putText(
        white_screen, description_text, (10, int(0.95 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA
    )

    if hands:
        for hand in hands:
            # drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                    pyautogui.moveTo(index_x, index_y)

                if id == 10:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))
                    mFinger_x = screen_width / frame_width * x
                    mFinger_y = screen_height / frame_height * y

                  
                    if mFinger_y > thumb_y:
                        pyautogui.mouseDown(button='left')
                    else:
                        pyautogui.mouseUp(button='left')


    # Display the white screen with heading and description
    frame = cv2.addWeighted(frame, 1, white_screen, 0.7, 0)

    cv2.imshow('Virtual Mouse', frame)

    # Check for the 'Esc' key press
    key = cv2.waitKey(1)
    if key == 27:  # 27 is the ASCII code for 'Esc'
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
