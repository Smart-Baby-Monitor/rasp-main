# Provides a unified interface to access retrieve and update data in the local database
from utils import utils
from .models import *
import env
import json


def create_video(file_name, date_time):
    filepath = utils.get_videos_folder() + file_name
    video = Video()
    video.create({
        # "title": title,
        # "description": description,
        "filename": file_name,
        # "duration": duration,
        "filepath": filepath,
        # "size": size,
        # "frame_rate": frame_rate,
        # "encoding_format": "",
        # "bit_rate": "",
        "created_at": date_time,
        # "updated_at": "",
        # "synced_at": ""
    })


def create_audio(file_name, date_time):
    filepath = utils.get_audios_folder() + file_name
    audio = Audio()
    audio.create({
        # "name": "Audio",
        "filename": file_name,
        "filepath": filepath,
        # "duration": duration,
        # "description": description,
        "created_at": date_time,
    })


def create_motion(file_name, date_time):
    filepath = utils.get_motions_folder() + file_name
    motion = Motion()

    # data_str = json.dumps(data)

    motion.create({
        # "name": "Motion",
        "filename":file_name,
        "filepath":filepath,
        # "data": data_str,
        # "duration": duration,
        # "interval": interval,
        # "description": description,
        "created_at": date_time
    })
