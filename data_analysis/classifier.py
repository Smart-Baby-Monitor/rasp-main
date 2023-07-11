# -*- coding: utf-8 -*-

import argparse
import json
import os
import pickle
import sys
import warnings
from data_analysis import Reader
import cv2
import numpy as np
from data_analysis.baby_cry_predictor import BabyCryPredictor
from data_analysis.feature_engineer import FeatureEngineer

# egg_path = '{}/../lib/baby_cry_detection-1.1-py2.7.egg'.format(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(egg_path)

# from data_analysis.reader import Reader
# from data_analysis.baby_cry_predictor import BabyCryPredictor
# from data_analysis.feature_engineer import FeatureEngineer
# from data_analysis.majority_voter import MajorityVoter


def classify_audio(audio_file_path):

    # Initializations - Getting different paths 
        
    load_path_model = os.path.normpath('{}/model/'.format(os.path.dirname(os.path.abspath(__file__))))
    save_path = os.path.normpath('{}/prediction/'.format(os.path.dirname(os.path.abspath(__file__))))
    
    # Read audio signal
    file_reader = Reader(os.path.join(audio_file_path))
    play_list = file_reader.read_audio_file()

    
    # iterate on play_list for feature engineering and prediction
    # FEATURE ENGINEERING
    # Feature extraction
    engineer = FeatureEngineer()

    play_list_processed = list()

    for signal in play_list:
        tmp = engineer.feature_engineer(signal)
        play_list_processed.append(tmp)

    # MAKE PREDICTION
    # https://stackoverflow.com/questions/41146759/check-sklearn-version-before-loading-model-using-joblib
    with warnings.catch_warnings():
      warnings.simplefilter("ignore", category=UserWarning)

      with open((os.path.join(load_path_model, 'model.pkl')), 'rb') as fp:
        model = pickle.load(fp)

    predictor = BabyCryPredictor(model)

    predictions = list()
    string_predictions = list()
    for signal in play_list_processed:
        [string_prediction, is_baby_crying] = predictor.classify(signal)
        predictions.append(is_baby_crying)
        string_predictions.append(string_prediction)
    
    
    return [string_predictions ,is_baby_crying]

def label_audio(audio_file_path):
   
    [predictions, is_baby_crying] = classify_audio(audio_file_path)
    categories = {"Crying":0,"Silence":0,"Noise":0,"Laughing":0}
    for prediction in predictions:
        categories[prediction] +=1
    total = len(predictions) 
    categories["Crying"] = categories['301 - Crying baby']/total*100
    categories["Silence"] = categories['901 - Silence']/total*100
    categories["Noise"] = categories['902 - Noise']/total*100
    categories['Laughing'] = categories['903 - Baby laugh']/total*100
    return get_max_category(categories)

def label_motion(motion_file):
    motion_data = load_json_file(motion_file)
    total_count = len(motion_data)
    count_0 = sum(1 for value in motion_data.values() if value == 0)
    count_1 = total_count - count_0

    percentage_0 = (count_0 / total_count) * 100
    percentage_1 = (count_1 / total_count) * 100

    if percentage_0 >= 70:
        return "No Motion"
    else:
        return "Motion"
    
def label_video(video_file_path):
    # Define the path to your video
    video_path = video_file_path
    # Load the pre-trained face detector model
    model_file = "opencv_face_detector_uint8.pb"
    config_file = "opencv_face_detector.pbtxt"
    load_path_model = os.path.normpath('{}/model/'.format(os.path.dirname(os.path.abspath(__file__))))
    load_path_config = load_path_model
    model_path =  os.path.join(load_path_model, model_file)
    config_path = os.path.join(load_path_config,config_file)
    net = cv2.dnn.readNetFromTensorflow(model_path, config_path)
    # Open the video capture
    cap = cv2.VideoCapture(video_path)

    # Initialize a counter to keep track of the number of faces
    face_count = 0

    # Set the parameters for face detection
    confidence_threshold = 0.8
    input_image_size = (300, 300)
    scale_factor = 1.5

    while cap.isOpened():
        # Read the next frame from the video
        ret, frame = cap.read()

        if not ret:
            break

    # Resize the frame if it's too large
    frame = cv2.resize(frame, input_image_size)

    # Create a blob from the frame and perform forward pass
    blob = cv2.dnn.blobFromImage(frame, 1.0, input_image_size, [104, 117, 123], swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    # Iterate over the detected faces
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > confidence_threshold:
            face_count += 1

            # Get the coordinates of the bounding box
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (x, y, w, h) = box.astype(int)

            # Draw the bounding box around the face
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

            # Display the frame with the bounding boxes
            cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture
    cap.release()
    cv2.destroyAllWindows()

    # Print the total number of faces detected
    if face_count :
        return "Detected"
    return "Not Detected"

def get_max_category(categories):
    max_category = max(categories, key=categories.get)
    return max_category

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

