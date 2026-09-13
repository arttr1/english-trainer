#!/usr/bin/env python3
"""
Manage the learner profile for the english-trainer skill.

The profile is a single JSON file that persists across sessions. It tracks:
- estimated CEFR level (overall + per-skill)
- recurring grammar mistakes (with counts, so we know what's actually frequent)
- vocabulary queue (spaced-repetition-ish: new / learning / known)
- session log (lightweight history so Claude can say "last time we worked on X")

Usage:
    python3 profile.py init                          # create profile if missing
    python3 profile.py show                           # print full profile as JSON
    python3 profile.py add-mistake "<category>" "<note>"
    python3 profile.py add-words "word1,word2,word3" [--topic "devops"]
    python3 profile.py review-words [--n 10]           # get words due for review
    python3 profile.py mark-word "<word>" "<known|learning|forgot>"
    python3 profile.py log-session "<mode>" "<summary>"
    python3 profile.py set-level "<skill>" "<level>"    # skill: overall|reading|listening|writing|speaking|grammar|vocab

    python3 profile.py anki-pending [--kind vocab|mistake|all]   # items not yet sent to Anki
    python3 profile.py anki-mark-word "<word>" "<note_id>"       # record word was pushed to Anki
    python3 profile.py anki-mark-mistake "<category>" "<note_id>" [--index N]  # record mistake example was pushed

All output is JSON on stdout so Claude can parse it directly.
"""
import json
import sys
import os
from datetime import datetime, timezone

PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "profile.json")
PROFILE_PATH = os.path.normpath(PROFILE_PATH)

DEFAULT_PROFILE = {
    "created_at": None,
    "updated_at": None,
    "levels": {
        "overall": "unknown",
        "reading": "unknown",
        "listening": "unknown",
        "writing": "unknown",
        "speaking": "unknown",
        "grammar": "unknown",
        "vocabulary": "unknown"
    },
    "feedback_language": "en-with-ru-on-request",
    "mistakes": [],
    "vocabulary": [],
    "sessions": [],
    "stats": {
        "total_sessions": 0,
        "total_words_tracked": 0,
        "total_mistakes_logged": 0
    }
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return None
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(profile):
    profile["updated_at"] = now_iso()
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def cmd_init():
    profile = load_profile()
    if profile is not None:
        print(json.dumps({"status": "exists", "profile": profile}, ensure_ascii=False, indent=2))
        return
    profile = json.loads(json.dumps(DEFAULT_PROFILE))  # deep copy
    profile["created_at"] = now_iso()
    save_profile(profile)
    print(json.dumps({"status": "created", "profile": profile}, ensure_ascii=False, indent=2))


def cmd_show():
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    print(json.dumps(profile, ensure_ascii=False, indent=2))


def cmd_set_level(skill, level):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    if skill not in profile["levels"]:
        print(json.dumps({"status": "error", "message": f"unknown skill '{skill}', valid: {list(profile['levels'].keys())}"}, ensure_ascii=False))
        return
    profile["levels"][skill] = level
    save_profile(profile)
    print(json.dumps({"status": "updated", "levels": profile["levels"]}, ensure_ascii=False, indent=2))


def cmd_add_mistake(category, note):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    # Check if this category already exists, bump count instead of duplicating
    for m in profile["mistakes"]:
        if m["category"].lower() == category.lower():
            m["count"] += 1
            m["last_seen"] = now_iso()
            m["examples"].append(note)
            m["examples"] = m["examples"][-5:]  # keep last 5 examples only
            save_profile(profile)
            print(json.dumps({"status": "incremented", "mistake": m}, ensure_ascii=False, indent=2))
            return
    new_mistake = {
        "category": category,
        "count": 1,
        "first_seen": now_iso(),
        "last_seen": now_iso(),
        "examples": [note],
        "anki_note_id": None,
        "anki_synced_at": None
    }
    profile["mistakes"].append(new_mistake)
    profile["stats"]["total_mistakes_logged"] += 1
    save_profile(profile)
    print(json.dumps({"status": "created", "mistake": new_mistake}, ensure_ascii=False, indent=2))


def cmd_add_words(words_csv, topic=None):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    words = [w.strip() for w in words_csv.split(",") if w.strip()]
    existing = {w["word"].lower() for w in profile["vocabulary"]}
    added = []
    for w in words:
        if w.lower() in existing:
            continue
        entry = {
            "word": w,
            "topic": topic or "general",
            "status": "new",
            "added_at": now_iso(),
            "last_reviewed": None,
            "review_count": 0,
            "correct_streak": 0,
            "anki_note_id": None,
            "anki_synced_at": None
        }
        profile["vocabulary"].append(entry)
        added.append(entry)
    profile["stats"]["total_words_tracked"] = len(profile["vocabulary"])
    save_profile(profile)
    print(json.dumps({"status": "added", "added": added, "skipped_duplicates": len(words) - len(added)}, ensure_ascii=False, indent=2))


def cmd_review_words(n=10):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    # Priority: new words first, then "learning" with lowest correct_streak, then oldest last_reviewed
    def sort_key(w):
        status_priority = {"new": 0, "learning": 1, "known": 2}
        return (
            status_priority.get(w["status"], 3),
            w["correct_streak"],
            w["last_reviewed"] or ""
        )
    candidates = [w for w in profile["vocabulary"] if w["status"] != "known" or w["correct_streak"] < 3]
    candidates.sort(key=sort_key)
    selected = candidates[:n]
    print(json.dumps({"status": "ok", "words": selected, "total_in_queue": len(candidates)}, ensure_ascii=False, indent=2))


def cmd_mark_word(word, result):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    for w in profile["vocabulary"]:
        if w["word"].lower() == word.lower():
            w["last_reviewed"] = now_iso()
            w["review_count"] += 1
            if result == "known":
                w["correct_streak"] += 1
                if w["correct_streak"] >= 3:
                    w["status"] = "known"
                else:
                    w["status"] = "learning"
            elif result == "learning":
                w["status"] = "learning"
                w["correct_streak"] = max(0, w["correct_streak"])
            elif result == "forgot":
                w["status"] = "learning"
                w["correct_streak"] = 0
            save_profile(profile)
            print(json.dumps({"status": "updated", "word": w}, ensure_ascii=False, indent=2))
            return
    print(json.dumps({"status": "not_found_word", "word": word}, ensure_ascii=False))


def cmd_anki_pending(kind="all"):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    result = {}
    if kind in ("vocab", "all"):
        result["vocab"] = [w for w in profile["vocabulary"] if not w.get("anki_note_id")]
    if kind in ("mistake", "all"):
        result["mistakes"] = [m for m in profile["mistakes"] if not m.get("anki_note_id")]
    print(json.dumps({"status": "ok", **result}, ensure_ascii=False, indent=2))


def cmd_anki_mark_word(word, note_id):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    for w in profile["vocabulary"]:
        if w["word"].lower() == word.lower():
            w["anki_note_id"] = note_id
            w["anki_synced_at"] = now_iso()
            save_profile(profile)
            print(json.dumps({"status": "updated", "word": w}, ensure_ascii=False, indent=2))
            return
    print(json.dumps({"status": "not_found_word", "word": word}, ensure_ascii=False))


def cmd_anki_mark_mistake(category, note_id):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    for m in profile["mistakes"]:
        if m["category"].lower() == category.lower():
            m["anki_note_id"] = note_id
            m["anki_synced_at"] = now_iso()
            save_profile(profile)
            print(json.dumps({"status": "updated", "mistake": m}, ensure_ascii=False, indent=2))
            return
    print(json.dumps({"status": "not_found_category", "category": category}, ensure_ascii=False))


def cmd_log_session(mode, summary):
    profile = load_profile()
    if profile is None:
        print(json.dumps({"status": "not_found"}, ensure_ascii=False))
        return
    entry = {
        "timestamp": now_iso(),
        "mode": mode,
        "summary": summary
    }
    profile["sessions"].append(entry)
    profile["sessions"] = profile["sessions"][-50:]  # cap history
    profile["stats"]["total_sessions"] += 1
    save_profile(profile)
    print(json.dumps({"status": "logged", "session": entry, "total_sessions": profile["stats"]["total_sessions"]}, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "no command given"}, ensure_ascii=False))
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "init":
        cmd_init()
    elif cmd == "show":
        cmd_show()
    elif cmd == "set-level":
        if len(args) < 2:
            print(json.dumps({"status": "error", "message": "usage: set-level <skill> <level>"}, ensure_ascii=False))
            sys.exit(1)
        cmd_set_level(args[0], args[1])
    elif cmd == "add-mistake":
        if len(args) < 2:
            print(json.dumps({"status": "error", "message": "usage: add-mistake <category> <note>"}, ensure_ascii=False))
            sys.exit(1)
        cmd_add_mistake(args[0], args[1])
    elif cmd == "add-words":
        if len(args) < 1:
            print(json.dumps({"status": "error", "message": "usage: add-words <csv> [--topic X]"}, ensure_ascii=False))
            sys.exit(1)
        topic = None
        if "--topic" in args:
            idx = args.index("--topic")
            topic = args[idx + 1]
        cmd_add_words(args[0], topic)
    elif cmd == "review-words":
        n = 10
        if "--n" in args:
            idx = args.index("--n")
            n = int(args[idx + 1])
        cmd_review_words(n)
    elif cmd == "mark-word":
        if len(args) < 2:
            print(json.dumps({"status": "error", "message": "usage: mark-word <word> <known|learning|forgot>"}, ensure_ascii=False))
            sys.exit(1)
        cmd_mark_word(args[0], args[1])
    elif cmd == "log-session":
        if len(args) < 2:
            print(json.dumps({"status": "error", "message": "usage: log-session <mode> <summary>"}, ensure_ascii=False))
            sys.exit(1)
        cmd_log_session(args[0], args[1])
    elif cmd == "anki-pending":
        kind = "all"
        if "--kind" in args:
            idx = args.index("--kind")
            kind = args[idx + 1]
        cmd_anki_pending(kind)
    elif cmd == "anki-mark-word":
        if len(args) < 2:
            print(json.dumps({"status": "error", "message": "usage: anki-mark-word <word> <note_id>"}, ensure_ascii=False))
            sys.exit(1)
        cmd_anki_mark_word(args[0], args[1])
    elif cmd == "anki-mark-mistake":
        if len(args) < 2:
            print(json.dumps({"status": "error", "message": "usage: anki-mark-mistake <category> <note_id>"}, ensure_ascii=False))
            sys.exit(1)
        cmd_anki_mark_mistake(args[0], args[1])
    else:
        print(json.dumps({"status": "error", "message": f"unknown command '{cmd}'"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
