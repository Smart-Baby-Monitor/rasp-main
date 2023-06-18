from data_analysis.classifier import label_audio
from data_storage.models import Audio
from utils import logger
from utils.utils import DbAccess 


logger.info(f"Analyzing data")
db = DbAccess()

videos = db.selectQuery("SELECT * FROM videos WHERE label IS NULL LIMIT "+ str(20))
audios = db.selectQuery("SELECT * FROM audios WHERE label IS NULL LIMIT "+ str(20))
motions = db.selectQuery("SELECT * FROM motions WHERE label IS NULL LIMIT "+str(20))
logger.info("Using upto 3 threads to analyze data data")
model = Audio()
for audio in audios :
    try:
        model.load_data(audio)
        logger.info(f"Analysing audio {model.getId()}")
        audio_label = label_audio(audio)
        logger.info(f"audio labeled as {audio_label}")
        db.update(model.table,{"label":audio_label},{"id":model.getId()})
        logger.info("Labelled successfully")
    except Exception as e:
        logger.error(e)
logger.info("Finished Analyzing data")
