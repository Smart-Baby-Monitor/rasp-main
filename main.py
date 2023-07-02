import threading

# from data_capture.motion import capture_motion
# from data_capture.video import capture_video
from data_capture.audio import capture_audio
from data_capture.motion import capture_motion
from data_capture.video import capture_video
from data_storage import storage_controller
from data_transfer.send_data import DataTransafer
from utils import logger, utils
from data_analysis.classifier import label_audio, label_motion, label_video
from data_storage.models import Audio, Motion, Video
from utils.utils import DbAccess 


def capture_data():
    logger.info("Capture Data Start")
    logger.info("Generating file_names")
    date_time = utils.generate_datetime()
    audio_file = utils.audio_filename(date_time)
    video_file = utils.video_filename(date_time)
    motion_file = utils.motion_filename(date_time)

    logger.info("Capturing Data using upto 3 threads ")
    # Create multiple threads
    threads = [
        # Task to capture audio
        threading.Thread(target=capture_audio, args=[audio_file]),
        # Task to capture video
        threading.Thread(target=capture_video, args=[video_file]),
        # Task to capture motion
        threading.Thread(target=capture_motion, args=[motion_file]),
    ]
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    logger.info("Capture Data End")

    logger.info("Saving Data Start ")
    storage_controller.create_audio(audio_file,date_time)
    storage_controller.create_video(video_file,date_time)
    storage_controller.create_motion(motion_file,date_time)

    logger.info("Saving Data End ")
        
def analyze_data():
    
    logger.info(f"Analyze Data Start")
    db = DbAccess()
    logger.info("Connected to databse")
    videos = db.selectQuery("SELECT * FROM videos WHERE label IS NULL LIMIT "+ str(20))
    audios = db.selectQuery("SELECT * FROM audios WHERE label IS NULL LIMIT "+ str(20))
    motions = db.selectQuery("SELECT * FROM motions WHERE label IS NULL LIMIT "+str(20))
    logger.info("Picked un analyzed data from the database")
    logger.info("Analyzing audios")
    if not audios:
        logger.info("No audios found for analysis")
    if audios:
        logger.info(f"Total audios to analyze: {len(audios)}")
        
        model = Audio()
        for audio in audios :
            try:
                model.load_data(audio)
                logger.info(f"Analysing audio #{model.getId()}. File name: {model.get_filepath()}")
                audio_label = label_audio(model.get_filepath())
                logger.info(f"Labelling Audio as {audio_label}")
                logger.info("Updating label in the databse")
                db.update(model.table,{"label":audio_label},{"audio_id":model.getId()})
                logger.info("Audio Labelled successfully")
            except Exception as e:
                logger.error(f"Exception Occured {e}")

    if not motions:
        logger.info("No motions found for analysis")    
    if motions:
        logger.info(f"Total motions to analyze: {len(motions)}")
        model = Motion()
        for motion in motions :
            try:
                model.load_data(motion)
                logger.info(f"Analysing motion #{model.getId()} File name: {model.get_filepath()}")
                motion_label = label_motion(model.get_filepath())
                logger.info(f"Labelling motion as {motion_label}")
                logger.info("Updating label in the databse")
                db.update(model.table,{"label":motion_label},{"motion_id":model.getId()})
                logger.info("Motion Labelled successfully")
            except Exception as e:
                logger.error(f"Exception Ocuured {e}")
    
    if not videos:
        logger.info("No videos found for analysis")    
    if videos:
        logger.info(f"Total videos to analyze: {len(videos)}")
        model = Video()
        for video in videos :
            try:
                model.load_data(video)
                logger.info(f"Analysing video #{model.getId()} File name: {model.get_filepath()}")
                video_label = label_video(model.get_filepath())
                logger.info(f"Labelling video as {video_label}")
                logger.info("Updating label in the databse")
                
                db.update(model.table,{"label":video_label},{"video_id":model.getId()})
                logger.info("Video Labelled successfully")
            except Exception as e:
                logger.error(e)

    logger.info("Analyzing data Stop")

def send_data():
    logger.info("Data Send Start")
    DataTransafer.send_data()
    logger.info("Data Send Stop")
def init():
    utils.create_folders()

    utils.run_migrations()

int()
try: 
    while True:
        
        capture_data()
        send_data()
        analyze_data()
        send_data()
        # capture_thread = threading.Thread(target=capture_data)
        # analyze_thread = threading.Thread(target=analyze_data)
        # send_thread = threading.Thread(target=send_data)
        # Start the threads 
        # capture_thread.start()
        # analyze_thread.start()
        # send_thread.start()
        # Wait for all threads to complete
        # capture_thread.join()
        # analyze_thread.join()
        # send_thread.join()
   
        
except Exception as e:
    logger.exception("Exception Occured ")
    logger.exception(e)
