from anki_connect import AnkiConnect
from bing_api import *
from interface import GraphicInterface
from tts.tts_config import TTSConfig
import time
from enum import Enum
import json

BING_KEY = None
TTS_KEY = None


class Logger:

    __instance = None

    class LoggerHandler:
        def __init__(self):
            self.arq = open("log.txt", "a")

        def __del__(self):
            self.arq.close()

        def write_log(self, text):
            self.arq.write(text)

    class LogType(Enum):
        INFO = "[INFO] "
        ERROR = "[ERROR] "

    @classmethod
    def log(cls, text: str, type: LogType = LogType.INFO):
        if Logger.__instance is None:
            Logger.__instance = Logger.LoggerHandler()

        t = time.localtime()
        current_time = time.strftime("%d/%m/%Y %H:%M:%S ", t)
        Logger.__instance.write_log(f"[{current_time}]{type.value}{text}")


if __name__ == "__main__":
    # Load config file
    with open("config.json", "r", encoding="utf-8") as fp:
        config = json.load(fp)

    # Define APIs urls
    BingImageAPI.BING_API = config["apis-urls"]["BING_API"]
    TTSConfig.TTS_API = config["apis-urls"]["TTS_API"]
    AnkiConnect.ANKI_CONNECT = config["apis-urls"]["ANKI_CONNECT"]

    # Define APIs keys
    BingImageAPI.BING_KEY = config["apis-keys"]["BING"]
    TTSConfig.TTS_KEY = config["apis-keys"]["TTS"]

    # Start graphic interface
    GraphicInterface.start_main(config)
