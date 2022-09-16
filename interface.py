import PySimpleGUI as Sg
from card_options import CardOptions
from tts.tts_config import TTSConfig


class GraphicInterface:
    @classmethod
    def start_main(cls, config):
        Sg.theme("Reddit")

        ffont = "Arial 12 bold"

        menu_opt = [["Options", ["Card options", "TTS config", "API keys"]]]

        layout = [
            [Sg.Menubar(menu_opt)],
            [
                Sg.Push(),
                Sg.Text("Anki-VAC", font="Arial 20 bold", text_color="green"),
                Sg.Push(),
            ],
            [
                Sg.Text("Deck: ", font=ffont),
                Sg.Text(config["options"]["deck"], font=ffont, text_color="red"),
            ],
            [
                Sg.Text("Model: ", font=ffont),
                Sg.Text(config["options"]["model"], font=ffont, text_color="red"),
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

                nwords = len(values["words"].split("\n"))
                count = 1

                while count <= nwords:
                    window["status"].update(
                        value=f"Processing words... ({count}/{nwords})"
                    )
                    window["progress"].update(current_count=count, max=nwords)
                    time.sleep(1)
                    count += 1

                window["status"].update(value="Finished")
                window["words"].update(value="")
                window["words"].update(disabled=False)
                window["add"].update(disabled=False)

                Sg.PopupOK(
                    f"{nwords} new flashcards were added to Anki!", title="Anki-VAC"
                )

            elif event == "TTS config":
                TTSConfig.start_window()
            elif event == "Card options":
                CardOptions.start_window()
