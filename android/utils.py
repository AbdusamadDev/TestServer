import socket
from geopy.distance import distance


def characters() -> list:
    letters = [chr(i) for i in list(range(97, 123)) + list(range(65, 91))]
    underscore = ["_"]
    digits = [str(k) for k in list(range(10))]
    return letters + underscore + digits


def host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        public_ip = "http://" + str(s.getsockname()[0]) + ":8000"
    except Exception:
        public_ip = "Unable to get IP"
    finally:
        s.close()
    return public_ip



def find_nearest_location(target_location, locations):
    """
    Find the nearest location in a list of locations to a target location.

    Parameters:
    - target_location: A dictionary with "longitude" and "latitude" keys.
    - locations: A list of dictionaries with "longitude" and "latitude" keys.

    Returns:
    - The nearest location as a dictionary.
    """
    target_point = (target_location["latitude"], target_location["longitude"])

    nearest_location = min(
        locations,
        key=lambda loc: distance(target_point, (loc["latitude"], loc["longitude"])).km,
    )

    return nearest_location


def check_allowed_characters(value, exception):
    lower_cases = [chr(i) for i in range(97, 123)]
    capital_cases = [chr(j) for j in range(65, 91)]
    numbers = [str(k) for k in range(10)]
    others = ["_", "'", '"']
    allowed_chrs = lower_cases + capital_cases + numbers + others
    for letter in value:
        if letter not in allowed_chrs:
            raise exception


allowed_characters = characters()
host_address = host()
is_allowed_chr = check_allowed_characters
