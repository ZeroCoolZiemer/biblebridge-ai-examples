import os
import requests
from dotenv import load_dotenv

load_dotenv()

BIBLEBRIDGE_KEY = os.getenv("BIBLEBRIDGE_KEY")


def slice_verses(center_index, radius=5):

    start = center_index - radius
    end = center_index + radius

    r = requests.get(
        "https://holybible.dev/api/slice",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={
            "start_index": start,
            "end_index": end
        }
    )

    return r.json()


def main():

    verse_index = 30174  # Hebrews 11:1

    print("\nCenter verse_index:", verse_index)
    print("Retrieving surrounding verses...\n")

    result = slice_verses(verse_index)

    for v in result["data"]:
        print(f"{v['book']['name']} {v['chapter']}:{v['verse']}  (index {v['verse_index']})")


if __name__ == "__main__":

    main()
