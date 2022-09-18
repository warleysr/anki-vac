import PySimpleGUI as Sg
from playsound import playsound
import json
import requests
import threading
import uuid
import os


class TTSConfig:

    TTS_API = None
    TTS_KEY = None

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
                Sg.Button(
                    cls.test_text,
                    font=font,
                    button_color="green",
                    disabled_button_color=("white", None),
                    key="test",
                ),
                Sg.Button("Save TTS config", font=font, key="save"),
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

                window.close()
                window = None
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

        ssml = (
            "<speak version='1.0' xml:lang='en-US'>"
            + f"<voice name='{voice_code}' style='{style}'>"
            + f"{text}</voice></speak>"
        )

        req = requests.post(
            cls.TTS_API,
            headers={
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
                "Ocp-Apim-Subscription-Key": cls.TTS_KEY,
            },
            data=ssml.encode("utf-8"),
        )

        name = "tts/" + str(uuid.uuid4()) + ".mp3"
        with open(name, "wb") as fp:
            fp.write(bytearray(req.content))

        if play:
            playsound(name)
            os.remove(name)
            cls.window["test"].update(text=cls.test_text, disabled=False)

        return name

    @classmethod
    def get_voice_code_config(cls):
        with open("tts/english_voices.json", "r") as fp:
            data = json.load(fp)
            config = data["config"]
        return data["voices"][config["accent"]][config["gender"]][config["voice"]]
