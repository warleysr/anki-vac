from bing_api import *
from anki_connect import AnkiConnect
from tts.tts_config import TTSConfig
from random import choice
import os
import interface
from wiktionaryparser import WiktionaryParser


class CardCreator:

    parser = WiktionaryParser()

    @classmethod
    def create_card(cls, config, word):
        deck = config["deck"]
        model = config["model"]
        data = {"fields": {}}

        wdefs = cls.parser.fetch(word)[0]["definitions"]
        if len(wdefs) == 0:
            return None
        wdefs = sorted(wdefs, key=lambda item: item["partOfSpeech"])
        wdef = wdefs[0]  # First adjectives, then verbs etc

        meanings = wdef["text"]
        meaning = ""
        mns = 1

        # Get all meanings that will fit 100 characters
        for mn in range(1, len(meanings)):
            if len(meaning) + len(meanings[mn]) > 100:
                continue
            meaning += f"{mns}. {meanings[mn]}<br>"
            mns += 1

        phrases = wdef["examples"]

        if len(phrases) == 0:
            return None

        phrases = sorted(phrases, key=len)
        if len(phrases) > 3:
            phrases = phrases[:4]  # Limit options as the 3 shortest phrases

        phrase = choice(phrases).replace(word, f"<b>{word}</b>")

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

    @classmethod
    def bulk_card_creation(cls, config, words, window):
        nwords = len(words)
        count = 0
        fails = 0

        for i, word in enumerate(words):
            window.write_event_value("-THREAD-", (i, nwords))
            cc = CardCreator.create_card(config, word)

            if cc is None:
                fails += 1
            else:
                count += 1

        window.write_event_value("-FINISH-", (count, fails))
