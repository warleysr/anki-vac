import PySimpleGUI as Sg
from anki_connect import AnkiConnect
from bing_api import BingImageAPI
from card_creator import CardCreator
from card_options import CardOptions
from tts.tts_config import TTSConfig
import json
import threading


class GraphicInterface:
    @classmethod
    def start_main(cls, config):
        Sg.theme("Reddit")

        ffont = "Arial 12 bold"

        menu_opt = [["Options", ["Card options", "TTS config", "APIs config"]]]

        layout = [
            [Sg.Menubar(menu_opt)],
            [
                Sg.Push(),
                Sg.Text("Anki-VAC", font="Arial 20 bold", text_color="green"),
                Sg.Push(),
            ],
            [
                Sg.Text("Deck: ", font=ffont),
                Sg.Text(config["deck"], font=ffont, text_color="red"),
            ],
            [
                Sg.Text("Model: ", font=ffont),
                Sg.Text(config["model"], font=ffont, text_color="red"),
            ],
            [Sg.Text("Words to add: ", font=ffont)],
            [Sg.Multiline(size=(60, 15), key="words")],
            [
                Sg.Push(),
                Sg.Button("Add to my vocabulary", font=ffont, key="add"),
                Sg.Push(),
            ],
            [
                Sg.StatusBar(
                    "Waiting input words",
                    key="status",
                    size=(2, 1),
                ),
                Sg.ProgressBar(0, key="progress", size=(20, 20)),
            ],
            [Sg.Push()],
        ]

        window = Sg.Window("Anki-VAC", layout)

        while True:
            event, values = window.read()

            if event == Sg.WIN_CLOSED:
                break
            elif event == "add":
                window["words"].update(disabled=True)
                window["add"].update(disabled=True)

                words = set(values["words"].split("\n"))
                threading.Thread(
                    target=CardCreator.bulk_card_creation,
                    args=(
                        config,
                        words,
                        window,
                    ),
                    daemon=True,
                ).start()

            elif event == "Card options":
                CardOptions.start_window(config)
            elif event == "TTS config":
                TTSConfig.start_window()
            elif event == "APIs config":
                cls.start_apis_config_window(config)
            elif event == "-THREAD-":
                i = values["-THREAD-"][0]
                nwords = values["-THREAD-"][1]

                window["status"].update(value=f"Processing words... ({i + 1}/{nwords})")
                window["progress"].update(current_count=i + 1, max=nwords)
            elif event == "-FINISH-":
                count = values["-FINISH-"][0]
                fails = values["-FINISH-"][1]

                cls.finish_popup(window, count, fails)

    @classmethod
    def start_apis_config_window(cls, config):
        ffont = "Arial 10 bold"

        s = (55, 10)

        layout = [
            [
                Sg.Text("AnkiConnect: ", font=ffont),
                Sg.Push(),
                Sg.InputText(AnkiConnect.ANKI_CONNECT, key="ankiend", size=s),
            ],
            [
                Sg.Text("TTS endpoint: ", font=ffont),
                Sg.Push(),
                Sg.InputText(TTSConfig.TTS_API, key="ttsend", size=s),
            ],
            [
                Sg.Text("Bing endpoint: ", font=ffont),
                Sg.Push(),
                Sg.InputText(BingImageAPI.BING_API, key="bingend", size=s),
            ],
            [
                Sg.Text("TTS key: ", font=ffont),
                Sg.Push(),
                Sg.InputText(TTSConfig.TTS_KEY, key="ttskey", size=s),
            ],
            [
                Sg.Text("Bing key: ", font=ffont),
                Sg.Push(),
                Sg.InputText(BingImageAPI.BING_KEY, key="bingkey", size=s),
            ],
            [
                Sg.Push(),
                Sg.Button("Save APIs config", font=ffont, key="save"),
                Sg.Push(),
            ],
        ]

        window = Sg.Window("Anki-VAC - APIs config", layout)

        while True:
            event, values = window.read()

            if event == Sg.WIN_CLOSED:
                break
            elif event == "save":
                config["apis-urls"]["ANKI_CONNECT"] = values["ankiend"]
                config["apis-urls"]["BING_API"] = values["bingend"]
                config["apis-urls"]["TTS_API"] = values["ttsend"]
                config["apis-keys"]["TTS"] = values["ttskey"]
                config["apis-keys"]["BING"] = values["bingkey"]

                AnkiConnect.ANKI_CONNECT = values["ankiend"]
                BingImageAPI.BING_API = values["bingend"]
                TTSConfig.TTS_API = values["ttsend"]
                TTSConfig.TTS_KEY = values["ttskey"]
                BingImageAPI.BING_KEY = values["bingkey"]

                with open("config.json", "w", encoding="utf-8") as fp:
                    json.dump(config, fp, indent=4)

                window.close()
                break

    @classmethod
    def finish_popup(cls, window, count, fails):
        window["status"].update(value="Finished")
        window["words"].update(value="")
        window["words"].update(disabled=False)
        window["add"].update(disabled=False)

        Sg.PopupOK(
            f"{count} new flashcards were added to Anki!"
            + f" {fails} failed. See log.txt for details.",
            title="Anki-VAC",
        )
