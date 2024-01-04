from django.apps import AppConfig
import multiprocessing
import sqlite3
import random
import time
from string import ascii_letters
from django.db.backends.signals import connection_created
from django.dispatch import receiver


def fake_server():
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()

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
            print("sleep here")

            record = cursor.execute("SELECT * FROM android_temprecords;")
            if len(record.fetchall()) == 0:
                cursor.execute("INSERT INTO android_temprecords (record_id) VALUES (1)")
                print("created at", time.strftime("%Y-%m-%d %H:%M:%S"))
                conn.commit()
            time.sleep(30)


def get_randomized_chrs():
    return "".join(random.choice(ascii_letters) for i in range(random.randint(0, 25)))


class AndroidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "android"

    def ready(self):
        multiprocessing.Process(target=fake_server).start()
