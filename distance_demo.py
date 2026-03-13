import os
import requests
from dotenv import load_dotenv

load_dotenv()

BIBLEBRIDGE_KEY = os.getenv("BIBLEBRIDGE_KEY")


def verse_distance(a, b):

    r = requests.get(
        "https://holybible.dev/api/distance",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={
            "a": a,
            "b": b
        }
    )

    return r.json()


def main():

    ref_a = "John 3:16"
    ref_b = "Romans 8:1"

    print("\nReference A:", ref_a)
    print("Reference B:", ref_b)

    result = verse_distance(ref_a, ref_b)

    print("\nCanonical distance between references:\n")

    print(f"{result['a']} → {result['b']}")
    print(f"Verse distance (global canonical index): {result['distance']}")


if __name__ == "__main__":
    main()