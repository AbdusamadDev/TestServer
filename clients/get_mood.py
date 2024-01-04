import time
import requests
import json


host = "localhost:8000"

creation = requests.post(
    f"http://{host}/api/mud/",
    json={
        "longitude": "69.2401",
        "latitude": "41.2995",
    },
)
print("Client created: ", creation.json())
print(creation.status_code)
# Tashkent
while True:
    try:
        print(
            requests.get(
                f"http://{host}/api/mud/",
                headers={
                    "longitude": "69.2401",
                    "latitude": "41.2995",
                },
            ).json(),
        )
        time.sleep(3)
    except KeyboardInterrupt:
        requests.delete(
            f"http://{host}/api/mud/"
            + str(creation.json().get("client_pk"))
        )
        break
