import requests
import sqlite3
import env
from datetime import datetime

import os


class DbAccess:
    def __init__(self, debug=False):
        self.debug = debug
        self.conn = sqlite3.connect(env.database_name)
        self.conn.row_factory = sqlite3.Row  # dict_factory
        self.query = ""
        # return self

    def update(self, table, data, where):
        query = f"UPDATE {table} SET "
        if data:
            for key, value in data.items():
                query += key + " ='" + value + "',"
            query = query[:-1] + " where "
        for key, value in where.items():
            query += key + " = '" + value + "' and "
        query = query[:-4]
        self.query = query
        try:
            self.sql(query)
        except:
            print("Exception occured")

    def sql(self, sql: str):
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def insert(self, table, data):
        query = "insert into " + table
        values = "("
        cols = "("
        for key, value in data.items():
            cols += key + ","
            values += "'" + str(value) + "',"

        cols = cols[:-1] + ")"
        values = values[:-1] + ")"
        query += cols + " values " + values
        self.query = query
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.commit()

        except Exception as e:
            print(e)
            print(self.query)
            pass

    def commit(
        self,
    ):
        self.conn.commit()
        self.conn.close()
        self.conn = sqlite3.connect(env.database_name)

    def selectQuery(self,sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            result = []
            rows = cur.fetchall()

            for row in rows:
                result.append(dict(row))

            return result

        except Exception as e:
            if self.debug:
                print(e)
            return False


    def select(self, table: str, columns: list = [], where: dict = {}):
        q = ""
        if not columns:
            q = "select *"
        else:
            strCols = ""
            for col in columns:
                strCols += col + ","
            strColsfinal = strCols[:-1]
            q = "select " + strColsfinal

        q += f" from {table} "

        if where:
            wherestr = ""
            orderbyValue = ""
            orderby = False
            for key, value in where.items():
                if key == "order by":
                    orderbyValue = value
                    orderby = True
                elif key == "between":
                    wherestr += " value and"
                else:
                    checkEmail = False
                    if checkEmail:
                        wherestr += f" {key} ='{value}' and"
                    else:
                        wherestr += f" {key} ='{value}' and"

            wherestr = wherestr[:-3]
            if wherestr and len(wherestr) > 3:
                q += " where " + wherestr

            if orderby:
                q += f" order by {orderbyValue}"
        try:
            cur = self.conn.cursor()
            cur.execute(q)
            result = []
            rows = cur.fetchall()

            for row in rows:
                result.append(dict(row))

            return result

        except Exception as e:
            if self.debug:
                print(e)
            return False


class Migration:
    def __init__(self, db: DbAccess):
        self.db = db

    def migrate(
        self,
    ):
        table_schemas = self.tables()
        for schema in table_schemas:
            try:
                self.db.sql(schema)
            except Exception as e:
                print("Exception", e)

    def tables(
        self,
    ):
        return [
            # vIDEOS Table will store information about tables
            "CREATE TABLE videos ("
            + "video_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            + "description TEXT  NULL,"
            + "filename TEXT  NULL,"
            + "filepath TEXT  NULL,"
            + "duration REAL  NULL,"
            + "created_at TEXT NULL,"
            + "updated_at TEXT NULL,"
            + "synced_at TEXT NULL"
            + ")",
            # Audios table will store audio files
            "CREATE TABLE audios ("
            + "audio_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            + "description TEXT NULL,"
            + "filename TEXT NULL,"
            + "filepath TEXT NULL,"
            + "duration TEXT NULL,"
            + "created_at TEXT NULL,"
            + "updated_at TEXT NULL,"
            + "synced_at TEXT NULL"
            + ")",
            # Motion Data
            "CREATE TABLE motions ("
            + "motion_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            + "description TEXT NULL,"
            + "filename TEXT NULL,"
            + "filepath TEXT NULL,"
            + "duration TEXT NULL,"
            + "created_at TEXT NULL,"
            + "updated_at TEXT NULL,"
            + "synced_at TEXT NULL"
            + ")",
            # Devices table  to store all the devices and their ststuses
            "CREATE TABLE devices ("
            + "device_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            + "name TEXT NULL,"
            + "type TEXT NULL,"
            + "location TEXT NULL,"
            + "status TEXT NULL,"
            + "version TEXT NULL,"
            + "created_at TEXT NULL,"
            + "updated_at TEXT NULL,"
            + "synced_at TEXT NULL"
            + ")",
            # Configurations table will store various configs
            "CREATE TABLE configs ("
            + "config_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            + "name TEXT NULL,"
            + "value TEXT NULL,"
            + "description TEXT NULL,"
            + "user_id TEXT NULL,"
            + "category TEXT NULL,"
            + "enabled TEXT NULL,"
            + "created_at TEXT NULL,"
            + "updated_at TEXT NULL,"
            + "deleted_at TEXT NULL"
            + ")",
            # account table
            "CREATE TABLE accounts (" + 
            "account_id INTEGER PRIMARY KEY AUTOINCREMENT,"+
            "auth_token TEXT NULL,"+
            "email TEXT NULL,"+
            "password TEXT NULL,"+
            "is_active INTEGER NULL)",
            
        ]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_videos_folder():
    return env.file_storage + "/videos/"


def get_audios_folder():
    return env.file_storage + "/audios/"


def get_motions_folder():
    return env.file_storage + "/motions/"


def generate_datetime():
    dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def generate_filename(date_time, type, extension):
    # Parse the date string
    date_format = "%Y-%m-%d %H:%M:%S"
    date_obj = datetime.strptime(date_time, date_format)
    # Generate the file name
    file_name = f"{type}_{date_obj.strftime('%Y%m%d_%H%M%S')}.{extension}"
    return file_name


def audio_filename(date_time):
    return generate_filename(date_time, "audio", "mp3")


def video_filename(date_time):
    return generate_filename(date_time, "video", "h264")


def motion_filename(date_time):
    return generate_filename(date_time, "motion", "json")


def run_migrations():
    db = DbAccess()
    migration = Migration(db)
    migration.migrate()


def create_folders():
    import os

    parent_folder = env.file_storage
    folder_names = ["audios", "videos", "motions"]

    # Check if parent folder exists
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    # Create subfolders within the parent folder
    for folder_name in folder_names:
        folder_path = os.path.join(parent_folder, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


def convert_to_mp4(file_name, keep_original=False):
    from moviepy.editor import VideoFileClip
    input_path = get_videos_folder() + file_name
    # Get the directory and base filename
    directory = os.path.dirname(input_path)
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    # Create the new output path with .mp4 extension
    output_path = os.path.join(directory, base_filename + ".mp4")

    # Covert the video
    clip = VideoFileClip(input_path).subclip(0, 30)
    clip.set_duration(30)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    if not keep_original:
        os.remove(input_path)
    return output_path
