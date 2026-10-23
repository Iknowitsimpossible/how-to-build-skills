# Example 3: case study, readme-organizer

[`readme-organizer/`](readme-organizer/) is a real, published skill that writes or reviews the README of a finished project. This folder is a snapshot of version 1.2.0; the live version is at [Iknowitsimpossible/readme-organizer](https://github.com/Iknowitsimpossible/readme-organizer).

```text
readme-organizer/
├── SKILL.md                      # 6 steps, Important, examples, troubleshooting
├── references/                   # one README template per project type
│   ├── cli-tool.md  coursework.md  data-ml.md
│   ├── game.md      library.md     web-app.md
│   └── writing-rules.md          # shared by every template
└── scripts/
    └── check_readme.py           # checks commands, links, clone URLs
```

The finished files are useful, but the more useful part is **how it got there**. Every version below is a real commit, and each one fixed something a test turned up. Read this after the lessons; it's all of them applied to one skill.

## The iteration story

### v1: a reasonable first draft

The first commit put `SKILL.md` at the repo root next to six template files. Its description was clear about *what* the skill did:

> Write or review the README of a finished project. Reads the repo, identifies what kind of project it is [...] Use when the user asks to write, organize, refresh, or review a README for a project that is done or nearly done. Do not use for projects still in early development.

It looked fine. The problems only showed up when it ran on a real project.

### Test: one hard, real task

Instead of writing a dozen test prompts, the first test was one real request on one real project: "review the README of penalty-night", a finished three.js browser game. This is the "iterate on one hard task first" advice from [lesson 6](../../lessons/06-testing.md). It found four bugs:

| What happened | Why it was wrong | Fix in the skill |
|---|---|---|
| Flagged the untracked `.claude/` folder as "uncommitted work" and asked whether the project was finished | Agent and editor folders are never project work | Step 1 now ignores untracked agent and editor folders by name |
| Suggested renaming "Run it yourself" to "Installation" | It judged headings, not content; the section *was* installation | Step 4: "judge content, not heading names" |
| Suggested putting back text the author had just removed in a "Trim the README" commit | It ignored the author's deliberate choice | Step 2 reads `git log -- README.md`; Step 4 respects recent trims |
| The game template assumed you run the game locally | penalty-night is played in the browser on GitHub Pages | `references/game.md` puts the play link first for deployed browser games |

Notice that none of these are syntax errors. A validator can't find them. Only running the skill on a real task did.

### v1.1: restructured to follow the guide

The second commit applied [Anthropic's skill guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) and the four fixes:

- **Moved the skill into `skills/readme-organizer/`** so the repo's README (for humans) sits outside the skill folder (for agents). See [lesson 8](../../lessons/08-publishing.md).
- **Rewrote the description** with the phrases people actually type ("review my README", "make it presentable") and negative triggers (not for changelogs, API docs, or docstrings). See [lesson 3](../../lessons/03-frontmatter.md).
- **Added `## Important`** with the three rules that ruin the result if broken: never invent commands, never overwrite, always run the checker.
- **Added `scripts/check_readme.py`**, because "make sure every command exists" is exactly the kind of check language models forget and code doesn't. See [lesson 5](../../lessons/05-scripts-and-references.md).
- **Added examples and troubleshooting**, including the penalty-night run itself as Example 1.

### v1.2: agent-neutral, with tests and CI

The `compatibility` field said "Designed for Claude Code". Nothing in the skill actually needed Claude Code, so it became "any coding agent that supports Agent Skills and can run shell commands", with a by-hand fallback for agents that can't run Python. The repo gained install steps for Codex (`~/.agents/skills/`), a structure validator, 22 unit tests for the checker, and CI. See the [platform pages](../../platforms/).

### The last bug: a negative trigger that was too broad

The final test was to run the skill on its own repo: "review this README". It refused to load. The description ended with "Do NOT use [...] for README files of the skill itself", which was meant to stop it from triggering while someone edited the skill, but in practice it blocked a perfectly reasonable request. That negative trigger was removed, and the matching should-not-trigger test case was replaced with one that reflects the real risk ("Write the SKILL.md for a new skill").

The lesson: negative triggers are powerful, so test them as carefully as positive ones. One over-broad "do NOT" can silently disable a skill.

## What to copy from this example

- The structure of [`SKILL.md`](readme-organizer/SKILL.md): a one-line goal, `## Important`, numbered steps that each name exact commands, a classification table that picks one reference file, a validate-then-fix loop, examples taken from real runs, and a troubleshooting section.
- The idea of a checker that the skill runs on its own output, with a manual fallback.
- The habit of turning every bug found in testing into a specific line in the skill, and every fixed bug into a test case.
