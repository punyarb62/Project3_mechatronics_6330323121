import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(1)  # Adjust as necessary

# Define the target screen resolution
target_screen_width, target_screen_height = 1920, 1080

# Gesture control variables
pinch_last_time = 0
gesture_cooldown = 2  # 2 seconds for gesture cooldown
scroll_active = False
last_scroll_time = 0

def calculate_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5

while True:
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Mouse movement
            hand_center_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
            hand_center_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            mouse_x = int(hand_center_x * target_screen_width)
            mouse_y = int(hand_center_y * target_screen_height)
            pyautogui.moveTo(mouse_x, mouse_y)

            current_time = time.time()

            # Left Click (hold for drag)
            if calculate_distance(thumb_tip, index_tip) < 0.02 and current_time - pinch_last_time > gesture_cooldown:
                pyautogui.click(button='left')
                pinch_last_time = current_time
                cv2.putText(image, 'Left click', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Right Click
            if calculate_distance(thumb_tip, middle_tip) < 0.02 and current_time - pinch_last_time > gesture_cooldown:
                pyautogui.click(button='right')
                pinch_last_time = current_time
                cv2.putText(image, 'Right Click', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Continuous Scrolling
            if calculate_distance(thumb_tip, ring_tip) < 0.02:
                if not scroll_active or current_time - last_scroll_time > 0.1:
                    pyautogui.scroll(-80)
                    scroll_active = True
                    last_scroll_time = current_time
                cv2.putText(image, 'Scrolling Down', (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            elif calculate_distance(thumb_tip, pinky_tip) < 0.02:
                if not scroll_active or current_time - last_scroll_time > 0.1:
                    pyautogui.scroll(80)
                    scroll_active = True
                    last_scroll_time = current_time
                cv2.putText(image, 'Scrolling Up', (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                scroll_active = False

    cv2.imshow('Virtual Mouse', image)
    if cv2.waitKey(5) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
