import cv2
import mediapipe as mp
import pyautogui
import random
import util
import numpy as np
from pynput.mouse import Button, Controller
mouse = Controller()

# Screen setup
screen_width, screen_height = pyautogui.size()

# Mouse smoothing parameters
SMOOTHING_FACTOR = 0.5  # Adjusts how smooth the motion is (0-1)
SCALING_FACTOR = 1.2    # Adjusts the sensitivity of mouse movement
DEADZONE = 5           # Minimum pixel movement required
prev_x, prev_y = 0, 0  # Previous mouse position

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None


def move_mouse(index_finger_tip):
    global prev_x, prev_y
    
    if index_finger_tip is not None:
        # Calculate raw coordinates
        raw_x = int(index_finger_tip.x * screen_width)
        raw_y = int(index_finger_tip.y / 2 * screen_height)
        
        # Apply smoothing using exponential moving average
        smooth_x = int(SMOOTHING_FACTOR * raw_x + (1 - SMOOTHING_FACTOR) * prev_x)
        smooth_y = int(SMOOTHING_FACTOR * raw_y + (1 - SMOOTHING_FACTOR) * prev_y)
        
        # Calculate movement delta
        delta_x = abs(smooth_x - prev_x)
        delta_y = abs(smooth_y - prev_y)
        
        # Only move if movement exceeds deadzone
        if delta_x > DEADZONE or delta_y > DEADZONE:
            # Apply scaling factor for more precise control
            dx = (smooth_x - prev_x) * SCALING_FACTOR
            dy = (smooth_y - prev_y) * SCALING_FACTOR
            
            # Get current mouse position and apply relative movement
            current_x, current_y = pyautogui.position()
            target_x = int(current_x + dx)
            target_y = int(current_y + dy)
            
            # Ensure coordinates stay within screen bounds
            target_x = max(0, min(target_x, screen_width))
            target_y = max(0, min(target_y, screen_height))
            
            # Move the mouse
            pyautogui.moveTo(target_x, target_y)
            
            # Update previous position
            prev_x, prev_y = smooth_x, smooth_y


def is_left_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50
    )


def is_right_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90  and
            thumb_index_dist > 50
    )


def is_double_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist > 50
    )


def is_screenshot(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist < 50
    )


def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:

        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if util.get_distance([landmark_list[4], landmark_list[5]]) < 50  and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list,  thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list,thumb_index_dist ):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
