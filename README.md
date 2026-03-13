# BibleBridge AI Examples

Python examples showing how to validate, canonicalize, and compute Scripture references using the BibleBridge API.

These examples show how BibleBridge can act as a reference integrity layer for AI systems. LLMs can generate Bible references, but those references may be malformed, ambiguous, or invalid. BibleBridge converts flexible human-written references into deterministic canonical coordinates before retrieval or computation occurs.

## Example Architecture
```
User Question
      ↓
LLM suggests Scripture reference
      ↓
BibleBridge /api/resolve
(reference normalization)
      ↓
Canonical span (OSIS identifier)
      ↓
BibleBridge /api/expand
(atomic verse coordinates)
      ↓
verse_index / verse_id
```

These canonical coordinates remain stable across translations and allow Scripture to be safely indexed, traversed, and analyzed.

---

## Included Examples

### 1. LLM Grounding

**`llm_grounding_demo.py`**

Demonstrates how to validate and canonicalize an LLM-generated Scripture reference.

**Pipeline:**
```
LLM → reference → /resolve → canonical span → /expand → verse coordinates
```

**Run:**
```bash
python llm_grounding_demo.py
```

**Example output:**
```
User question:
What does the Bible say about faith?

LLM suggested reference:
Hebrews 11:1

Canonical span:
Heb.11.1

Canonical coordinates (version-agnostic):

verse_id:    58011001
verse_index: 30174
book:        Hebrews
chapter:     11
verse:       1
```

---

### 2. Slice Traversal

**`slice_traversal_demo.py`**

Uses the global canonical verse index to retrieve a reading window around a verse.

**Pipeline:**
```
verse_index → /slice → surrounding verses
```

**Run:**
```bash
python slice_traversal_demo.py
```

**Example output:**
```
Center verse_index: 30174
Retrieving surrounding verses...

Hebrews 10:35  (index 30169)
Hebrews 10:36  (index 30170)
Hebrews 10:37  (index 30171)
Hebrews 10:38  (index 30172)
Hebrews 10:39  (index 30173)
Hebrews 11:1   (index 30174)
Hebrews 11:2   (index 30175)
Hebrews 11:3   (index 30176)
Hebrews 11:4   (index 30177)
Hebrews 11:5   (index 30178)
Hebrews 11:6   (index 30179)
```

---

### 3. Verse Distance

**`distance_demo.py`**

Computes the canonical verse distance between two references.

**Pipeline:**
```
reference A + reference B → /distance → verse distance
```

**Run:**
```bash
python distance_demo.py
```

**Example output:**
```
Reference A: John 3:16
Reference B: Romans 8:1

Canonical distance between references:
John.3.16 → Rom.8.1
Verse distance (global canonical index): 1981
```

---

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Copy the environment template:
```bash
cp .env.example .env
```
Then fill in your keys:
```
GROQ_API_KEY=your_api_key

BIBLEBRIDGE_KEY=your_api_key

```
- Groq API key: https://console.groq.com
- BibleBridge API key: https://holybible.dev/signup
---

## API Documentation

https://holybible.dev/api-docs

---

## About BibleBridge

BibleBridge is a deterministic Scripture infrastructure API providing:

- Reference normalization
- Canonical OSIS identifiers
- Stable verse coordinates
- Cross-translation compatibility
- Traversal and structural computation

https://holybible.dev
