# 7. Patterns

These are shapes that keep showing up in skills that work well. They're not templates to copy exactly; pick the one that matches your task, and mix them when it helps.

First, decide which direction your skill leans:

- **Problem-first:** the user describes an outcome ("make this README presentable") and the skill figures out which tools and steps to use.
- **Tool-first:** the user already has a tool or service connected ("I've got the GitHub MCP set up") and the skill teaches the best way to use it.

Most skills lean one way. Problem-first skills need strong triggers and decision tables; tool-first skills need precise tool names and error handling.

## 1. Sequential workflow

**Use when** steps must happen in a fixed order, and later steps depend on earlier ones.

```markdown
### Step 1: Check the project is committed and pushed
If not, stop and ask.

### Step 2: Gather facts
Keep a list of facts with their sources.

### Step 3: Classify the project
Use the facts from Step 2.
```

**Key moves:** number the steps; say what each step needs from the one before; put a check between steps ("if X, stop and ask"); say what to do if a step fails partway. *Seen in:* [commit-message](../examples/01-minimal/commit-message/SKILL.md), [readme-organizer](../examples/03-readme-organizer/readme-organizer/SKILL.md).

## 2. Coordinating several services

**Use when** one workflow crosses several tools or MCP servers, for example: export screenshots from a design tool, upload them to cloud storage, then create tickets that link to them.

```markdown
### Phase 1: Export (design tool)
### Phase 2: Upload (storage) - needs the file list from Phase 1
### Phase 3: Create tickets (issue tracker) - needs the links from Phase 2
```

**Key moves:** one phase per service; say exactly what data passes between phases; confirm a phase succeeded before starting the next; handle errors in one place ("if any upload fails, stop and list which ones").

## 3. Iterative refinement

**Use when** the first draft is rarely good enough and quality can be checked.

```markdown
### Step 4: Check, then fix
Run scripts/check_cards.py. Fix every error. Run it again.
Stop when it reports 0 errors. If the same failure persists after a repair, or a required dependency is unavailable, preserve the output and report what remains unverified.
```

**Key moves:** an explicit quality bar; a script for the checks that can be automated ([lesson 5](05-scripts-and-references.md)); a checklist for the ones that can't; both a success condition and a failure exit so the loop ends. *Seen in:* [flashcard-maker](../examples/02-with-references/flashcard-maker/SKILL.md), readme-organizer's Step 5.

## 4. Choosing by context

**Use when** the goal is the same but the right approach depends on the situation.

```markdown
| Project type | Strong signals | Template |
|---|---|---|
| Game | pygame, three.js, game loop | references/game.md |
| CLI tool | argparse, "bin" in package.json | references/cli-tool.md |
| ...
| Nothing fits | | closest template; say so |
```

**Key moves:** clear criteria for each option; a fallback row; tell the user which option was picked and why ("Classified as a game: three.js browser game on GitHub Pages"). Pairs naturally with one reference file per option. *Seen in:* readme-organizer's Step 3, flashcard-maker's Step 2.

## 5. Domain expertise

**Use when** the value of the skill is knowledge the agent doesn't have: your field's rules, your team's conventions, the mistakes beginners make.

```markdown
## Important
- Only use facts from the source. Never add facts from memory.

### Before writing cards
Read references/card-writing.md: one fact per card, no give-aways, ...
```

**Key moves:** put the rules where they're checked *before* acting, not after; keep the expertise in reference files so it's loaded only when needed; record why decisions were made when it matters (for example, reporting what was skipped and why).

## Combining patterns

Real skills mix these. readme-organizer is a **sequential workflow** (Steps 1 to 6) that **chooses by context** (project type), adds **domain expertise** (writing rules), and ends in an **iterative refinement** loop (check, repair, and report persistent failures).

## Exercise

Think of a task you do in several steps (submitting an assignment, setting up a new project, preparing for a lab). Which pattern fits it best? Sketch the step headings.

## Your deliverable

A workflow sketch with only necessary dependencies.

**Self-check:** Can it exit usefully when a tool fails?

**Next:** [8. Publish and share](08-publishing.md)
