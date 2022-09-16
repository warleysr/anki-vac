import requests
import json

# import anki_vac as av
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
    def __api_request(cls, opt):
        try:
            res = requests.get(cls.ANKI_CONNECT, data=json.dumps(opt)).json()
            return None if res["error"] is not None else res["result"]
        except Exception as e:
            pass
            # av.Logger.log(traceback.format_exc(), av.Logger.LogType.ERROR)
