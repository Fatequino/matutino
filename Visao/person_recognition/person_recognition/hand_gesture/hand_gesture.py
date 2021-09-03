import cv2
import mediapipe as mp

import math

###############################################
#Consts fingers names                         #
###############################################
THUMB = "THUMB"
INDEX = "INDEX"
MIDDLE = "MIDDLE"
RING = "RING"
PINKY = "PINKY"
################################################

FINGERS_INDEX = {
    THUMB: [1, 2, 3, 4], #Dedão
    INDEX: [5, 6, 7, 8], #Indicador
    MIDDLE: [9, 10, 11, 12], #Do meio
    RING: [13, 14, 15, 16], #Anelar
    PINKY: [17, 18, 19, 20] #Mindinho
}

def detect_hand(hand_landmarks):

    is_thumb_up = thumb_is_up(hand_landmarks)
    is_index_up = finger_is_up(FINGERS_INDEX[INDEX], hand_landmarks)
    is_middle_up = finger_is_up(FINGERS_INDEX[MIDDLE], hand_landmarks)
    is_ring_up = finger_is_up(FINGERS_INDEX[RING], hand_landmarks)
    is_pinky_up = finger_is_up(FINGERS_INDEX[PINKY], hand_landmarks)

    up = is_index_up and is_middle_up and is_ring_up and is_pinky_up

    return up

    #return image, (not is_thumb_up) and is_middle_up and is_index_up and (not is_ring_up) and (not is_pinky_up)


    # if results.multi_hand_landmarks:

    #     finger_landmarks = results.multi_hand_landmarks[0].landmark

    #     middleFingerMcp = results.multi_hand_landmarks[0].landmark[9]
    #     middleFingerTip = results.multi_hand_landmarks[0].landmark[12]

    #     # if (middleFingerDip.y < middleFingerPip.y and middleFingerTip.y < middleFingerPip.y):
    #         # print("Dedo do meio ta pra cima")
        
    #     middleFingerMcpCoord = draw_circle_landmark(middleFingerMcp, image)
    #     middleFingerTipCoord = draw_circle_landmark(middleFingerTip, image)

    #     is_thumb_up = finger_is_up(FINGERS_INDEX[THUMB], finger_landmarks)
    #     is_index_up = finger_is_up(FINGERS_INDEX[INDEX], finger_landmarks)
    #     is_middle_up = finger_is_up(FINGERS_INDEX[MIDDLE], finger_landmarks)
    #     is_ring_up = finger_is_up(FINGERS_INDEX[RING], finger_landmarks)
    #     is_pinky_up = finger_is_up(FINGERS_INDEX[PINKY], finger_landmarks)

    #     return image, (not is_thumb_up) and is_middle_up and is_index_up and (not is_ring_up) and (not is_pinky_up)

    #     # print(finger_is_up(FINGERS_INDEX["MIDDLE"], finger_landmarks) and finger_is_up(FINGERS_INDEX["INDEX"], finger_landmarks))

    #     # middleFingerTip = results.multi_hand_landmarks[9]
    #     # print(middleFingerTip)
    #     # mp_drawing.draw_landmarks(image, middleFingerTip, mp_hands.HAND_CONNECTIONS)
    #     # for hand_landmarks in results.multi_hand_landmarks:
    #         # print(hand_landmarks)

    # return image, False

def thumb_is_up(finger_landmarks):
    thumb_mcp = finger_landmarks[2]
    index_finger_mcp = finger_landmarks[5]
    return thumb_mcp.x > index_finger_mcp.x
        

def finger_is_up(finger, finger_landmarks):
    mcp_index, pip_index, dip_index = finger[1:]

    return finger_landmarks[mcp_index].y > finger_landmarks[pip_index].y and finger_landmarks[mcp_index].y > finger_landmarks[dip_index].y

def draw_circle_landmark(landmark, image):
    x = math.ceil(landmark.x * 640)
    y = math.ceil(landmark.y * 480)

    cv2.circle(image, (x, y), 6, (255, 0, 0), -1)

    return (x, y)


def calculate_distance(p, q):
    px, py = p
    qx, qy = q

    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))