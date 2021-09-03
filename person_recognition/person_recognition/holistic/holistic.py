import cv2
import mediapipe as mp
from .custom_holistic import CustomHolistic

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

custom_holistic = CustomHolistic(min_tracking_confidence = 0.5, min_detection_confidence=0.7)
holistic = mp_holistic.Holistic(min_tracking_confidence = 0.5, min_detection_confidence=0.7, upper_body_only=True)

def process(image):
    results = custom_holistic.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # TODO: Refactor this line
    IMAGE_WIDTH, IMAGE_HEIGHT = len(image[0]), len(image)

    face_five_landmarks = []

    # if results.pose_landmarks:

    #     face_five_landmarks = [
    #         results.pose_landmarks.landmark[3],
    #         results.pose_landmarks.landmark[1],
    #         results.pose_landmarks.landmark[6],
    #         results.pose_landmarks.landmark[4],
    #         results.pose_landmarks.landmark[0]
    #     ]

    #     face_five_landmarks = [
    #         (int(landmark.x * IMAGE_WIDTH), int(landmark.y * IMAGE_HEIGHT)) for landmark in face_five_landmarks
    #     ]            
    face_region = None

    if results.face_roi_from_pose:

        roi = results.face_roi_from_pose
        x_center, y_center = roi.x_center, roi.y_center
        width, height = roi.width, roi.height

        x = int((x_center - (width / 2)) * IMAGE_WIDTH)
        y = int((y_center - (height / 2)) * IMAGE_HEIGHT)
        
        xf = x + int(roi.width * IMAGE_WIDTH)
        yf = y + int(roi.height * IMAGE_HEIGHT)

        cv2.rectangle(image, (x, y), (xf, yf), (255, 0, 0), 2)

        face_region = {
            'x': x,
            'y': y,
            'xf': xf,
            'yf': yf
        }

    # if results.face_roi_from_pose:
    #     # print(results.face_roi_from_pose)

    #     roi = results.face_roi_from_pose

    #     x_center, y_center = roi.x_center, roi.y_center

    #     width, height = roi.width * 640, roi.height * 480
    #     width, height = int(width / 2), int(height / 2)

    #     xi = int(x_center * 640) - width
    #     yi = int(y_center * 480) - height

    #     xf = xi + int(roi.width * 640.0)
    #     yf = yi + int(roi.height * 480.0)

    #     cv2.rectangle(image, (xi, yi), (xf, yf), (255, 0, 0), 2)

    #     # cv2.circle(image, (xi, yi), 6, (255, 0, 0), -1)

    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    # if results.right_hand_landmarks:
    #     mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
    #if results.pose_landmarks:
        # mp_drawing.draw_landmarks(
        #     image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        # mp_drawing.draw_landmarks(
            # image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        # mp_drawing.draw_landmarks(
            # image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # print(results.pose_landmarks)
        #mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.UPPER_BODY_POSE_CONNECTIONS) #Version 0.8.3.1 required

    return image, (results.left_hand_landmarks, ), face_region, face_five_landmarks