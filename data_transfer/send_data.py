import os
import threading
from data_storage.models import Audio, Motion, Video
import env
import requests
from utils import account, logger

from utils.utils import DbAccess


class DataTransafer:
    
    @staticmethod
    def send(url,data:dict,file_path):
        try:
           
            logger.info("DT.send: Sending Data")
            data['auth_token'] = account.Account.get_auth_token() 
            data['device_id'] = env.device_id
            files = {
                "file": open(file_path, "rb")
            }
            logger.info(f"Making API call {url}")
            
            response = requests.post(url, data=data, files=files,headers={
                            "X-Requested-With": "XMLHttpRequest"})
            
            logger.info("Got a response ")
            
            if response.status_code == 200:
                logger.info("Response Status code 200 OK")
                # response_data = response.json()
                logger.info(response.text)
                return True
            else:
                logger.info("Some Errors occured Check the reponse below")
                logger.info(response.text)
                return False
        except Exception as e:
            logger.exception("An Exception Occured")
            logger.info(e)
            return False
      
    
    @staticmethod
    def send_video(video: Video):
        print(video)
        logger.info("Sending Video data ")
        url = env.api_base_url+"/client/data"
        try:
            file_path = video.get_filepath()
            # Set the parameters
            data = {
                "type": "video",
                "title": video.get_filename(),#video.get_title(),
                "description": "This is my video description",
                "authToken":env.auth_token,
                "label":video.get_label()
  
            }

            ret = DataTransafer.send(url,data,file_path)
            if ret :
                logger.info("Video sennt Successfully ")
                return True
            else :
                logger.info("Failed to send video")
                return False
        except Exception as e:
            logger.info("Exception occured")
            logger.exception(e)
            return False


 
          
    @staticmethod
    def send_audio(audio: Audio):
        print(audio)
        logger.info("Sending Audio")
        url = env.api_base_url+"/client/data"

        file_path = audio.get_filepath()
        try:
            # Set the parameters
            data = {
                "type": "audio",
                "title": audio.get_filename(),
                "description": "This is my audio description",
                "authToken":env.auth_token,
                "label":audio.get_label()
            }

            ret = DataTransafer.send(url,data,file_path)
            if ret :
                logger.info("Audio sennt Successfully ")
                return True
            else :
                logger.info("Failed to send audio")
                return False
        except Exception as e:
            logger.info("Exception occured")
            logger.exception(e)
            return False
            
    @staticmethod
    def send_motion(motion: Motion):
        print(motion)
        logger.info("Sending Motion data")
        url = env.api_base_url+"/client/data"

        try:
            file_path = motion.get_filepath()
            # Set the parameters
            data = {
                "type": "motion",
                "title": motion.get_filename(),
                "description": "This is my motion description",
                "authToken":env.auth_token,
                "label":motion.get_label()
            }

            ret = DataTransafer.send(url,data,file_path)
            if ret :
                logger.info("Motion sennt Successfully ")
                return True
            else :
                logger.info("Failed to send motion")
                return False
        except Exception as e:
            logger.info("Exception occured")
            logger.exception(e)
            return False
  
    @staticmethod
    def process_videos(videos):
        logger.info("Processing videos")
        
        if not videos :
            logger.info("No videos found Returning False")
            
            return 
        logger.info(f"Found Videos: {len(videos)}")
       
        model = Video()
        for video in videos :
            model.load_data(video)
            sent = DataTransafer.send_video(model)
            if sent :
               os.remove(model.get_filepath())
               model.remove()

        logger.info("Processed videos")
        
    @staticmethod
    def process_audios(audios):
        logger.info("Processing audios")
        if not audios :
            logger.info("No audios found Returning False")
            return
        logger.info(f"Found  Audios: {len(audios)}")
       
        model = Audio()
        for audio in audios :
            model.load_data(audio)
            sent = DataTransafer.send_audio(model)
            if sent :
               os.remove(model.get_filepath())
               model.remove()
        logger.info("Processed audios")
    @staticmethod
    def process_motions(motions):
        logger.info("Processing motions")
        
        if not motions :
            logger.info("No motions found Returning False")
            return
        logger.info(f"Found Motions: {len(motions)}")
       
        model = Motion()
        for motion in motions :
            model.load_data(motion)
            sent = DataTransafer.send_motion(model)
            if sent :
                os.remove(model.get_filepath())
                model.remove()
        logger.info("Processed motions")

     
    @staticmethod 
    def send_data(chunk=20):
        logger.info(f"Sending data chunk size {chunk}")
        db = DbAccess()
        
        videos = db.selectQuery("SELECT * FROM videos WHERE synced_at IS NULL LIMIT "+ str(chunk))
        audios = db.selectQuery("SELECT * FROM audios WHERE synced_at IS NULL LIMIT "+ str(chunk))
        motions = db.selectQuery("SELECT * FROM motions WHERE synced_at IS NULL LIMIT "+str(chunk))
        logger.info("Using upto 3 threads to send data")
       
        # Create multiple threads
        # threads = [
        #     # Task to transfer audios 
        #     threading.Thread(target=DataTransafer.process_audios, args=[audios]),
        #     # Task to transfer videos
        #     threading.Thread(target=DataTransafer.process_videos, args=[videos]),
        #     # Task to transfer motions
        #     threading.Thread(target=DataTransafer.process_motions, args=[motions]),
        #  ]
        # for t in threads:
        #     t.start()
        DataTransafer.process_audios(audios)
        # Task to transfer videos
        DataTransafer.process_videos(videos)
        # Task to transfer motions
        DataTransafer.process_motions(motions)

        # Wait for all threads to complete
        # for t in threads:
            # t.join()
        logger.info("Finished Sending data")
    @staticmethod
    def synchronize():
        pass
