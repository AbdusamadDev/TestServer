import sqlite3
import random
import time
from string import ascii_letters

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()


def get_randomized_chrs():
    return "".join(random.choice(ascii_letters) for i in range(random.randint(0, 25)))


def fake_server():
    for _ in range(50):
        cursor.execute(
            "INSERT INTO android_criminalsrecords (image_path, date_recorded, camera_id, criminal_id) VALUES (?,?,?,?)",
            (
                get_randomized_chrs(),
                get_randomized_chrs(),
                random.choice([1, 2]),
                random.choice([1, 2]),
            ),
        )
        conn.commit()
    while True:
        record = cursor.execute("SELECT * FROM android_temprecords;")
        if len(record.fetchall()) == 0:
            cursor.execute("INSERT INTO android_temprecords (record_id) VALUES (1)")
            print("created")
            conn.commit()
        time.sleep(60)


if __name__ == "__main__":
    fake_server()
