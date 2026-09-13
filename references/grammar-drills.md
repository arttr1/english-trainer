# Grammar Drills

Reference for targeted grammar practice. Loaded by `english-trainer` SKILL.md when the user wants grammar correction or drilling.

## Why this file is shaped this way

Generic grammar exercises waste time — a Russian-speaking learner's errors are not random, they cluster around specific structural differences between Russian and English. Prioritize drilling *those* over generic "grammar review." The list below is ordered roughly by how often these actually show up for Russian-speaking learners, especially technical ones writing/speaking about work.

## High-frequency error categories (Russian → English)

For each category: what causes it, what it looks like, and a drill pattern. When you spot one of these in the user's writing/speech, name the category using these exact labels when logging to the profile (`add-mistake`), so counts accumulate consistently.

### 1. Articles (a / an / the / no article)
**Cause:** Russian has no articles at all, so this is almost never intuitive — it has to become semi-mechanical knowledge.
**Looks like:** "I work on project", "I read the article yesterday" (when no specific article was established), "Database is slow" (missing "The database").
**Drill pattern:** Give 8-10 sentences with articles removed (technical context — "___ model overfit because ___ dataset was too small"), have the user fill them in, then explain the *logic* (first mention vs. already-known; countable vs. uncountable; generic vs. specific) rather than just marking right/wrong.

### 2. Verb tenses: present perfect vs. past simple
**Cause:** Russian uses aspect (perfective/imperfective) instead of the English tense-and-time-reference system; "I have done X" and "I did X" both tend to collapse toward one Russian-feeling option.
**Looks like:** "I already finished the report" (should often be "I've already finished"), or overusing present perfect where past simple fits ("I have seen him yesterday" — wrong, "yesterday" forces past simple).
**Drill pattern:** Give pairs of sentences differing only in whether a specific past time is mentioned; ask which tense fits and why. Tie the rule to a concrete test: "if there's a specific finished time word (yesterday, in 2022, last week) → past simple; if it's about result-now or unspecified time → present perfect."

### 3. Prepositions
**Cause:** Prepositions rarely map 1:1 between languages; this is largely memorization, not logic, so treat it that way rather than over-explaining.
**Looks like:** "depends of" (→ "depends on"), "different than" used inconsistently, "in the weekend" (→ "on the weekend"), "discuss about" (→ just "discuss").
**Drill pattern:** Collocational drilling — give common verb/adjective + preposition pairs relevant to work English (depend on, responsible for, interested in, good at, consist of, result in) and have the user produce full sentences. Correct silently and move on; don't try to derive a "rule," there often isn't one.

### 4. Word order, especially in questions and after adverbs
**Cause:** Russian word order is much freer (flexible due to case marking); English relies on word order to carry meaning, so direct word-for-word translation breaks.
**Looks like:** "What means this word?" (→ "What does this word mean?"), "I very like it" (→ "I like it very much" / "I really like it"), reported-question word order errors ("I don't know what is this" → "what this is").
**Drill pattern:** Give Russian-influenced broken sentences and have the user fix word order, then have them generate 3-4 original questions from scratch about a technical topic (e.g., questions they'd ask in a code review) to check it generalizes.

### 5. Articles/plurals with uncountable nouns (tech-specific)
**Cause:** Words like "information," "data," "software," "feedback," "research" behave as uncountable in English but their Russian equivalents are often used more freely; also some words are uncountable in English but countable in Russian-influenced thinking, and vice versa.
**Looks like:** "I have an information", "softwares", "datas", "many researches".
**Drill pattern:** Build a personal list of uncountable nouns common in their domain (data, software, information, research, equipment, knowledge) and drill quantifiers: "a lot of / some / much" + noun, never "a/an" + noun, never pluralized.

### 6. Conditionals and hypotheticals
**Cause:** Russian conditional marking (бы) is less differentiated than English's first/second/third conditional system.
**Looks like:** Mixing "If I will have time" (→ "If I have time"), or using present tense where a hypothetical past needs "would have."
**Drill pattern:** Present real work scenarios ("if the deploy fails, what do you do?" = zero/first conditional; "if you had more time on that project, what would you have done differently?" = third conditional) and have them respond, correcting the conditional structure live.

### 7. False friends and calques (literal translation traps)
**Cause:** Direct translation of common Russian phrasing produces non-native English even when grammatically parseable.
**Looks like:** "It depends from", "I have 30 years" (→ "I'm 30"), "make a decision" said as "do a decision," "normal" used to mean "fine/okay" (которое в английском звучит иначе), "actual" used to mean "current" (calque of актуальный, should be "current/relevant," since "actual" means "real/genuine" in English).
**Drill pattern:** Translation drills specifically — give a Russian sentence containing a known calque trap and have them produce natural English, then show the natural native phrasing side by side.

## Drill formats to rotate through

Don't run the same format every time — vary it so practice doesn't go stale:

1. **Spot and fix.** Give 5-8 sentences, some correct, some with one error each (from the categories above). User identifies and fixes.
2. **Translate the trap.** Give a Russian sentence specifically engineered to trigger a calque or structural error. User translates; compare to natural phrasing.
3. **Fill in the blank.** Cloze-style sentences targeting one category (e.g., all articles, or all prepositions) — good for rapid-fire practice.
4. **Produce from a prompt.** Give a real-world dev scenario ("explain to a junior why the test is flaky") and have them write or say 3-5 sentences; correct organically rather than against a checklist.
5. **Error hunt in their own text.** If they paste something they wrote (Slack message, PR description, email), go through it line by line.

## Calibrating difficulty

If the user's level is unknown or low-confidence, start with format 1 (spot and fix) using sentences with a single, obvious error — this reveals a lot about what they actually know without being intimidating. Adjust:
- Frequent correct answers, fast → move to format 4 (production), which is harder and more diagnostic.
- Struggling even with single, obvious errors → slow down, do format 3 (fill in blank) on just one category at a time, and explain the underlying rule more explicitly before drilling.

## Giving feedback

Per the parent skill's policy: explain corrections in English first ("This needs the present perfect here because there's no specific time mentioned — 'I've already deployed it' rather than 'I already deployed it'"). If the user seems lost, immediately follow with a Russian explanation of the same point, then continue in English.

Keep explanations short — one or two sentences naming the rule, not a grammar lecture. The goal is pattern recognition through repetition, not theoretical mastery of English grammar terminology.
