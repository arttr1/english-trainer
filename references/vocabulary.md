# Vocabulary

Reference for vocabulary building. Loaded by `english-trainer` SKILL.md when the user wants to learn words, get quizzed, or grow tech vocabulary specifically.

## Why this file is shaped this way

Vocabulary that isn't reviewed is forgotten within days (the forgetting curve is real and fast). The point of tracking words in `profile.json` is to actually space out review instead of doing one-off vocab lists that vanish from memory. Always prefer reviewing existing queued words over endlessly adding new ones — a learner who "knows" 50 words solidly is in better shape than one who's been shown 500 words once each.

## The core loop

This skill uses a lightweight spaced-repetition approach via `scripts/profile.py`, not a fixed schedule with exact intervals — good enough for a conversational coaching context. The status field per word is one of:
- `new` — added but never quizzed
- `learning` — quizzed at least once, not yet consistently correct
- `known` — answered correctly 3 times in a row (`correct_streak >= 3`)

### Reviewing existing words

When the user wants vocab practice (or you're choosing what to do and vocab is due), pull the queue:

```bash
python3 scripts/profile.py review-words --n 10
```

This returns words prioritized: `new` words first, then `learning` words with the lowest streak, then whatever hasn't been reviewed in the longest time. Quiz them — don't just show the word and definition, make them produce something:
- Ask them to use the word in an original sentence (ideally work-relevant).
- Give a definition or a Russian translation and ask for the English word.
- Give the English word in a sentence with a blank and ask them to recall it.
- For confusable pairs (affect/effect, lose/loose), give a sentence and ask them to pick.

After each word, record the result:

```bash
python3 scripts/profile.py mark-word "<word>" known      # got it right, confidently
python3 scripts/profile.py mark-word "<word>" learning    # got it right but hesitant, or partially
python3 scripts/profile.py mark-word "<word>" forgot      # got it wrong / blanked
```

### Adding new words

Add words when: the user asks to learn vocabulary on a topic, encounters unfamiliar words while reading (see `tech-reading.md` — that workflow feeds words back here), or asks "what's a good word for X."

```bash
python3 scripts/profile.py add-words "word1,word2,word3" --topic "networking"
```

Don't dump 30 words at once from a single session — somewhere around 5-10 new words per session is realistic to actually retain. If a text has way more unfamiliar words than that, pick the highest-value/most-recurring ones and let the rest go.

### Always give pronunciation for new words

Whenever you introduce a new word or multi-word expression (in vocab work, in tech-reading, anywhere), include its pronunciation:
- **IPA** in slashes: `obsolete /ˈɒbsəliːt/`.
- **A rough Russian-letters approximation** in parentheses, with stress marked (CAPS or an acute accent): `(об-со-ли́т)`. This is what the user specifically asked for — it's the fast, low-friction cue, and the IPA is the precise backup.
- Note the stressed syllable explicitly when the word is long or the stress is non-obvious (`emphasis on the first syllable`), since misplaced stress is a bigger intelligibility problem than vowel quality.
- For expressions/phrases, transcribe the parts likely to trip the user up rather than every word (e.g. for "a foolish consistency" just gloss `foolish /ˈfuːlɪʃ/ (фу́-лиш)`).
- Flag when spelling and sound diverge sharply (silent letters, `-ough`, stress shifting between noun/verb like `ˈrecord` vs `reˈcord`) — those are the ones worth a spoken drill.

Keep it compact — one line per word, not a phonetics lecture.

## Tech vocabulary by theme

The user is a software engineer / data scientist — bias word selection toward these domains rather than generic "advanced vocabulary" lists. Use these as a starting menu when they want a themed batch, not a rigid checklist:

**General software engineering:** deprecated, idempotent, race condition, boilerplate, scaffolding, tech debt, edge case, brittle (code), verbose, granular, fault-tolerant, stateless/stateful, throughput, latency, bottleneck, regression (in the testing sense), rollback, mitigate, instrument (as a verb, "instrument the code"), under the hood, off the shelf, leverage (as a verb, common in work English even though style guides complain about it).

**Data science / ML:** overfit/underfit, drift (data drift, concept drift), ablation, confound/confounding, heuristic, sparse/dense, skewed (distribution), outlier, ground truth, inference (as in "run inference," distinct from statistical inference), pipeline, feature (as in feature engineering — distinct from product feature), benchmark, interpretability, brittle (model), spurious (correlation).

**Working/collaborating in English (soft-skill adjacent but high value):** blocked (on something), follow up, circle back, flag (as a verb — "I'll flag this"), nitpick, scope creep, push back (on a decision), align/alignment ("let's get aligned"), trade-off, walk through (as a verb — "let me walk you through it"), surface (a problem), actionable, in the loop, take a stab at, ballpark (figure), sanity check.

**General higher-frequency vocabulary** (not tech-specific, but commonly missing for B1/B2 learners and useful in professional writing): nuance, ambiguous, redundant, arbitrary, robust, viable, plausible, contingent (on), comprehensive, discrepancy, mitigate, exacerbate, prevalent, inherent, substantial, marginal (as in "marginal improvement"), counterintuitive.

When introducing a themed batch, give a short, natural example sentence per word — ideally one that could plausibly appear in a PR description, a Slack message, or a paper, since that's directly transferable to their work.

## Quizzing formats to rotate

1. **Definition → word.** "What's the word for repeatedly running the same operation and always getting the same result?" → idempotent.
2. **Word → use it.** Give the word, ask them to write an original sentence using it correctly in a technical context.
3. **Cloze from real-feeling context.** "The model started to ___ after epoch 40, performing great on train but poorly on validation." → overfit.
4. **Confusable pairs.** affect/effect, principle/principal, complement/compliment, lose/loose, its/it's — these are genuinely common slip points even at higher levels, including for native speakers, but worth a quick check.
5. **Synonym precision.** Give a sentence with a vague word ("the model is bad at this") and ask for 2-3 more precise alternatives (brittle, unreliable, prone to error) — this builds toward more native-sounding writing rather than just expanding raw vocabulary count.

## Connecting to the bigger goal

Vocabulary work should feed into production practice, not stay abstract. When a word has been marked `known`, look for a natural moment later (in a conversation/writing exercise from `production.md`) to nudge the user to actually use it unprompted — that's the real test of whether it's internalized, not just recognized.
