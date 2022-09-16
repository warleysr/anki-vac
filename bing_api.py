import requests
import json


class BingImageAPI:

    BING_API = None

    @classmethod
    def get_image_links(cls, query, size="medium", count=5):
        with open("api_keys.json", "r") as fp:
            keys = json.load(fp)

        req = requests.get(
            cls.BING_API,
            params={"q": query, "size": size, "count": count},
            headers={"Ocp-Apim-Subscription-Key": keys["Azure"]["bing"]},
        )
        data = req.json()

        return tuple(value["contentUrl"] for value in data["value"])


if __name__ == "__main__":
    print(BingImageAPI.get_image_links("horse"))
