import requests


print(
    requests.get(
        "http://androidserver.pythonanywhere.com/api/mud/",                headers={
                    "longitude": "69.2401",
                    "latitude": "41.2995",
                },
    ).json()
)