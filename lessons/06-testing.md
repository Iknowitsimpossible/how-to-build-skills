# 6. Test your skill

A skill can pass every validator check and still be useless: it never loads, or it loads and does the wrong thing. The [case study](../examples/03-readme-organizer/) passed its first review on paper, then failed four ways on its first real run. Testing is where skills actually get good.

## Start with one hard, real task

Don't begin with a big test suite. Pick **one** realistic, hard request on real material, run it, and watch closely. Fix what goes wrong, run it again, and repeat until it works well. Then widen out.

Why: one real run gives you specific, surprising failures fast. readme-organizer's first run on a real game project showed that it:

- flagged an untracked `.claude/` folder as unfinished work,
- suggested renaming a section because of its heading, not its content,
- suggested putting back text the author had just deliberately removed,
- assumed a browser game must be run locally.

These failures were easy to miss in a paper review. Each suggested a targeted correction to test on other projects, rather than a universal rule to add automatically.

A useful variant: do the task *with the agent but without a skill*, steering it until the result is great. Then turn the steering you had to do into the skill's instructions.

## Then test three things

### 1. Triggering: does it load at the right times?

Write two lists of prompts and try each in a **fresh session** (old context can sway the agent):

```markdown
**Should trigger**
- "write a commit message"
- "commit this"                       <- obvious
- "what should I call this commit?"   <- paraphrased
- "describe my staged changes"

**Should NOT trigger**
- "write a PR description"            <- nearby task
- "write release notes for v2"        <- nearby task
- "explain git rebase"                <- same topic, different job
```

Include obvious requests, paraphrases, and **nearby tasks that should go elsewhere**. Aim for roughly 9 out of 10 correct in each list. Test in every agent you support, since each decides from the description on its own. ([Platform pages](../platforms/) show how to see whether a skill loaded.)

**Debugging trick:** ask the agent "When would you use the commit-message skill?" It will answer from the description, which shows you what it understood.

| Signal | Problem | Fix |
|---|---|---|
| Doesn't load for requests it should handle; you keep invoking it by name | **Under-triggering** | Add the phrases users actually type, file types, and keywords to the description |
| Loads for unrelated requests | **Over-triggering** | Add negative triggers ("Do NOT use for..."); make the "what" more specific |
| Never loads, even by name | Broken frontmatter | Run `tools/validate_skill.py` |

### 2. Functional: does it do the job right?

For each use case from [lesson 2](02-plan-use-cases.md), write the setup and what should happen:

| Case | Setup | Expected |
|---|---|---|
| Normal | Notes with 10 relevant facts, user says "Anki" | Relevant facts covered accurately, one concept per card, valid import format |
| Ask first | User doesn't name an app | Agent asks "Anki, Quizlet, or something else?" |
| Edge case | A fact contains a comma | The field is quoted; the checker passes |
| Consistency | Same request, 3 runs | Source fidelity, coverage, atomic cards, and import format remain good; wording and card count may vary |

Also unit-test any bundled script, like ordinary code ([`tests/`](../tests/)).

### 3. Performance: is it better than no skill?

Run the same task with and without the skill and compare: how many messages, how many corrections you had to make, how many failed commands. If the skill doesn't clearly win, it isn't earning its place in every session's context.

## Test transfer, not memorization

After improving the initial task, set aside unfamiliar inputs that you did not use to write the instructions. Try a different project type, a shorter source, and an ambiguous request. A change that fixes one example can damage another.

Record the input, agent/model, skill revision, observed outcome, and corrections needed. Compare with and without the skill on the same material using the same quality criteria. Repeat when variation could change your conclusion; do not require identical phrasing or arbitrary counts.

Add a failure-path case: the checker is unavailable or reports the same error after a repair. The agent should preserve useful work, state what remains unverified, and stop the repair loop.

## Iterate

Skills are never "done". After each round of testing or real use:

1. Write down what went wrong, specifically ("asked for the app even though the user said Anki").
2. Make the smallest supported change. Sometimes removing a rigid rule or improving an example works better than adding another instruction.
3. Add the failure as a test case so it can't quietly come back.
4. Bump `metadata.version`.

Keep your test cases in the repo, for example `tests/test-cases.md`, so anyone changing the skill can rerun them. See the case study's [test cases](https://github.com/Iknowitsimpossible/readme-organizer/blob/main/tests/test-cases.md) for a full example.

## Automated checks

Some things never need a human:

```bash
python3 tools/validate_skill.py examples     # structure and frontmatter
python3 -m unittest discover tests           # bundled scripts
```

Run them in CI on every push ([lesson 8](08-publishing.md)). They catch the boring mistakes, so your manual testing can focus on behavior.

## Exercise

Write 5 should-trigger and 5 should-not-trigger prompts for [`flashcard-maker`](../examples/02-with-references/flashcard-maker/SKILL.md). Which of your should-not prompts is most likely to trigger it by mistake? What would you add to the description to prevent that?

## Your deliverable

A test record for the original task and an unfamiliar input.

**Self-check:** What improved versus no skill, and what remains unverified?

**Next:** [7. Patterns](07-patterns.md)
