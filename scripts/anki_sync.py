#!/usr/bin/env python3
"""
Push flashcards to Anki via AnkiConnect (https://localhost:8765).

Anki Desktop must be running with the AnkiConnect add-on (code 2055492159)
installed. This script does NOT decide what content goes on a card — Claude
builds the card fields (front/back text, examples, cloze sentences) and
passes them in; this script only talks to AnkiConnect and reports back the
Anki note ID so profile.py can record it (anki-mark-word / anki-mark-mistake).

Usage:
    python3 anki_sync.py ping
    python3 anki_sync.py add-basic --deck "English" --front "obsolete" --back "устаревший<br><br>Example: This API is obsolete." [--tags tag1,tag2] [--reversed]
    python3 anki_sync.py add-cloze --deck "English" --text "The model started to {{c1::overfit}} after epoch 40." --back-extra "overfit — переобучаться" [--tags tag1,tag2]
    python3 anki_sync.py add-batch --file cards.json   # bulk add, see format below

add-batch expects a JSON file: a list of objects, each either
    {"type": "basic", "front": "...", "back": "...", "reversed": true, "tags": [...]}
or
    {"type": "cloze", "text": "...", "back_extra": "...", "tags": [...]}

All output is JSON on stdout: {"status": "ok", "note_id": 12345} per card,
or {"status": "error", "message": "..."} — including "duplicate" for cards
AnkiConnect refuses because an identical note already exists (this is
expected/safe when re-running after a partial failure, not a real error).
"""
import json
import sys
import urllib.request

ANKI_CONNECT_URL = "http://localhost:8765"
DEFAULT_DECK = "English"


def invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return None, f"could not reach AnkiConnect at {ANKI_CONNECT_URL} — is Anki Desktop running with the AnkiConnect add-on? ({e})"
    if body.get("error"):
        return None, body["error"]
    return body.get("result"), None


def ensure_deck(deck):
    invoke("createDeck", deck=deck)


def cmd_ping():
    result, error = invoke("version")
    if error:
        print(json.dumps({"status": "error", "message": error}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps({"status": "ok", "anki_connect_version": result}, ensure_ascii=False))


def build_basic_note(deck, front, back, reversed_card=False, tags=None):
    model = "Basic (and reversed card)" if reversed_card else "Basic"
    return {
        "deckName": deck,
        "modelName": model,
        "fields": {"Front": front, "Back": back},
        "options": {"allowDuplicate": False},
        "tags": tags or []
    }


def build_cloze_note(deck, text, back_extra="", tags=None):
    return {
        "deckName": deck,
        "modelName": "Cloze",
        "fields": {"Text": text, "Back Extra": back_extra},
        "options": {"allowDuplicate": False},
        "tags": tags or []
    }


def add_note(note):
    ensure_deck(note["deckName"])
    result, error = invoke("addNote", note=note)
    if error:
        if "duplicate" in str(error).lower():
            print(json.dumps({"status": "duplicate", "message": error}, ensure_ascii=False))
            return
        print(json.dumps({"status": "error", "message": error}, ensure_ascii=False))
        return
    print(json.dumps({"status": "ok", "note_id": result}, ensure_ascii=False))


def cmd_add_basic(args):
    deck = DEFAULT_DECK
    front = back = None
    reversed_card = False
    tags = []
    i = 0
    while i < len(args):
        if args[i] == "--deck":
            deck = args[i + 1]; i += 2
        elif args[i] == "--front":
            front = args[i + 1]; i += 2
        elif args[i] == "--back":
            back = args[i + 1]; i += 2
        elif args[i] == "--tags":
            tags = [t.strip() for t in args[i + 1].split(",") if t.strip()]; i += 2
        elif args[i] == "--reversed":
            reversed_card = True; i += 1
        else:
            i += 1
    if not front or not back:
        print(json.dumps({"status": "error", "message": "usage: add-basic --front X --back Y [--deck D] [--tags a,b] [--reversed]"}, ensure_ascii=False))
        sys.exit(1)
    add_note(build_basic_note(deck, front, back, reversed_card, tags))


def cmd_add_cloze(args):
    deck = DEFAULT_DECK
    text = None
    back_extra = ""
    tags = []
    i = 0
    while i < len(args):
        if args[i] == "--deck":
            deck = args[i + 1]; i += 2
        elif args[i] == "--text":
            text = args[i + 1]; i += 2
        elif args[i] == "--back-extra":
            back_extra = args[i + 1]; i += 2
        elif args[i] == "--tags":
            tags = [t.strip() for t in args[i + 1].split(",") if t.strip()]; i += 2
        else:
            i += 1
    if not text or "{{c1::" not in text:
        print(json.dumps({"status": "error", "message": "usage: add-cloze --text 'sentence with {{c1::word}}' [--back-extra Y] [--deck D] [--tags a,b]"}, ensure_ascii=False))
        sys.exit(1)
    add_note(build_cloze_note(deck, text, back_extra, tags))


def cmd_add_batch(path):
    with open(path, "r", encoding="utf-8") as f:
        cards = json.load(f)
    notes = []
    for c in cards:
        deck = c.get("deck", DEFAULT_DECK)
        tags = c.get("tags", [])
        if c["type"] == "basic":
            notes.append(build_basic_note(deck, c["front"], c["back"], c.get("reversed", False), tags))
        elif c["type"] == "cloze":
            notes.append(build_cloze_note(deck, c["text"], c.get("back_extra", ""), tags))
        else:
            print(json.dumps({"status": "error", "message": f"unknown card type '{c['type']}'"}, ensure_ascii=False))
            sys.exit(1)
    for deck in {n["deckName"] for n in notes}:
        ensure_deck(deck)
    result, error = invoke("addNotes", notes=notes)
    if error:
        print(json.dumps({"status": "error", "message": error}, ensure_ascii=False))
        sys.exit(1)
    # addNotes returns a list of note IDs, with null for duplicates/failures
    output = []
    for card, note_id in zip(cards, result):
        if note_id is None:
            output.append({"status": "duplicate_or_failed", "card": card})
        else:
            output.append({"status": "ok", "note_id": note_id, "card": card})
    print(json.dumps({"status": "ok", "results": output}, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "no command given"}, ensure_ascii=False))
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "ping":
        cmd_ping()
    elif cmd == "add-basic":
        cmd_add_basic(args)
    elif cmd == "add-cloze":
        cmd_add_cloze(args)
    elif cmd == "add-batch":
        if "--file" not in args:
            print(json.dumps({"status": "error", "message": "usage: add-batch --file cards.json"}, ensure_ascii=False))
            sys.exit(1)
        cmd_add_batch(args[args.index("--file") + 1])
    else:
        print(json.dumps({"status": "error", "message": f"unknown command '{cmd}'"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
