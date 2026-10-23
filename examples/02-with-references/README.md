# Example 2: a skill with references and a script

[`flashcard-maker/`](flashcard-maker/) turns lecture notes into an Anki or Quizlet deck. It shows the two optional folders you'll use most:

```text
flashcard-maker/
├── SKILL.md                 # always loaded when the skill runs
├── references/              # loaded only when a step says so
│   ├── anki.md
│   ├── quizlet.md
│   └── card-writing.md
└── scripts/
    └── check_cards.py       # run, not read: a deterministic check
```

## What to notice

- **References are chosen, not all loaded.** Step 2 is a small table: Anki users get `anki.md`, Quizlet users get `quizlet.md`. The agent never reads the file it doesn't need, which keeps its context small. This is progressive disclosure's third level ([lesson 1](../../lessons/01-what-is-a-skill.md), [lesson 5](../../lessons/05-scripts-and-references.md)).
- **The script checks what words can't guarantee.** "Make sure every line has two fields" is easy to forget; `check_cards.py` never forgets. The skill tells the agent to fix and re-run until it reports 0 errors, which is the iterative refinement pattern ([lesson 7](../../lessons/07-patterns.md)).
- **There's a fallback.** If the agent can't run Python (for example in some chat apps), the skill lists the same checks to do by hand.
- **`compatibility` is used** because the skill needs file access, and says Python is optional.
- **The script is tested.** [`tests/test_check_cards.py`](../../tests/test_check_cards.py) runs it on good and bad decks in CI.

## Try it

[`sample/`](sample/) has a page of notes and the deck the skill produced from it. Check the deck yourself:

```bash
python3 examples/02-with-references/flashcard-maker/scripts/check_cards.py examples/02-with-references/sample/cell-biology-flashcards.csv --format anki
```

To use the skill, copy `flashcard-maker/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex), then ask: "make Anki flashcards from week3-notes.md".
