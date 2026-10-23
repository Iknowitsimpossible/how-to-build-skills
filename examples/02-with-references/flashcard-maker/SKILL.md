---
name: flashcard-maker
description: Turns lecture notes, slides, or a textbook chapter into study flashcards and saves them as a file that Anki or Quizlet can import. Writes one fact per card, checks the file with a bundled script, and fixes any problems before handing it over. Use when the user says "make flashcards", "turn my notes into cards", "Anki deck from this", "Quizlet set", or "help me memorize this". Do NOT use for practice exams, summaries, or study schedules.
license: MIT
compatibility: Needs file read and write access. Python 3 is optional, for the bundled checker.
metadata:
  author: Iknowitsimpossible
  version: 1.0.0
---

# Flashcard Maker

Turn source material into a deck of flashcards that the user can import in one step and study without editing.

## Important

- **Only use facts from the source.** Never add facts from memory. If the source is unclear or seems wrong, ask instead of guessing.
- **One fact per card.** A card that tests two things gets split into two cards.
- **Run the checker before handing over the file** (Step 4). A file that fails import wastes the user's study time.

## Instructions

### Step 1: Get the source and the target app

Read the notes, slides, or chapter the user points to. If they didn't say which app they use, ask: "Anki, Quizlet, or something else?" If they don't know, use Anki.

### Step 2: Read the rules for that app

| App | Read |
|---|---|
| Anki | `references/anki.md` |
| Quizlet | `references/quizlet.md` |
| Anything else | `references/anki.md` (its CSV format imports into most apps), and tell the user |

Read only the file for the app you are using. Then read `references/card-writing.md` for how to write good cards.

### Step 3: Write the cards

Go through the source section by section. For each fact worth remembering, write one card following `references/card-writing.md`. Aim for 10 to 40 cards per lecture; if you have many more, ask the user whether to keep only the most important.

Save the deck as `<topic>-flashcards.csv` (Anki) or `<topic>-flashcards.txt` (Quizlet) next to the source file, using a short kebab-case topic such as `cell-biology`.

### Step 4: Check the file, then fix

```bash
python3 scripts/check_cards.py <deck-file> --format anki      # or --format quizlet
```

(`scripts/` is relative to this skill's folder.) It reports cards with an empty side, duplicate fronts, fronts that are too long, and lines with the wrong number of fields. Fix every error and run it again until it reports `0 error(s)`.

**If you can't run Python**, check by hand: every line has exactly two fields, no side is empty, and no two fronts are the same.

### Step 5: Report

Tell the user the file name, the number of cards, and the import steps from the reference file for their app. List any facts you skipped because the source was unclear.

## Examples

**Example 1: lecture slides to Anki**

User says: "Make Anki flashcards from week3-slides.md"

Actions:
1. Read `week3-slides.md`. The user named Anki, so read `references/anki.md` and `references/card-writing.md`.
2. Write 24 cards, splitting "mitochondria make ATP and have their own DNA" into two cards.
3. Save `cell-biology-flashcards.csv`; the checker finds one duplicate front, which you merge, then reports 0 errors.

Result: "Saved 23 cards to `cell-biology-flashcards.csv`. In Anki: File, Import, pick the file, check that Field 1 maps to Front."

**Example 2: no app named**

User says: "help me memorize the dates in this history chapter"

Actions: ask which app they use. They say "Quizlet". Read `references/quizlet.md`, write date cards with the event on the front and the year on the back, check with `--format quizlet`.

## Troubleshooting

**The checker says a line has 3 fields.** A comma (Anki) or tab (Quizlet) inside a card split it. For Anki, wrap that field in double quotes. For Quizlet, replace the tab with a space.

**The source is a PDF or image you can't read.** Ask the user to paste the text, or export the slides as text first.

**The user wants cloze (fill-in-the-blank) cards.** Anki supports them; see the cloze section of `references/anki.md`. Quizlet doesn't, so write normal question cards instead and say why.
