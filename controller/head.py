import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    #white screen at the bottom 20% of the frame
    height, width, _ = frame.shape
    white_screen = frame.copy()
    white_screen[int(0.8 * height):, :] = (0, 0, 0)

  
    heading_text = "Move head to move cursor, blink left eye for left click"
    cv2.putText(
        white_screen, heading_text, (10, int(0.9 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2, cv2.LINE_AA
    )
    
    
    description_text = "Blink right eye for right click , Press 'esc' to close"
    cv2.putText(
        white_screen, description_text, (10, int(0.95 * height)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2, cv2.LINE_AA
    )
    
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)
        
        right_eye_landmarks = [landmarks[362], landmarks[363], landmarks[374], landmarks[380], landmarks[381], landmarks[382]]
        right_eye_aspect_ratio = (right_eye_landmarks[1].y + right_eye_landmarks[2].y + right_eye_landmarks[3].y) / 3.0
        if (abs(right_eye_landmarks[5].y - right_eye_landmarks[1].y)) < 0.02:
            pyautogui.rightClick()
            #print(right_eye_landmarks[5].y - right_eye_landmarks[1].y)
            pyautogui.sleep(1)
        
        left_eye_landmarks = [landmarks[145], landmarks[159]]
        for landmark in left_eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.02:
            #print(left_eye_landmarks[0].y - left_eye_landmarks[1].y)
            pyautogui.click()
            pyautogui.sleep(1)


    
    frame = cv2.addWeighted(frame, 1, white_screen, 0.7, 0)

    cv2.imshow('Head Controlled Mouse', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break  # Break the loop when the 'Esc' key is pressed

cam.release()
cv2.destroyAllWindows()
