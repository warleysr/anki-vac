import requests
import json
from abc import ABC


class API(ABC):

    KEYS = None

    @classmethod
    def start(cls):
        with open("api_keys.json", "r") as fp:
            cls.KEYS = json.load(fp)


class BingImageAPI(API):

    BING_API = None

    @classmethod
    def get_image_links(cls, query, size="medium", count=5):
        req = requests.get(
            cls.BING_API,
            params={"q": query, "size": size, "count": count, "mkt": "en-US"},
            headers={"Ocp-Apim-Subscription-Key": super().KEYS["Azure"]["bing"]},
        )
        data = req.json()

        return tuple(value["contentUrl"] for value in data["value"])


class OxfordAPI(API):

    OXFORD_API = None

    @classmethod
    def get_definition(cls, word):
        req = requests.get(
            cls.OXFORD_API + word,
            headers={
                "app-id": super().KEYS["Oxford"]["app-id"],
                "app-key": super().KEYS["Oxford"]["app-key"],
            },
        )
        return req.json()


class BritannicaAPI(API):

    BRITANNICA_API = None

    @classmethod
    def get_definition(cls, word):
        req = requests.get(
            cls.BRITANNICA_API + word, params={"key": super().KEYS["Britannica"]["key"]}
        )
        return req.json()
