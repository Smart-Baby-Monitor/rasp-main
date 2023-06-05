import os
import unittest
from unittest.mock import patch, MagicMock
from data_transfer.send_data import DataTransafer
from data_storage.models import Audio, Motion, Video
from  utils import utils
from data_capture.audio import capture_audio
from data_capture.motion import capture_motion
from data_capture.video import   capture_video 
import env


class DataCaptureTestCase(unittest.TestCase):
    def test_capture_audio(self):

        OUTPUT_FILE =  utils.audio_filename() + "test_output.wav"
        capture_audio(OUTPUT_FILE)
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        # Remove the file
        os.remove(OUTPUT_FILE)

    def test_capture_motion(self):
        OUTPUT_FILE = utils.motion_filename() + "test_output.json"
        capture_motion(OUTPUT_FILE)
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        # Remove the file
        os.remove(OUTPUT_FILE)


    def test_capture_video(self):
        OUTPUT_FILE =  utils.video_filename() + "test_output.wav"
        capture_video(OUTPUT_FILE)
        self.assertTrue(os.path.exists(OUTPUT_FILE))
        # Remove the file
        os.remove(OUTPUT_FILE)


class DbAccessTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary objects or variables for the tests
        self.db = utils.DbAccess(debug=True)  # Initialize DbAccess with debug mode

    def tearDown(self):
        # Clean up any resources used by the tests
        self.db.conn.close()

    def test_update(self):
        # Test the update method of DbAccess
        table = "videos"
        data = {"label": "New Label"}
        where = {"video_id": 1}
        
        # Mock the sql method of DbAccess to assert the query and return value
        with patch.object(self.db, "sql", MagicMock()) as mock_sql:
            self.db.update(table, data, where)
            
            # Assert that the query is constructed correctly
            expected_query = "UPDATE videos SET label ='New Label' where video_id = '1'"
            self.assertEqual(self.db.query, expected_query)
            
            # Assert that the sql method is called with the correct query
            mock_sql.assert_called_with(expected_query)

    def test_insert(self):
        # Test the insert method of DbAccess
        table = "videos"
        data = {"description": "New Video", "label": "Video Label"}
        
        # Mock the cursor and execute methods of DbAccess to assert the query and return value
        with patch.object(self.db.conn, "cursor", MagicMock()) as mock_cursor:
            mock_execute = mock_cursor.return_value.execute
            self.db.insert(table, data)
            
            # Assert that the query is constructed correctly
            expected_query = "insert into videos(description,label) values ('New Video','Video Label')"
            self.assertEqual(self.db.query, expected_query)
            
            # Assert that the cursor and execute methods are called with the correct query
            mock_execute.assert_called_with(expected_query)
            self.db.commit.assert_called()

    def test_select(self):
        # Test the select method of DbAccess
        table = "videos"
        columns = ["video_id", "label"]
        where = {"label": "Video Label"}
        
        # Mock the cursor and execute methods of DbAccess to assert the query and return value
        with patch.object(self.db.conn, "cursor", MagicMock()) as mock_cursor:
            mock_execute = mock_cursor.return_value.execute
            mock_fetchall = mock_cursor.return_value.fetchall
            
            # Set up the fetchall method to return a list of rows
            mock_fetchall.return_value = [(1, "Video Label"), (2, "Video Label")]
            
            result = self.db.select(table, columns, where)
            
            # Assert that the query is constructed correctly
            expected_query = "select video_id,label from videos where label ='Video Label'"
            self.assertEqual(self.db.query, expected_query)
            
            # Assert that the cursor and execute methods are called with the correct query
            mock_execute.assert_called_with(expected_query)
            
            # Assert that the result is a list of dictionaries
            expected_result = [{"video_id": 1, "label": "Video Label"}, {"video_id": 2, "label": "Video Label"}]
            self.assertEqual(result, expected_result)


class MigrationTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary objects or variables for the tests
        self.db = MagicMock()  # Mock the DbAccess object
        self.migration = utils.Migration(self.db)

    def test_migrate(self):
        # Test the migrate method of Migration
        table_schemas = self.migration.tables()
        
        # Mock the sql method of DbAccess to assert the query
        with patch.object(self.db, "sql", MagicMock()) as mock_sql:
            self.migration.migrate()
            
            # Assert that the sql method is called with the correct schema queries
            for schema in table_schemas:
                mock_sql.assert_any_call(schema)

class UtilsTestCase(unittest.TestCase):
    def test_generate_filename(self):
        # Test the generate_filename function
        date_time = "2023-07-05 12:30:00"
        type = "audio"
        extension = "mp3"
        
        result = utils.generate_filename(date_time, type, extension)
        
        # Assert that the result is constructed correctly
        expected_result = "audio_20230705_123000.mp3"
        self.assertEqual(result, expected_result)

class FolderTestCase(unittest.TestCase):
    def test_create_folders(self):
        
        # Mock the os.makedirs method to assert the folder creation
        with patch("os.makedirs") as mock_makedirs:
            utils.create_folders()
            
            # Assert that the makedirs method is called with the correct folder paths
            expected_folders = [
                "/path/to/file_storage/audios",
                "/path/to/file_storage/videos",
                "/path/to/file_storage/motions"
            ]
            for folder in expected_folders:
                mock_makedirs.assert_any_call(folder)
                

class DataTransferTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary objects or variables for the tests
        self.data_transfer = DataTransafer()

    @patch.object(DataTransafer, "send")
    def test_send_video(self, mock_send):
        # Test the send_video method of DataTransafer
        video = MagicMock(spec=Video)
        video.get_filepath.return_value = "/path/to/video.mp4"
        video.get_filename.return_value = "video.mp4"
        video.get_label.return_value = "Video Label"
        
        mock_send.return_value = True
        
        result = self.data_transfer.send_video(video)
        
        # Assert that the send method is called with the correct parameters
        expected_url = env.api_base_url + "/client/data"
        expected_data = {
            "type": "video",
            "title": "video.mp4",
            "description": "This is my video description",
            "label": "Video Label"
        }
        expected_file_path = "/path/to/video.mp4"
        mock_send.assert_called_with(expected_url, expected_data, expected_file_path)
        
        # Assert that the result is True
        self.assertTrue(result)

    @patch.object(DataTransafer, "send")
    def test_send_audio(self, mock_send):
        # Test the send_audio method of DataTransafer
        audio = MagicMock(spec=Audio)
        audio.get_filepath.return_value = "/path/to/audio.wav"
        audio.get_filename.return_value = "audio.wav"
        audio.get_label.return_value = "Audio Label"
        
        mock_send.return_value = True
        
        result = self.data_transfer.send_audio(audio)
        
        # Assert that the send method is called with the correct parameters
        expected_url = env.api_base_url + "/client/data"
        expected_data = {
            "type": "audio",
            "title": "audio.wav",
            "description": "This is my audio description",
            "label": "Audio Label"
        }
        expected_file_path = "/path/to/audio.wav"
        mock_send.assert_called_with(expected_url, expected_data, expected_file_path)
        
        # Assert that the result is True
        self.assertTrue(result)

    @patch.object(DataTransafer, "send")
    def test_send_motion(self, mock_send):
        # Test the send_motion method of DataTransafer
        motion = MagicMock(spec=Motion)
        motion.get_filepath.return_value = "/path/to/motion.txt"
        motion.get_filename.return_value = "motion.txt"
        motion.get_label.return_value = "Motion Label"
        
        mock_send.return_value = True
        
        result = self.data_transfer.send_motion(motion)
        
        # Assert that the send method is called with the correct parameters
        expected_url = env.api_base_url + "/client/data"
        expected_data = {
            "type": "motion",
            "title": "motion.txt",
            "description": "This is my motion description",
            "label": "Motion Label"
        }
        expected_file_path = "/path/to/motion.txt"
        mock_send.assert_called_with(expected_url, expected_data, expected_file_path)
        
        # Assert that the result is True
        self.assertTrue(result)

    @patch.object(DataTransafer, "send_video")
    @patch.object(DataTransafer, "send_audio")
    @patch.object(DataTransafer, "send_motion")
    @patch.object(DataTransafer, "process_audios")
    @patch.object(DataTransafer, "process_videos")
    @patch.object(DataTransafer, "process_motions")
    @patch.object(utils.DbAccess, "selectQuery")
    def test_send_data(self, mock_select_query, mock_process_motions, mock_process_videos,
                       mock_process_audios, mock_send_motion, mock_send_audio, mock_send_video):
        # Test the send_data method of DataTransafer
        mock_select_query.side_effect = [
            [],  # No videos
            [],  # No audios
            []   # No motions
        ]
        
        self.data_transfer.send_data(chunk=20)
        
        # Assert that the selectQuery method is called with the correct queries
        expected_select_queries = [
            "SELECT * FROM videos WHERE synced_at IS NULL AND label IS NOT NULL LIMIT 20",
            "SELECT * FROM audios WHERE synced_at IS NULL AND label IS NOT NULL LIMIT 20",
            "SELECT * FROM motions WHERE synced_at IS NULL AND label IS NOT NULL LIMIT 20"
        ]
        for i, query in enumerate(expected_select_queries):
            mock_select_query.assert_any_call(query)
        
        # Assert that the process_videos, process_audios, and process_motions methods are called
        mock_process_videos.assert_called_once()
        mock_process_audios.assert_called_once()
        mock_process_motions.assert_called_once()


if __name__ == '__main__':
    unittest.main()
