# Tech Reading & Listening

Reference for technical reading/listening practice — documentation, articles, papers, talks, lectures. Loaded by `english-trainer` SKILL.md when the user wants to work through real technical material in English.

## Why this file is shaped this way

The user already reads/listens better than they write/speak, so this isn't primarily remedial — it's about (a) pushing reading/listening from "I get the gist" to "I get the precise meaning, including nuance and idiom," (b) harvesting vocabulary from real material instead of artificial lists, and (c) using comprehension as a launchpad for production practice (see `production.md` mode 4, summarize-it-back), since that's the user's actual weak point. Don't treat this as passive reading time — every session here should produce something: words logged, a summary produced, or a comprehension gap closed.

## Two material sources — both are in scope

The user wants both. Use whichever fits the moment:

### A. User-supplied material

The user brings a link, a pasted excerpt, or a file (PDF, markdown, transcript). Fetch/read it directly:
- For a URL: use `web_fetch` to get the content.
- For an uploaded file: check `/mnt/user-data/uploads/` and read it (use the `pdf-reading` skill if it's a PDF you need to inspect closely — check `/mnt/skills/public/pdf-reading/SKILL.md` for the right extraction approach rather than guessing).
- For pasted text: just work with what's given.

Don't summarize the whole thing back to them wholesale (that's also a copyright/displacement concern for published material, and it short-circuits the learning value) — instead use it as the basis for the exercises below.

### B. Claude-suggested material

When the user wants something to read/watch but doesn't have a specific source, or asks for suggestions ("найди что почитать", "porecomend an article on X"):
- Use `web_search` to find something current and genuinely good — prefer primary sources (official docs, original blog posts from engineering teams, arXiv papers, conference talks) over aggregator content.
- Match difficulty to their level: if `levels.reading` is lower, prefer well-written blog posts and official docs (these tend to use clearer, more direct English) over dense academic papers, which often have harder syntax even at the same vocabulary level.
- Match topic to stated interests if known, or ask briefly: "Something on a specific area (ML, backend, data infra), or surprise you?"
- For talks/lectures specifically, search for ones with transcripts or good captions available — comprehension-checking is much easier with text to refer back to, and you can pull a transcript via `web_fetch` if the source page has one.

When suggesting something, give a one-line reason it's a good fit ("this is from the PyTorch team's own blog, clear technical English, intermediate length") rather than just dropping a link.

## Core exercise patterns

Rotate through these rather than always doing the same thing:

### 1. Guided comprehension check
After the user reads a section, ask 2-4 questions that require actual understanding, not just located-the-keyword recall — e.g., "what would happen if you skipped step 3?", "why does the author recommend X over Y?", "what's the author's actual claim here, in your own words?" This catches the gap between "I recognized all the words" and "I understood the argument," which is common even for strong readers.

### 2. Vocabulary harvest
Ask the user to flag (or you flag, if they're reading silently and reporting back) words/phrases that were unfamiliar or unclear, even if they could guess meaning from context. Don't let "I could guess it" stop the word from being logged — guessable-from-context and actually-known-and-retrievable are very different things, and the gap between them is exactly the comprehension/production split. Add the real finds to the vocab queue:

```bash
python3 scripts/profile.py add-words "word1,word2" --topic "<source topic, e.g. distributed-systems>"
```

Keep this realistic — 5-10 words per article/section, not every slightly-unusual word in a long paper.

### 3. Idiom / phrasing decode
Technical writing and especially talks are full of semi-idiomatic phrasing that's hard to look up directly (hedging language, transitions, casual asides in talks: "as you might expect," "the gotcha here is," "long story short," "this is where it gets interesting," "by the same token"). When one comes up, briefly decode it and note that it's a set phrase rather than literal — these are exactly the things that make native speech feel faster/harder than it "should" be given the vocabulary involved.

### 4. Summarize-it-back (production bridge)
After a reading/listening session, hand off to `production.md` mode 4: have the user explain what they just read/watched in their own words, without looking at the source. This is the single highest-value exercise for connecting this skill's strength (comprehension) to their actual goal (production), so default to including it rather than treating reading as a complete, standalone activity.

### 5. Listening-specific: talks and lectures
If working from a talk/lecture (not pure text):
- If only audio/video is available with no transcript, this skill can't directly process audio — ask the user to either find a version with captions/transcript, or describe/paraphrase a section for discussion instead. Be upfront about this limitation rather than pretending to have watched something.
- If a transcript is available, treat it like a reading exercise but flag that real speech includes false starts, filler, and looser grammar than written text — point out a few of these features explicitly so the user doesn't mistake transcribed disfluency for a fixed rule they're missing. ("Speakers often restart sentences mid-thought — that's normal spoken English, not something to model your own writing on.")

## Difficulty signals to watch for

While working through material, take note of (and feed back into the profile / your sense of their level):
- Sentence length/complexity where comprehension visibly slows down (long noun phrases, nested clauses, passive voice stacking) — this is a strong B2→C1 marker.
- Domain jargon vs. general vocabulary gaps — these need different handling; jargon just needs a definition, general vocabulary gaps are a bigger pattern worth tracking.
- Whether they can follow the *argument structure* (claim → evidence → caveat) versus just the *sentence-level meaning* — argument-tracking is a higher-order skill worth explicitly praising when it's going well, since it's easy to undervalue.

## Copyright note

When working with real articles/papers/docs: don't reproduce large verbatim chunks back to the user in your own responses, even for "let's go through this together" purposes — refer to the original (which they already have open/pasted) rather than re-quoting big sections. Short quotes (under 15 words) for pointing at something specific are fine; summarizing structure or content at length is not.
