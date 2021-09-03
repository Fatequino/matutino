import face_recognition
import numpy as np

import person_recognition.api as api

import pickle

from pathlib import Path

import time

import dlib
import face_recognition_models

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

known_face_encodings = []
known_face_ids = []
clf = None

content = None

path_trained_data = Path(__file__).parent.parent.parent.joinpath('data', 'face_trained.data')

with open(path_trained_data, 'rb') as f:
    content = pickle.load(f)

if content is not None:
    known_face_encodings = content['input']
    known_face_ids = content['output']
    # clf = content['clf']


def recognize_face(image, face_region, face_five_landmarks):
    if len(known_face_encodings) == 0:
        return "Not found"

    # start = time.clock()
    face_roi = image[face_region['y']:face_region['yf'], face_region['x']:face_region['xf']]

    # face_locations = face_recognition.face_locations(face_roi)
    # print(face_locations)
    

    # print(help(face_encoder.compute_face_descriptor))

    # print(type(face_roi))

    # rect = dlib.rectangle(face_region['x'], face_region['y'], face_region['xf'], face_region['yf'])
    # dlib_face_landmarks = [dlib.point(landmark[0], landmark[1]) for landmark in face_five_landmarks]

    # dlib_full_face_detection = dlib.full_object_detection(rect, dlib_face_landmarks)

    # face_encodings = np.array(face_encoder.compute_face_descriptor(face_roi, dlib_full_face_detection, 1))
    face_encodings = face_recognition.face_encodings(face_roi)

    # print(time.clock() - start)
    # start = time.clock()
    if len(face_encodings) == 0: #Nenhuma face encontrada
        return ""


    matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
    face_name = None
    # print(time.clock() - start)
    if True in matches:
        match_index = matches.index(True)
        face_idx = known_face_ids[match_index]
        face_name = api.get_face_detail(int(face_idx))
        print(face_name)

    return face_name

    # face_unkown_encoding = face_recognition.face_encodings(face_roi, face_locations)[0]

    # matches = face_recognition.compare_faces(known_face_encodings=known_face_encodings, face_encoding_to_check=face_unkown_encoding)
    
    # face_distances = face_recognition.face_distance(face_encodings=known_face_encodings, face_to_compare=face_unkown_encoding)
    # best_match_index = np.argmin(face_distances)

    # face_name = None

    # if matches[best_match_index]:
    #     face_index = known_face_ids[best_match_index]
    #     face_name = api.get_face_detail(int(face_index))

    # return face_name