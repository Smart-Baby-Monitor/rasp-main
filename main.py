import threading

# from data_capture.motion import capture_motion
# from data_capture.video import capture_video
from data_capture.audio import capture_audio
from data_capture.motion import capture_motion
from data_capture.video import capture_video
from data_storage import storage_controller
from data_transfer.send_data import DataTransafer
from utils import logger, utils

try: 
    # Ensure the storage folders are existent
    utils.create_folders()

    utils.run_migrations()

    logger.info("Generating file_names")
    date_time = utils.generate_datetime()
    audio_file = utils.audio_filename(date_time)
    video_file = utils.video_filename(date_time)
    motion_file = utils.motion_filename(date_time)

    logger.info("Capturing Data using upto 4 threads ")
    # Create multiple threads
    threads = [
        # Task to capture audio
        threading.Thread(target=capture_audio, args=[audio_file]),
        # Task to capture video
        threading.Thread(target=capture_video, args=[video_file]),
        # Task to capture motion
        threading.Thread(target=capture_motion, args=[motion_file]),
        # Task for syncing data
        threading.Thread(target=DataTransafer.synchronize),
    ]
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    logger.info("Completed Data capture")

    logger.info("Saving the data to the database ")
    # Some conversions -Convert the h264 to mp4
    # video_file = utils.convert_to_mp4(video_file)
    # logger.info("Conversion complete")

    # # Save the details to the database
    # logger.info("Savings data using upto 3 threads ")
    # threads = [
    #     threading.Thread(target=storage_controller.create_audio, args=[audio_file,date_time]),
    #     threading.Thread(target=storage_controller.create_video, args=[video_file,date_time]),
    #     threading.Thread(target=storage_controller.create_motion, args=[motion_file,date_time]),
    # ]

    # for t in threads:
    #     t.start()

    # # Wait for all threads to complete
    # for t in threads:
    #     t.join()
    storage_controller.create_audio(audio_file,date_time)
    storage_controller.create_video(video_file,date_time)
    storage_controller.create_motion(motion_file,date_time)
    
    logger.info("Data save completed ")
    # Now do analysis
except Exception as e:
    logger.exception("Exception Occured ")
    logger.exception(e)