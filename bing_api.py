import requests


class BingImageAPI:

    BING_API = None
    BING_KEY = None

    @classmethod
    def get_image_links(cls, query, size="medium", count=5):
        req = requests.get(
            cls.BING_API,
            params={
                "q": query,
                "size": size,
                "count": count,
                "mkt": "en-US",
                "imageType": "Photo",
            },
            headers={"Ocp-Apim-Subscription-Key": cls.BING_KEY},
        )
        data = req.json()

        return tuple(value["contentUrl"] for value in data["value"])
