import requests
import json


class AnkiConnect:

    ANKI_CONNECT = None

    @classmethod
    def get_decks(cls):
        opt = {"action": "deckNames", "version": 6}
        return cls.__api_request(opt)

    @classmethod
    def get_models(cls):
        opt = {"action": "modelNames", "version": 6}
        return cls.__api_request(opt)

    @classmethod
    def get_model_fieldnames(cls, modelname):
        opt = {
            "action": "modelFieldNames",
            "version": 6,
            "params": {"modelName": modelname},
        }
        return cls.__api_request(opt)

    @classmethod
    def add_note(cls, deck, model, data):
        opt = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck,
                    "modelName": model,
                    "fields": data["fields"],
                    "audio": [],
                    "picture": [],
                }
            },
        }

        if "audio" in data:
            opt["params"]["note"]["audio"].append(
                {
                    "path": data["audio"]["path"],
                    "fields": data["audio"]["fields"],
                    "filename": data["audio"]["filename"],
                }
            )

        if "picture" in data:
            opt["params"]["note"]["picture"].append(
                {
                    "url": data["picture"]["url"],
                    "fields": data["picture"]["fields"],
                    "filename": data["picture"]["filename"],
                }
            )

        with open("options.json", "w") as fp:
            json.dump(opt, fp, indent=4)

        return cls.__api_request(opt)

    @classmethod
    def __api_request(cls, opt):
        try:
            res = requests.get(cls.ANKI_CONNECT, data=json.dumps(opt)).json()
            return None if res["error"] is not None else res["result"]
        except Exception as e:
            pass
            # av.Logger.log(traceback.format_exc(), av.Logger.LogType.ERROR)
