import PySimpleGUI as Sg
from playsound import playsound
import json
import requests
import os
import threading
import uuid


class TTSConfig:

    window = None
    test_text = "\u25b6 Test voice"

    @classmethod
    def start_window(cls):

        # Read voices data and config
        with open("tts/english_voices.json", "r") as fp:
            voices_data = json.load(fp)
            voices = voices_data["voices"]
            styles = voices_data["styles"]
            config = voices_data["config"]

        Sg.theme("Reddit")

        font = "Arial 10 bold"
        fsize = (30, 10)

        layout = [
            [
                Sg.Text("Accent from: ", font=font),
                Sg.Push(),
                Sg.DropDown(
                    tuple(voices.keys()),
                    enable_events=True,
                    key="accent",
                    size=fsize,
                    default_value=config["accent"],
                ),
            ],
            [
                Sg.Text("Gender: ", font=font),
                Sg.Push(),
                Sg.DropDown(
                    ("Male", "Female"),
                    enable_events=True,
                    key="gender",
                    size=fsize,
                    default_value=config["gender"],
                ),
            ],
            [
                Sg.Text("Voice: ", font=font),
                Sg.Push(),
                Sg.DropDown((), enable_events=True, key="voice", size=fsize),
            ],
            [
                Sg.Text("Style: ", font=font),
                Sg.Push(),
                Sg.DropDown((), key="style", size=fsize),
            ],
            [
                Sg.Push(),
                Sg.Button(cls.test_text, button_color="green", key="test"),
                Sg.Button("Save TTS config", key="save"),
                Sg.Push(),
            ],
        ]

        window = Sg.Window("Anki-VAC - TTS Config", layout, finalize=True)
        cls.window = window

        # First window update: load saved config
        cls.__update_window(window, voices, styles, config, True)

        while True:
            event, values = window.read()

            if event == Sg.WIN_CLOSED:
                break
            elif event == "accent" or event == "gender":
                # Update voice options
                window["voice"].update(
                    values=tuple(voices[values["accent"]][values["gender"]].keys())
                )
                window["style"].update(disabled=True, value="Default")

            elif event == "voice":
                # Update styles list if available
                cls.__update_window(window, voices, styles, values, False)

            elif event == "test":

                voice_code = voices[values["accent"]][values["gender"]][values["voice"]]

                thread = threading.Thread(
                    target=cls.gen_tts_audio,
                    args=(
                        voice_code,
                        "Hello, do you like my voice?",
                        values["style"],
                        True,
                    ),
                )
                thread.start()

            elif event == "save":
                voices_data["config"]["accent"] = values["accent"]
                voices_data["config"]["gender"] = values["gender"]
                voices_data["config"]["voice"] = values["voice"]
                voices_data["config"]["style"] = values["style"]

                with open("tts/english_voices.json", "w") as fp:
                    json.dump(voices_data, fp, indent=4)

                break

    @classmethod
    def __update_window(cls, window, voices, styles, values, first):

        window["voice"].update(
            value=values["voice"],
            values=tuple(voices[values["accent"]][values["gender"]].keys()),
        )

        voice_code = voices[values["accent"]][values["gender"]][values["voice"]]
        if voice_code in styles:
            window["style"].update(
                disabled=False,
                value=values["style"] if first else "Default",
                values=styles[voice_code],
            )
        else:
            window["style"].update(disabled=True, value="Default")

    @classmethod
    def gen_tts_audio(cls, voice_code, text, style="default", play=False):
        if play:
            cls.window["test"].update(text="Playing...", disabled=True)

        with open("api_keys.json", "r") as fp:
            keys = json.load(fp)

        url = "https://brazilsouth.tts.speech.microsoft.com/cognitiveservices/v1"
        req = requests.post(
            url,
            headers={
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
                "Ocp-Apim-Subscription-Key": keys["Azure"]["key"],
            },
            data="<speak version='1.0' xml:lang='en-US'>"
            + f"<voice name='{voice_code}' style='{style}'>"
            + f"{text}</voice></speak>",
        )

        name = "tts/" + str(uuid.uuid4()) + ".mp3"
        with open(name, "wb") as fp:
            fp.write(bytearray(req.content))

        if play:
            playsound(name)
            cls.window["test"].update(text=cls.test_text, disabled=False)

        # os.remove(f"{name}.mp3")

        return name


if __name__ == "__main__":
    TTSConfig.start_window()
