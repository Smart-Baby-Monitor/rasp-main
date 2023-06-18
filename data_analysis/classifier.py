# -*- coding: utf-8 -*-

import argparse
import os
import pickle
import sys
import warnings

egg_path = '{}/../lib/baby_cry_detection-1.1-py2.7.egg'.format(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(egg_path)

from data_analysis.reader import Reader
from data_analysis.baby_cry_predictor import BabyCryPredictor
from data_analysis.feature_engineer import FeatureEngineer
from data_analysis.majority_voter import MajorityVoter


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

    # MAJORITY VOTE Just tries to know if the baby is crying 
   
    majority_voter = MajorityVoter(predictions)
    is_baby_crying = majority_voter.vote()

    # Save prediction result
    with open(os.path.join(save_path, 'prediction.txt'), 'a+') as text_file:
        text_file.write("{0}".format(is_baby_crying))
    
    
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

def get_max_category(categories):
    max_category = max(categories, key=categories.get)
    return max_category

