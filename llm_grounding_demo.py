import os
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

BIBLEBRIDGE_KEY = os.getenv("BIBLEBRIDGE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def get_reference_from_llm(question):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Return ONLY a single valid Bible reference. Example: John 3:16"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def resolve_reference(reference):
    r = requests.get(
        "https://holybible.dev/api/resolve",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={"reference": reference}
    )

    return r.json()


def expand_reference(reference):
    r = requests.get(
        "https://holybible.dev/api/expand",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={"reference": reference}
    )

    return r.json()


def main():

    question = "What does the Bible say about faith?"

    print("\nUser question:")
    print(question)

    reference = get_reference_from_llm(question)

    print("\nLLM suggested reference:")
    print(reference)

    resolved = resolve_reference(reference)

    if not resolved.get("valid"):
        print("\nReference failed validation:")
        print(resolved)
        return

    osis = resolved["osis_id"]

    print("\nCanonical span:")
    print(osis)

    expanded = expand_reference(osis)

    verse = expanded["data"][0]

    print("\nCanonical coordinates (version-agnostic):\n")

    print(f"verse_id:    {verse['verse_id']}")
    print(f"verse_index: {verse['verse_index']}")
    print(f"book:        {verse['book']}")
    print(f"chapter:     {verse['chapter']}")
    print(f"verse:       {verse['verse']}")


if __name__ == "__main__":
    main()