import json
import requests

OXFORD_API = "https://od-api.oxforddictionaries.com:443/api/v2/entries/en-gb/"
BRITANNICA_API = "https://dictionaryapi.com/api/v3/references/learners/json/"
GOOGLE_API = "https://customsearch.googleapis.com/customsearch/v1"
ANKI_CONNECT = "http://localhost:8765"

if __name__ == "__main__":
    params = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "CIMV",
                "modelName": "Básico",
                "fields": {
                    "Frente": "Frente de um card de teste.",
                    "Verso": "<b>Back</b> de um card de teste",
                },
            }
        },
    }
    req = requests.get(ANKI_CONNECT, json=params)

    print(req.json())

    """
    with open("api-keys.json", "r") as fp:
        data = json.load(fp)

    word = "horse"
    req = requests.get(
        GOOGLE_API,
        params={
            "cx": data["Google"]["cx"],
            "key": data["Google"]["key"],
            "searchType": "image",
            "imgSize": "MEDIUM",
            "q": word,
            "num": 5,
        },
    )

    data = req.json()
    with open(f"{word}.json", "w") as fp:
        json.dump(data, fp, indent=4)

    for item in data["items"]:
        print(f" {item['title']} ".center(100, "="))
        print(item["link"])
        print()

    word = "shrimp"
    req = requests.get(BRITANNICA_API + word, params={"key": data["Britannica"]["key"]})

    req = requests.get(
        OXFORD_API + "/" + word,
        headers={"app-id": data["app-id"], "app-key": data["app-key"]},
    )

    with open(f"{word}.json", "w") as fp:
        json.dump(req.json(), fp, indent=4)
    """
