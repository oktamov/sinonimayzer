import requests

API_URL = "https://api-inference.huggingface.co/models/Mokhiya/syn-roberta"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


print(query('hello !'))
