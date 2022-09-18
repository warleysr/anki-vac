from data_apis import *
from anki_connect import AnkiConnect
from tts.tts_config import TTSConfig
from random import choice
import os


class CardCreator:
    @classmethod
    def create_card(cls, config, word):
        deck = config["deck"]
        model = config["model"]
        data = {"fields": {}}
        phrases = []
        meanings = []

        ox_def = OxfordAPI.get_definition(word)
        bt_def = BritannicaAPI.get_definition(word)

        if "results" in ox_def:
            lex = ox_def["results"][0]["lexicalEntries"][0]

            if "phrases" in lex:
                phrases.extend([ph["text"] for ph in lex["phrases"]])

            meaning = lex["entries"][0]["senses"][0]
            if "shortDefinitions" in meaning:
                meanings.extend([mn for mn in meaning["shortDefinitions"]])
            else:
                cross = meaning["crossReferences"][0]
                meanings.extend([cross["type"] + " " + cross["id"]])

        if "dros" in (entry := bt_def[0]):
            phrases.extend([ph["drp"] for ph in entry["dros"]])

            meanings.extend([mn for mn in entry["shortdef"]])

        if len(phrases) == 0 or len(meanings) == 0:
            return None

        phrase = sorted(phrases, key=len, reverse=True)[0]
        meaning = sorted(meanings, key=len)[0]

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
