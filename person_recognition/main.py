import cv2

import person_recognition.hand_gesture as hand_gesture
import person_recognition.holistic as holistic
import person_recognition.face_processing as face_processing

import time

capture = cv2.VideoCapture(1)
width  = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

font = cv2.FONT_HERSHEY_SIMPLEX

skip_processing_frame = False

while capture.isOpened():
    success, image = capture.read()
    image = cv2.flip(image, 1)

    if not success: # Empty camera frame - ignore
        continue
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # With writeable False can improve performance, because it will pass by reference
    image.flags.writeable = False

    image, hands_landmarks, face_region = holistic.process(image)
    for hand_landmark in hands_landmarks:
        if hand_landmark:
            finger_is_up = hand_gesture.detect_hand(hand_landmark.landmark)

            if finger_is_up and face_region is not None:
                face_name = face_processing.recognize_face(image, face_region)
                cv2.putText(image, face_name, (face_region['x'] - 50, height - 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow('Debug - Centralizer', small_image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

capture.release()