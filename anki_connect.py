import requests
import json
import traceback


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
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": deck,
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
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
                    "path": data["picture"]["path"],
                    "fields": data["picture"]["fields"],
                    "filename": data["picture"]["filename"],
                }
            )

        return cls.__api_request(opt)

    @classmethod
    def __api_request(cls, opt):
        try:
            res = requests.get(cls.ANKI_CONNECT, data=json.dumps(opt)).json()
            return None if res["error"] is not None else res["result"]
        except Exception as e:
            import anki_vac as av
            av.Logger.log(traceback.format_exc(), av.Logger.LogType.ERROR)
