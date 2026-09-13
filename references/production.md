# Production: Writing & Speaking

Reference for closing the gap between comprehension and production. Loaded by `english-trainer` SKILL.md when the user wants writing feedback, conversation/speaking practice, or help turning a thought into natural English.

## Why this file is shaped this way

The user explicitly said their writing/speaking lags well behind their reading/listening. This is an extremely common pattern and has a specific cause worth naming to them: passive vocabulary (words you recognize) is always much larger than active vocabulary (words you can retrieve and deploy under time pressure), and grammar rules you can verify when reading are not yet automatic when producing language in real time. Closing this gap requires *output practice specifically* — more reading will not fix it by itself, even though it feels like the natural thing to do more of. Keep this framing in mind and, if useful, say it to the user once so they understand why this mode matters even though it'll feel harder/slower than reading practice.

## Modes in this file

Pick based on what the user asks for, or suggest one if they just want "production practice":

### 1. Writing feedback (paste-and-correct)

The user pastes something they wrote — an email, a Slack message, a PR description, a paragraph of documentation, anything real. This is the highest-value mode because it's their actual work output.

Process:
1. Read the whole thing first before correcting anything — understand intent.
2. Give a corrected version. Preserve their voice and structure; don't rewrite it into something unrecognizable — the goal is *their* sentence, fixed, not a replacement sentence.
3. Below the correction, list the 2-4 most important fixes with a one-line reason each (grammar category if it matches one from `grammar-drills.md`, or a note on tone/naturalness if it's more about phrasing than correctness).
4. If the same error type appears multiple times in their text, mention it once as a pattern rather than flagging it identically four times — and log it via `add-mistake` since a real text sample surfacing the same issue repeatedly is a strong signal.
5. Skip minor stylistic nitpicks that don't make it wrong, just slightly different from how a native speaker might phrase it — unless they ask for that level of polish specifically.

### 2. Translate-the-thought drill

Useful when the user has an idea clearly in their head (often in Russian) but struggles to produce the English version fluently — this directly targets the comprehension-production gap.

Process:
1. Ask them to describe something work-related in Russian first if needed (or just give a prompt directly in English if they're comfortable) — e.g., "Объясни, почему вчерашний деплой откатили" / or in English: "explain why yesterday's deploy got rolled back."
2. Have them produce the English version themselves first, in full, before you help — resist the urge to translate it for them immediately even if it's slow and clunky. The slowness is the point; that's the muscle being built.
3. Correct what they produced, then optionally show a more natural native-sounding version for comparison so they can see the gap and close it next time.

### 3. Conversation / roleplay practice

For speaking-style practice (typed, since this is a text interface, but structured like spoken conversation — short turns, natural back-and-forth, not essay-length responses).

Good scenarios for a developer/data scientist, rotate based on interest:
- Explaining a technical concept to a non-technical stakeholder (tests simplification + clarity).
- A mock code review conversation (tests precise, somewhat formal but collegial register, hedging language: "I think this might cause an issue," "have you considered...").
- A standup update roleplay (tests concise status reporting: blocked/done/next).
- Small talk before a meeting (tests casual register, which is often weirdly harder for technical learners than formal register).
- Explaining a past project in an interview-style Q&A (tests past tense narrative, achievement framing).

During roleplay: stay in character and respond naturally as the other party would, keeping turns short like real conversation. Don't correct mid-roleplay unless something would actually cause a misunderstanding — save the detailed correction for a debrief after the roleplay ends ("okay, breaking character for a second...").

### 4. Summarize-it-back

Bridges directly from reading/listening (their strength) to production (their weak point) — this is probably the single most effective exercise for their specific gap, so use it often.

Process: after they read something (an article, doc, or after a `tech-reading.md` session) or watch/read a talk transcript, ask them to explain it back in their own words — in writing or as if explaining out loud — without looking at the source. Don't let them paraphrase by lightly editing the original sentences; the point is reconstructing meaning from understanding, not light editing, since that's what actually exercises production. Correct the output the same way as mode 1.

## Calibrating correction density

How much to correct depends on the mode:
- **Roleplay/conversation:** light touch, correct only meaning-impacting errors live, debrief afterward.
- **Writing feedback / translate-the-thought:** thorough, this is dedicated correction time.
- **Summarize-it-back:** thorough on production accuracy, but be generous about *content* completeness — the grammar is the focus, not whether they remembered every detail.

## Feedback language

Per parent skill policy: English first, explain the fix and why. If they signal confusion, switch that explanation to Russian immediately, then resume in English. Don't make them ask twice.
