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
        """
        This function creates a new Anki flashcard using the configured format and the unknown word.
        All data is collected using the APIs. Anki needs to be running and AnkiConnect installed.
        """
        deck = config["deck"]
        model = config["model"]
        data = {"fields": {}}

        wdefs = cls.parser.fetch(word)[0]["definitions"]
        if len(wdefs) == 0:
            return None

        # First adjectives, then verbs etc
        wdefs = sorted(wdefs, key=lambda item: item["partOfSpeech"])
        deflists = []
        meanings = []

        for defs in wdefs:
            deflists.append(defs["text"])

        # Organizing definitions based on sorted ones
        # Mix one adjective with a verbe etc
        for i in range(1, len(deflists[0])):
            for j in range(len(deflists)):
                if i > (len(deflists[j]) - 1):
                    continue
                meanings.append(
                    deflists[j][i]
                    if len(deflists[j][i]) <= 244
                    else deflists[j][i][:244]
                )

        meaning = ""
        mns = 1

        for meani in meanings:
            # Ignore just past tense definitions
            if "simple past" in meani or "past participle" in meani:
                continue

            # Get all meanings that will fit 244 characters (max a tweet length)
            if len(meaning) + len(meani) > 244:
                continue

            meaning += f"{mns}. {meani}<br>"
            mns += 1

        # Check if any suitable meaning was found
        if mns == 1:
            return None

        phrases = wdefs[0]["examples"]

        if len(phrases) == 0:
            return None

        # Remove synonyms
        phrases = [ph for ph in phrases if "Synonym" not in ph]

        phrases = sorted(phrases, key=len)
        if len(phrases) > 3:
            phrases = phrases[:4]  # Limit options as the 4 shortest phrases

        phrase = choice(phrases)

        # Limit phrase in one sentence
        def one_sentence():
            delimiters = ("/", ".", "!", "?")
            for deli in delimiters:
                # Try each delimiter and check if it exists in the phrase
                phr = phrase.split(deli)
                if len(phr) < 2:
                    continue

                # Return the part that contains the unknown word
                for part in phr:
                    if word in part:
                        return part.strip()

            return phrase

        phrase = one_sentence()

        for field, value in config["fields"].items():
            data["fields"][field] = (
                value.replace("[AUDIO]", "")
                .replace("[PICTURE]", "")
                .replace("[WORD]", word)
                .replace("[PHRASE]", phrase.replace(word, f"<b>{word}</b>"))
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

        audio = None
        if "audio" in data:
            audio = os.path.abspath(
                TTSConfig.gen_tts_audio(TTSConfig.get_voice_code_config(), phrase)
            )
            data["audio"]["path"] = audio
            data["audio"]["filename"] = f"{word}.wav"

        img_path = None
        if "picture" in data:
            links = BingImageAPI.get_image_links(word)

            for url in links:
                req = requests.get(url)
                if req.status_code != 200:
                    continue

                with open(f"{word}.png", "wb+") as fp:
                    fp.write(req.content)

                img_path = os.path.abspath(f"{word}.png")
                break

            if img_path is None:
                del data["picture"]
            else:
                data["picture"]["path"] = img_path
                data["picture"]["filename"] = f"{word}.png"
        else:
            del data["picture"]

        res = AnkiConnect.add_note(deck, model, data)

        # Remove generate files
        if audio is not None:
            os.remove(audio)
        if img_path is not None:
            os.remove(img_path)

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
