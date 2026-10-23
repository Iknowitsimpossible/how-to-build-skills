# 5. Scripts and references

A skill can bundle more than `SKILL.md`. The two folders you'll use most are `references/` (documents the agent **reads** when needed) and `scripts/` (code the agent **runs**).

## `references/`: load only what this task needs

Put material here when it's long, or when only some tasks need it. The agent reads a reference file only when a step in `SKILL.md` tells it to. That's the third level of progressive disclosure ([lesson 1](01-what-is-a-skill.md)).

Good candidates:

- **Variants:** one file per case, where each task needs only one. [`flashcard-maker`](../examples/02-with-references/flashcard-maker/) has `anki.md` and `quizlet.md`; [readme-organizer](../examples/03-readme-organizer/) has one README template per project type.
- **Long rules:** a style guide, a checklist, API details.
- **Shared rules** that several steps or variants use (`card-writing.md`, `writing-rules.md`).

How to point to them:

- **Say when to read it**, not just that it exists. "Read `references/anki.md`" inside the step that needs it beats a list of files at the bottom.
- **Use paths relative to the skill folder**, like `references/anki.md`.
- **Keep it one level deep.** `SKILL.md` points to reference files; reference files shouldn't send the agent on to more files.
- **Keep each file focused.** Several small files beat one big one, because the agent loads only what it needs.

## `scripts/`: let code do what code does better

Language models are good at judgment and bad at being exact every single time. Code is the opposite. So when a check must be **deterministic** (the same answer every time), write a script for it instead of an instruction.

| Better as an instruction | Better as a script |
|---|---|
| "Write one fact per card" | "Every line has exactly two fields" |
| "Judge content, not heading names" | "Every `npm run X` in the README exists in `package.json`" |
| "Keep the author's voice" | "No two cards have the same front" |
| Anything needing taste | Counting, matching, parsing, checking files exist |

The pattern that makes scripts most useful is **validate, then fix, in a loop**:

```markdown
### Step 4: Check the file, then fix

Run `python3 scripts/check_cards.py <deck-file> --format anki`.
Fix every error and run it again until it reports 0 errors.
```

### Writing a good bundled script

- **Standard library only**, if you can. Every dependency is something the user's machine might not have.
- **Clear, specific messages:** `line 5: same front as line 4` tells the agent exactly what to fix. `invalid input` doesn't.
- **Exit code 0 for success, 1 for errors**, so the agent (and CI) can tell at a glance.
- **A docstring at the top** with usage and what it checks. The agent may read it to understand the output.
- **Test it.** It's real code. See [`tests/test_check_cards.py`](../tests/test_check_cards.py).

### Always give a fallback

Some environments can't run code (some chat apps, locked-down machines). Tell the agent what to do by hand:

```markdown
**If you can't run Python**, check by hand: every line has exactly two fields,
no side is empty, and no two fronts are the same.
```

And say so in the `compatibility` field: "Python 3 is optional, for the bundled checker."

## `assets/`: things that go into the output

Templates, images, fonts, or data files that end up in what the skill produces (a slide template, a logo, a lookup table). The agent uses them; it doesn't need to read them as instructions.

## What not to put in the skill folder

- **No `README.md`.** Documentation for the agent goes in `SKILL.md` or `references/`. A README for humans belongs at the repo root, outside the skill folder ([lesson 8](08-publishing.md)).
- **No secrets.** API keys and tokens never go in a skill.
- **No large generated files** the agent doesn't need.

## Exercise

Look at [`check_cards.py`](../examples/02-with-references/flashcard-maker/scripts/check_cards.py). Name one more check that should be in the script, and one that should stay as an instruction in `references/card-writing.md`. Why?

**Next:** [6. Test your skill](06-testing.md)
