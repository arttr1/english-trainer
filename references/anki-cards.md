# Anki Flashcards

Reference for pushing flashcards to the user's Anki collection. Loaded by `english-trainer` SKILL.md when the user asks for Anki cards, says "добавь в анки", "сделай карточки", or when a vocab/mistake session naturally produces material worth spaced-repeating outside this skill's own `profile.py` queue.

## Why this exists

`profile.py` already does lightweight spaced repetition inside the coaching conversation, but the user wants real cards in their own Anki collection — reviewable on the phone (AMGI, synced via AnkiWeb) or the desktop, independent of whether they're chatting with Claude. This file is additive, not a replacement: keep logging to `profile.py` as usual (see `vocabulary.md`, `grammar-drills.md`), and push to Anki on top of that when the user wants it.

## Setup this relies on

- **Anki Desktop** running locally with the **AnkiConnect** add-on (code `2055492159`) installed. AnkiConnect listens on `http://localhost:8765`.
- A deck named **"English"** (already created). Don't create more decks unless the user asks — they explicitly chose one flat deck over subdecks.
- The user syncs that Anki Desktop profile to AnkiWeb, and reviews from **AMGI** on iPhone or Anki Desktop directly — Anki Desktop must be running (even in the background) for the sync script to reach it, but the user does not need to be looking at it.

If `python3 scripts/anki_sync.py ping` fails, Anki Desktop probably isn't running. Tell the user plainly ("Anki's not running — open it and I'll retry") rather than silently failing or queuing forever.

## Card types — mix Basic and Cloze, per the user's preference

The user wants both formats mixed, not one or the other:

- **Basic reversed, custom model "Basic RU-EN with Example"** — for standalone vocabulary: Front is the English word (+ pronunciation), Back is the Russian translation, Example is a separate field with a natural example sentence. `anki_sync.py`'s `--reversed` flag uses this model automatically (and creates it via AnkiConnect on first use if it doesn't exist yet) — never pass `--reversed` while also stuffing the example into `--back`. Use this for most vocabulary.
- **Cloze** — for a word learned *in context* (e.g. harvested from tech-reading, or a grammar-mistake pattern), where testing recall inside a real sentence is more valuable than an isolated word→translation pair. Put the target word/phrase as `{{c1::...}}` in the sentence; put the translation + any note in "Back Extra".

Rule of thumb: word came from a themed vocab list or was quizzed in isolation → Basic reversed. Word/phrase came from a real sentence (an article, a mistake example, a cloze drill you already ran) → Cloze, reusing that sentence.

**Do not use the stock "Basic (and reversed card)" note type.** Its Card 2 (RU→EN) template renders the *entire* Back field as the question — so if Back holds `translation<br><br>Example: <English sentence containing the answer>`, Card 2 shows the English answer right there in the question, spoiling itself before the user even tries to recall it. This was caught and fixed once already (all affected cards migrated to the custom model) — don't reintroduce it. Always pass the example as its own `--example` (CLI) / `"example"` (batch JSON) field, never appended into `back`.

## What becomes a card — three sources, all in scope

### 1. Vocabulary queue (`profile.json` → `vocabulary`)
Any word tracked there is a candidate. Use:
```bash
python3 scripts/profile.py anki-pending --kind vocab
```
This returns vocab entries with no `anki_note_id` yet — i.e. never pushed. Don't re-push words that already have one (that's what the field is for — check it, don't just re-run everything).

For each word, build:
- **Front:** `word /IPA/ (russian-letters, stress marked)` — reuse the pronunciation format from `vocabulary.md`, don't invent a new one.
- **Back:** Russian translation (keep it to the translation — don't fold the example in here for reversed cards, see the warning above).
- **Example:** a natural example sentence, ideally mentioning the word's topic if it fits naturally rather than appending "Topic: X" as a separate line.

### 2. New words from tech-reading
When `tech-reading.md`'s vocabulary-harvest step pulls words from a real article/doc, and the user wants them in Anki too, prefer **Cloze** using the actual sentence from the source material (or a close paraphrase if the original is long) — this preserves the real context, which is the whole point of harvesting from reading rather than a word list.

### 3. Grammar mistakes (`profile.json` → `mistakes`)
```bash
python3 scripts/profile.py anki-pending --kind mistake
```
For a recurring mistake category, make a **Cloze** card out of the corrected example: put the corrected form in `{{c1::...}}`, and put the wrong version + a one-line rule reminder in "Back Extra". E.g. for "modal + to":
- Text: `I {{c1::should fix}} it before the demo.`
- Back Extra: `Wrong: "I should to fix it" — modals (should/can/must/will) never take "to".`

Only make a mistake card for a category worth drilling repeatedly (count ≥ 2, or the user explicitly asks) — a one-off slip doesn't need a permanent flashcard.

## The push workflow

1. Decide what to push (ask the user, or use `anki-pending` if they just said "добавь то, что накопилось").
2. Check Anki is reachable: `python3 scripts/anki_sync.py ping`. If it fails, stop and tell the user.
3. For a handful of cards, add them one at a time:
   ```bash
   python3 scripts/anki_sync.py add-basic --front "..." --back "..." --example "..." --tags "vocab,<topic>" --reversed
   python3 scripts/anki_sync.py add-cloze --text "...{{c1::word}}..." --back-extra "..." --tags "vocab,<topic>"
   ```
   For a batch (e.g. pushing a whole backlog), write a JSON file to the skill's scratch area and use `add-batch --file <path>` instead of many individual calls — check the format in `anki_sync.py`'s docstring.
4. Each successful add returns `{"status": "ok", "note_id": N}`. Immediately record that back into the profile so it isn't re-pushed next time:
   ```bash
   python3 scripts/profile.py anki-mark-word "<word>" "<note_id>"
   python3 scripts/profile.py anki-mark-mistake "<category>" "<note_id>"
   ```
5. A `"status": "duplicate"` result means AnkiConnect already has an identical note (e.g. from a previous partial run) — treat this as success, not an error, but still mark it in the profile so future runs skip it cleanly (you won't have a real note_id in this case; marking with `"synced"` as a placeholder is fine — the point is just to stop re-attempting it).

## Tagging convention

Always tag cards so the user can filter/browse them in Anki later:
- `vocab` or `mistake` (source type)
- the topic (e.g. `pep8`, `ml`, `distributed-systems`) or the mistake category slug (e.g. `articles`, `modal-to`)

Keep tags lowercase, hyphenated, no spaces — Anki splits tags on whitespace.

## Batch size and pacing

Same principle as `vocabulary.md`: don't dump 50 cards on the user in one push just because the queue has that many. When the user says "закинь всё, что накопилось", pushing everything is fine (that's their instruction), but when *you're* deciding proactively at the end of a session, stick to what was actually covered in that session — 5-15 cards, not the entire historical backlog.

## Don't narrate the mechanics

Same rule as the rest of this skill: run the sync commands, confirm briefly ("added 8 cards to your English deck — obsolete, comprise, the overfit cloze, and 5 more"), don't walk the user through every JSON response.
