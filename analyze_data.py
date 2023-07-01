from data_analysis.classifier import label_audio, label_motion, label_video
from data_storage.models import Audio, Motion, Video
from utils import logger
from utils.utils import DbAccess 


logger.info(f"Analyzing data")
db = DbAccess()

videos = db.selectQuery("SELECT * FROM videos WHERE label IS NULL LIMIT "+ str(20))
audios = db.selectQuery("SELECT * FROM audios WHERE label IS NULL LIMIT "+ str(20))
motions = db.selectQuery("SELECT * FROM motions WHERE label IS NULL LIMIT "+str(20))
logger.info("Using upto 3 threads to analyze data data")
if audios:
    logger.info(f"Labeling audios {audios}")
    model = Audio()
    for audio in audios :
        try:
            model.load_data(audio)
            logger.info(f"Analysing audio {model.getId()}")
            audio_label = label_audio(model.get_filepath())
            logger.info(f"audio labeled as {audio_label}")
            print("So close")
            db.update(model.table,{"label":audio_label},{"audio_id":model.getId()})
            print("after")
            logger.info("Audio Labelled successfully")
        except Exception as e:
            logger.error(e)


if motions:
    logger.info(f"Labeling motions {motions}")
    model = Motion()
    for motion in motions :
        try:
            model.load_data(motion)
            logger.info(f"Analysing motion {model.getId()}")
            motion_label = label_motion(model.get_filepath())
            logger.info(f"motion labeled as {motion_label}")
            db.update(model.table,{"label":motion_label},{"motion_id":model.getId()})
            logger.info("Motion Labelled successfully")
        except Exception as e:
            logger.error(e)

if videos:
    logger.info(f"Labeling videos {videos}")
    model = Video()
    for video in videos :
        try:
            model.load_data(video)
            logger.info(f"Analysing video {model.getId()}")
            video_label = label_video(model.get_filepath())
            logger.info(f"video labeled as {video_label}")
            db.update(model.table,{"label":video_label},{"video_id":model.getId()})
            logger.info("Video Labelled successfully")
        except Exception as e:
            logger.error(e)



logger.info("Finished Analyzing data")
