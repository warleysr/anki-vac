import requests
import json


class AnkiConnect:

    ANKI_CONNECT = "http://localhost:8765"

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
        res = requests.get(cls.ANKI_CONNECT, data=json.dumps(opt)).json()
        return None if res["error"] is not None else res["result"]

