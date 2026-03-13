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
                "content": "Return ONLY a single Bible reference. Example: John 3:16"
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


def expand_reference(osis):
    r = requests.get(
        "https://holybible.dev/api/expand",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={"reference": osis}
    )
    return r.json()


def fetch_passage(reference):
    r = requests.get(
        "https://holybible.dev/api/passage",
        headers={"Authorization": f"Bearer {BIBLEBRIDGE_KEY}"},
        params={
            "reference": reference,
            "version": "KJV"
        }
    )
    return r.json()


def main():
    question = "What does the Bible say about faith?"

    print("\nUser question:")
    print(question)

    # Step 1 — LLM suggests reference
    reference = get_reference_from_llm(question)

    print("\n--- AI Suggested Reference ---")
    print(reference)

    # Step 2 — Canonical validation
    resolved = resolve_reference(reference)

    if not resolved.get("valid"):
        print("\nReference failed canonical validation:")
        print(resolved)
        return

    osis = resolved["osis_id"]

    print("\n--- Canonical OSIS Span ---")
    print(osis)

    if resolved.get("references"):
        confidence = resolved["references"][0].get("confidence")
        if confidence:
            print(f"\nResolver confidence: {confidence}")

    # Step 3 — Expand to canonical coordinates
    expanded = expand_reference(osis)

    if expanded.get("status") != "success":
        print("\nExpand failed:")
        print(expanded)
        return

    first = expanded["data"][0]

    print("\n--- Canonical Coordinates ---")
    print(f"verse_id:    {first['verse_id']}")
    print(f"verse_index: {first['verse_index']}")
    print(f"book:        {first['book']['name']}")
    print(f"chapter:     {first['chapter']}")
    print(f"verse:       {first['verse']}")
    print(f"\nVerse count: {expanded['verse_count']}")

    # Step 4 — Retrieve verified scripture using validated OSIS
    passage = fetch_passage(osis)

    if passage.get("status") != "success":
        print("\nPassage retrieval failed:")
        print(passage)
        return

    print("\n--- Verified Scripture ---\n")

    verses = passage["data"]

    for v in verses:
        print(f"{v['book']} {v['chapter']}:{v['verse']}")
        print(v["text"])
        print()


if __name__ == "__main__":
    main()