import pyaudio
import wave
import sounddevice as sd
import soundfile as sf

from utils import logger, utils

# Configurations DON'T unless you understand them
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integer)
CHANNELS = 2  # Mono audio
RATE = 44100  # Sampling rate


def capture_audio(file_name, seconds=30) -> list:
    seconds += 1
    """
    This function records sound using the microphone for 30 seconds by default or specified number of seonds 
    Args:
        file_name (str): The name of the file to save the audio to 
        seconds(int): How long the audio should be recored
    Returns: 
        None
    """
    logger.info("Starting audio recording ")
    path = utils.get_audios_folder() + file_name
    path.replace("//","/")

    duration = seconds  # Duration in seconds
    sample_rate = 44100  # Sample rate in Hz
    channels = 2  # Number of audio channels (1 for mono, 2 for stereo)

    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait()  # Wait until the recording is complete
    logger.info("Saving audio file ")

    # Save the recorded audio to a file using soundfile

    sf.write(path, audio_data, sample_rate, format='wav')
    return path
    
    