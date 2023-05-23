import os
import unittest
import pyaudio
import wave

from data_capture.audio import capture_audio


class TestAudioCapture(unittest.TestCase):
    def test_capture_audio(self):

        OUTPUT_FILE = "test_output.wav"
        capture_audio(OUTPUT_FILE)
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        # Clean up any generated files or resources after the test
        os.remove(OUTPUT_FILE)


class TestMotionCapture(unittest.TestCase):
    def test_capture_motion(self):
        pass


class TestVideoCapture(unittest.TestCase):
    def test_capture_video(self):
        pass


if __name__ == '__main__':
    unittest.main()
