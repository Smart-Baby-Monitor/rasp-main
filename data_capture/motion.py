
import json
import RPi.GPIO as GPIO
import time
import env
from utils import utils


def capture_motion(file_name, seconds=30, interval=1) -> dict:
    """
        This function records motion data for a period specified at specific intervals   

        Args:
            seconds (int): The length of the motion capture in seconds
            interval (int): The number of seconds between successive motion data

        Returns:
            dict: A dictionary whose keys are the time between 0 and seconds and values are 1 for motion and 0 for no motion detected .

        Raises:
            Exception: 
    """

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    # Read output from PIR motion sensor
    GPIO.setup(env.motion_sensor_pin, GPIO.IN)

    counter = 0
    dict = {}
    detected = 0
    while True:
        detected = GPIO.input(11)
        dict[counter] = detected
        time.sleep(interval)
        counter += interval
        if (counter >= seconds):
            break
    path = utils.get_motions_folder() + file_name
    path.replace("//","/")
    with open(path, "w") as json_file:
        json.dump(dict, json_file)

    return dict
