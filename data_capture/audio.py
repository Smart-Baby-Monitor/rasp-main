import pyaudio
import wave

from utils import utils

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
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    path = utils.get_audios_folder() + file_name
    path.replace("//","/")
    with wave.open(path, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
    return path
