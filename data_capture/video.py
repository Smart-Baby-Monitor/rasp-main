import picamera
from utils import logger, utils


def capture_video(file_name, seconds=30):
    """
    This function captures video for the specified number of seconds 
    and saves it ti the specified file 
    Args: 
        file_name (str):the name of the file to save the video to 
        seconds (int):The length of the video in seconds 
    Returns:
        None
    """
    logger.info("Capturing Video ...")
    path = utils.get_videos_folder() + file_name
    path.replace("//","/")
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_recording(path)
    camera.wait_recording(seconds)
    camera.stop_recording()
    camera.close()
    logger.info("Done Capturing Video")
