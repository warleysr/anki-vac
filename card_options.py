import PySimpleGUI as Sg
from anki_connect import AnkiConnect


class CardOptions:
    @classmethod
    def start_window(cls):
        ffont = "Arial 12 bold"

        decks = AnkiConnect.get_decks()
        if decks is None:
            Sg.PopupError(
                "No decks were found. Create one in Anki.", title="Anki-VAC", font=ffont
            )
            return

        models = AnkiConnect.get_models()
        if models is None:
            Sg.PopupError(
                "No models were found. Create one in Anki.",
                title="Anki-VAC",
                font=ffont,
            )
            return

        layout = [
            [
                Sg.Push(),
                Sg.Text("Select a deck and a model", font="Arial 16 bold"),
                Sg.Push(),
            ],
            [
                Sg.Text("Deck: ", font=ffont),
                Sg.Push(),
                Sg.Text("Model: ", font=ffont),
                Sg.Push(),
            ],
            [
                Sg.Listbox(decks, key="deck", size=(30, 5)),
                Sg.Listbox(models, key="model", size=(30, 5)),
            ],
            [
                Sg.Push(),
                Sg.Button("Configure card", key="config", font=ffont),
                Sg.Push(),
            ],
        ]

        window = Sg.Window("Anki-VAC - Card options", layout)

        while True:
            event, values = window.read()

            if event == Sg.WIN_CLOSED:
                break
            elif event == "config":
                deck = values["deck"]
                model = values["model"]

                if len(deck) == 0 or len(model) == 0:
                    Sg.PopupError(
                        "Select a deck and a model.", title="Anki-VAC", font=ffont
                    )
                else:
                    deck = deck[0]
                    model = model[0]
                    fields = AnkiConnect.get_model_fieldnames(model)
                    if fields is None or len(fields) == 0:
                        Sg.PopupError(
                            "The selected model doesn't have any field.",
                            title="Anki-VAC",
                            font=ffont,
                        )
                    else:
                        cls.__card_config(window, fields)

    @classmethod
    def __card_config(cls, parent_window, fields):
        ffont = "Arial 12 bold"
        layout = [
            [
                Sg.Push(),
                Sg.Text("Configure your flashcard", font="Arial 16 bold"),
                Sg.Push(),
            ]
        ]

        for field in fields:
            layout.append([Sg.Text(f"{field}:", font=ffont)])
            layout.append([Sg.Multiline(size=(50, 8))])

        layout.append(
            [
                Sg.Push(),
                Sg.Button("Save card config", key="save", font=ffont),
                Sg.Push(),
            ]
        )

        window = Sg.Window("Anki-VAC - Card options", layout)

        while True:
            event, values = window.read()

            if event == Sg.WIN_CLOSED:
                break
            elif event == "save":
                window.close()
                parent_window.close()
                break
