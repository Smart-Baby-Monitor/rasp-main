
from utils import utils
from utils.utils import DbAccess


class Model:

    def __init__(self, id=""):
        self.db = DbAccess(True)
        self.id = id
        self.data = {}
        if id:
            self.data = self.select([], {f"{self.key}": id})
    def remove(self,):
        return self.db.update(self.table,{"synced_at":utils.generate_datetime()},{"id":self.id})
    def getId(self):
        return self.id

    def select(self, columns, where):
        results = self.db.select(self.table, columns, where)
        if (results and len(results) > 0):
            return results[0]
        return results

    def create(self, data):
        self.db.insert(self.table, data)
    def load_data(self,data:dict):
        self.id = data[self.key]
        self.data = data
    def get_filepath(self):
        return self.data['filepath']
    def get_filename(self):
        return self.data['filename']
    def get_created_at(self):
        return self.data['created_at']
    def get_updated_at(self):
        return self.data['updated_at']
    def get_synced_at(self):
        return self.data['synced_at']
    


class Video(Model):
    def __init__(self, id=""):
        self.table = "videos"
        self.key = "video_id"
        super().__init__(id)

    def get_video_id(self,):
        return self.data['video_id']

    def get_title(self,):
        return self.data['title']

    def get_description(self,):
        return self.data['description']

    def get_duration(self,):
        return self.data['duration']

    def get_size(self,):
        return self.data['size']

    def get_frame_rate(self,):
        return self.data['frame_rate']

    def get_encoding_format(self,):
        return self.data['encoding_format']

    def get_bit_rate(self,):
        return self.data['bit_rate']

class Account(Model):
    def __init__(self, id=""):
        self.table = "accounts"
        self.key = "account_id"
        super().__init__(id)
    def get_auth_token(self):
        return self.data['auth_token']
    def get_email(self):
        return self.data['email']
    def get_password(self):
        return self.data['password']
    def get_is_active(self):
        return self.data['is_active']
            
class Audio(Model):
    def __init__(self, id=""):
        self.table = "audios"
        self.key = "audio_id"
        super().__init__(id)


class Device(Model):
    def __init__(self, id=""):
        self.table = "devices"
        self.key = "device_id"
        super().__init__(id)


class Config(Model):
    def __init__(self, id=""):
        self.table = "configs"
        self.key = "config_id"
        super().__init__(id)

    def get_name(self):
        return self.data['name']

    def get_value(self):
        return self.data['value']


class Motion(Model):
    def __init__(self, id=""):
        self.table = "motions"
        self.key = "motion_id"
        super().__init__(id)
    # new_dict = json.loads(json_str)
    