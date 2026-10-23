# 4. Write the instructions

Once the description gets your skill loaded, the body of `SKILL.md` has to get the task done. The body is plain Markdown with no required format, but a structure that works well is:

```markdown
# Skill Name
One or two sentences: the outcome, and what "good" looks like.

## Important
The rules that ruin the result if broken.

## Instructions
### Step 1: ...
### Step 2: ...

## Examples
## Troubleshooting
```

[`templates/SKILL.template.md`](../templates/SKILL.template.md) has this skeleton ready to fill in.

## Put the critical rules first

Agents pay the most attention to what they read first, and long instructions get skimmed. If a rule matters, put it under `## Important` at the top, before any steps:

```markdown
## Important

- Describe only what is **staged**. Unstaged changes are not part of the commit.
- Never run `git commit` yourself unless the user asked you to commit.
```

Keep this to two or three rules. If everything is important, nothing is. It's fine to repeat a critical rule inside the step where it applies.

## Choose how much to prescribe

Use an outcome and decision criteria for open-ended writing, design, or review. Use a preferred workflow when order helps. Use exact commands and limits when deviation risks an incorrect result or an unintended side effect.

For example, “preserve the author's voice and give each proposed edit a location and replacement” leaves room for judgment. An import format requiring two CSV columns needs an exact schema.

Add guidance the agent would otherwise miss. Do not restate ordinary capabilities or turn one author's preference into a global rule. Respect the user's current request and authorization; ask only when missing information or an unapproved consequential action requires it.

Start with the [minimal template](../templates/SKILL.minimal.md). Add steps, references, scripts, and troubleshooting only when they improve the outcome.

## Be specific where correctness depends on it

Specific instructions reduce ambiguity, but do not guarantee identical behavior. Prescribe only the details that matter to correctness or the intended result.

| Vague | Specific |
|---|---|
| Look at the changes. | Run `git diff --staged --stat`, then `git diff --staged`. |
| Keep the subject short. | Subject line: at most 50 characters, imperative mood ("Add", not "Added"), no period. |
| Validate the output. | Run `python3 scripts/check_cards.py <file> --format anki`. Fix reported errors and recheck; stop and explain if the same failure persists or the check cannot run. |
| Use the right template. | A table mapping each project type to its template file (see below). |

A good test: could two different people follow the step and do the same thing?

## Use tables for decisions

When the next step depends on the situation, a small table is clearer than paragraphs of "if... otherwise if...":

```markdown
| App | Read |
|---|---|
| Anki | `references/anki.md` |
| Quizlet | `references/quizlet.md` |
| Anything else | `references/anki.md`, and tell the user |
```

Include a fallback when unmatched inputs are plausible; do not silently force an incompatible format.

## Say when to stop and ask

Agents tend to either barrel ahead or ask too much. Tell them exactly which situations need the user:

```markdown
If nothing is staged, explain that no staged diff is available. Ask which specific changes the user wants included; do not propose staging unrelated files by default.
Otherwise continue without asking.
```

The "otherwise continue" line matters as much as the "ask" line.

## Show examples

One example of real input and output teaches style faster than a paragraph of rules. Use this shape:

```markdown
**Example 1: lecture slides to Anki**

User says: "Make Anki flashcards from week3-slides.md"

Actions:
1. Read the slides, then references/anki.md and references/card-writing.md.
2. Write 24 cards; split one card that tested two facts.
3. Run the checker, fix the one duplicate it found.

Result: "Saved 23 cards to cell-biology-flashcards.csv. In Anki: File, Import..."
```

The best examples come from real test runs ([lesson 6](06-testing.md)). The case study's Example 1 is the exact run that found its bugs.

## Add troubleshooting

List what goes wrong and what to do: a cause and a fix for each.

```markdown
**The checker says a line has 3 fields.** A comma inside a card split it.
Wrap that field in double quotes.
```

This saves the agent from improvising a fix, which is where skills tend to go off the rails.

## Keep it lean

- Keep the body as short as the task permits. The spec recommends under 500 lines and under 5,000 tokens, not a 5,000-word hard limit. The whole body loads every time the skill runs.
- Move long reference material (style guides, API details, templates) into `references/` ([lesson 5](05-scripts-and-references.md)).
- Prefer numbered steps and bullets to paragraphs.
- Write for the agent, not for a human reader: no marketing, no history of why the skill exists.

## If the agent ignores your instructions

| Symptom | Likely cause | Fix |
|---|---|---|
| Skips a rule | It's buried in the middle | Move it to `## Important`; repeat it in the step |
| Does it differently each time | The step is ambiguous | Name the exact command, file, or number |
| Skips the checking step | Checking sounds optional | Give validation a clear success condition and an exit for persistent failures; consider a script |
| Rushes through | Instructions are long and flat | Shorten; move detail to `references/` |

## Exercise

Open [`examples/01-minimal/commit-message/SKILL.md`](../examples/01-minimal/commit-message/SKILL.md). Find one vague phrase and make it more specific. Then find the line that tells the agent when *not* to ask the user anything.

## Your deliverable

A first instruction draft.

**Self-check:** Which constraints protect correctness, and which should remain choices?

**Next:** [5. Scripts and references](05-scripts-and-references.md)
