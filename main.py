import cv2
import mediapipe as mp
import random
import time

# Initialize Mediapipe Hands (FAST MODE)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0     # SPEED BOOST
)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)   # smoother frames
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Finger tip landmarks
FINGER_TIPS = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    """Count opened fingers (FAST + STABLE)"""
    lm = hand_landmarks.landmark
    fingers = []

    # Thumb
    if lm[4].x < lm[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip in [8, 12, 16, 20]:
        if lm[tip].y < lm[tip - 2].y - 0.02:  # stability margin
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

def get_gesture(fingers):
    """Map finger count to gestures"""
    if fingers == 0:
        return "Rock"
    elif fingers == 2:
        return "Scissors"
    elif fingers == 5:
        return "Paper"
    return "Unknown"

def decide_winner(player, computer):
    if player == computer:
        return "Draw"
    if (player == "Rock" and computer == "Scissors") or \
       (player == "Paper" and computer == "Rock") or \
       (player == "Scissors" and computer == "Paper"):
        return "You Win!"
    return "Computer Wins!"

last_action_time = 0
COOLDOWN = 0.5  # faster response

player_choice = "None"
computer_choice = "None"
winner = "None"

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # natural mirror
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)
    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = count_fingers(hand_landmarks)
            gesture = get_gesture(finger_count)

            if gesture in ["Rock", "Paper", "Scissors"] and (current_time - last_action_time > COOLDOWN):
                player_choice = gesture
                computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                winner = decide_winner(player_choice, computer_choice)
                last_action_time = current_time

    # Display results
    cv2.putText(img, f"Player: {player_choice}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(img, f"Computer: {computer_choice}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.putText(img, f"Result: {winner}", (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,255), 3)

    cv2.imshow("Rock Paper Scissors - FAST MODE", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
