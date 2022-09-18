from bing_api import *
from anki_connect import AnkiConnect
from tts.tts_config import TTSConfig
from random import choice
import os
from wiktionaryparser import WiktionaryParser


class CardCreator:

    parser = WiktionaryParser()

    @classmethod
    def create_card(cls, config, word):
        deck = config["deck"]
        model = config["model"]
        data = {"fields": {}}

        wdef = cls.parser.fetch(word)[0]
        wdef = wdef["definitions"][0]
        if len(wdef) == 0:
            return None

        meanings = wdef["text"]
        meaning = meanings[1]  # Main meaning
        phrases = wdef["examples"]

        if len(phrases) == 0:
            return None

        phrase = sorted(phrases, key=len)[0]

        for field, value in config["fields"].items():
            data["fields"][field] = (
                value.replace("[AUDIO]", "")
                .replace("[PICTURE]", "")
                .replace("[WORD]", word)
                .replace("[PHRASE]", phrase)
                .replace("[MEANING]", meaning)
            )

            if "[AUDIO]" in value:
                if not "audio" in data:
                    data["audio"] = {"fields": []}
                data["audio"]["fields"].append(field)

            elif "[PICTURE]" in value:
                if not "picture" in data:
                    data["picture"] = {"fields": []}
                data["picture"]["fields"].append(field)

        if "audio" in data:
            audio = os.path.abspath(
                TTSConfig.gen_tts_audio(TTSConfig.get_voice_code_config(), phrase)
            )
            data["audio"]["path"] = audio
            data["audio"]["filename"] = f"{word}.wav"

        if "picture" in data and len(meanings) >= 2:
            links = BingImageAPI.get_image_links(word)
            url = choice(links)
            data["picture"]["url"] = url
            data["picture"]["filename"] = f"{word}.png"
        else:
            del data["picture"]

        res = AnkiConnect.add_note(deck, model, data)

        os.remove(audio)

        return res
