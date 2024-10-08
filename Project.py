
import cv2
import mediapipe as mp
import time 


#mediapipe solution -->hands or drawing_utils-->Hands(specifications)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


landmark_color = (255,0,0)          
connection_color = (255,255,0)       


cap = cv2.VideoCapture(0)

while cap.isOpened():   
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.flip(frame, 1)

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Process the image with MediaPipe
    results = hands.process(image_rgb)

    left_hand_detected = False
    right_hand_detected = False

    #Draw landmarks and connections if hands are detected
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness): # type: ignore

            #Determine handedness (left or right)
            if handedness.classification[0].label == 'Left':
                handedness_str = 'Left Hand Detected'
                left_hand_detected = True
            elif handedness.classification[0].label == 'Right':
                handedness_str = 'Right Hand Detected'
                right_hand_detected = True

            #Draw landmarks with custom colors and thickness
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                      landmark_drawing_spec=mp_drawing.DrawingSpec(color=landmark_color, thickness=3, circle_radius=4),
                                      connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=3))

            # Draw landmark numbers with custom font and style
            for idx, landmark in enumerate(hand_landmarks.landmark):    
                h, w, c = frame.shape  
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.putText(frame, str(idx), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

    #Display hand detection messages
    if left_hand_detected and right_hand_detected:
        cv2.putText(frame, 'Both Hands Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
    elif left_hand_detected:
        cv2.putText(frame, 'Left Hand Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    elif right_hand_detected:
        cv2.putText(frame, 'Right Hand Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

        

    #### current time ####
    current_time = time.strftime('%H:%M:%S')
    cv2.putText(frame, f'Time: {current_time}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    
    cv2.imshow('Hand Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):    
        break

cap.release()
cv2.destroyAllWindows()
