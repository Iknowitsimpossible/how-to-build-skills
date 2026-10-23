---
name: readme-organizer
description: Writes or reviews the README of a finished software project. Detects the project type (web app, library, CLI tool, game, data/ML, coursework) and produces a README covering what it does, how to install it, and how to use it, with every command checked against the repo. Reviews an existing README by suggesting fixes and never overwrites it. Use when the user says "write a README", "review my README", "improve/fix/organize my README", "document this project for GitHub", or "my project is done, make it presentable". Do NOT use for projects still in early development, or for API reference docs, changelogs, or docstrings.
license: MIT
compatibility: Works with any coding agent that supports Agent Skills and can run shell commands in a local git repository (for example Claude Code or Codex). Python 3 is optional, for the bundled checker. Not for chat-only apps without access to the repo.
metadata:
  author: Iknowitsimpossible
  version: 1.2.0
---

# README Organizer

Produce a README that answers, in order: **What does this project do? How do I install it? How do I use it?** A visitor should be able to decide in under a minute whether the project is useful to them, and get it running in a few more.

## Important

- **Never invent** a command, flag, URL, version, or feature. Each must trace to a file you read. If something can't be confirmed, write `<!-- TODO: ... -->` and tell the user.
- **Never overwrite an existing README.** Suggest changes, then apply only what the user approves.
- **Always run the checker** (Step 5) before showing results.

## Instructions

### Step 1: Check the project is ready

This skill is for finished projects. Run:

```bash
git status --short --untracked-files=no   # tracked changes only
git status -sb | head -1                  # "ahead N" means unpushed commits
git log --oneline -5
```

- **Tracked changes or unpushed commits:** tell the user and ask whether to continue. The README should describe what is actually pushed.
- **Untracked files:** ignore them, unless they look like project source (for example a new `src/` file). Agent and editor folders such as `.claude/`, `.agents/`, `.codex/`, `.cursor/`, `.vscode/`, `.idea/`, `.DS_Store`, and an old `README-SUGGESTIONS.md` never count.
- **Very few commits, with stubs or TODOs throughout the code:** say the project looks unfinished and ask before continuing.
- Otherwise continue without asking.

### Step 2: Gather facts

Run `git ls-files` to see what is tracked, then read only what applies:

1. **Manifests:** `package.json`, `pyproject.toml`, `setup.py`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `CMakeLists.txt`, `Makefile`, `Dockerfile`, `environment.yml`.
2. **Entry points:** `main.*`, `app.*`, `index.*`, `src/`, `bin/`, and the `"bin"`, `"main"`, or `[project.scripts]` fields.
3. **Runnable commands:** `package.json` scripts, Makefile targets, `[project.scripts]`, and steps in `.github/workflows/`.
4. **Requirements:** `engines`, `requires-python`, `rust-version`, `.nvmrc`, `.python-version`, CI language versions.
5. **Config the user must supply:** `.env.example`, `config.example.*`, code reading `process.env` or `os.environ`.
6. **Context:** the existing README, `LICENSE`, `git remote get-url origin`, the repo's visibility and homepage (`gh repo view --json visibility,homepageUrl` if `gh` is available), deploy configs (GitHub Pages workflow, `vercel.json`, `netlify.toml`), and tracked images.
7. **README history:** `git log --oneline -5 -- README.md`. Recent deliberate edits (for example "trim the README") tell you what the author wants. Don't suggest undoing them.

Keep a list of **facts with their sources**, for example "dev server: `npm run dev` (package.json scripts.dev)".

### Step 3: Classify the project

Pick **one** primary type, then read only its template:

| Type | Strong signals | Template |
|---|---|---|
| Web app / website | React/Vue/Svelte/Next/Vite/Flask/Django/Express; `index.html`; deploy config | `references/web-app.md` |
| Library / package | Package metadata with `exports`/`main` and no app entry point; code meant to be imported | `references/library.md` |
| CLI tool | `"bin"`, `[project.scripts]`, argparse/click/commander/clap, `main` reading argv | `references/cli-tool.md` |
| Game | pygame/Unity/Godot/Phaser/three.js game loop, cmu_graphics, player input handling, levels | `references/game.md` |
| Data / ML | Mostly `.ipynb`, `data/`, pandas/sklearn/torch, model weights, results plots | `references/data-ml.md` |
| Coursework | Course codes or `hw`/`lab` in names, handout PDFs, autograders, starter code | `references/coursework.md` |

If two types fit, pick the one that describes **how a visitor uses it**, and borrow sections from the other. For example, a browser game is a game that borrows the web app's live-demo link. If nothing fits, use the closest template and say so. Ask the user only if you really can't tell.

Tell the user the type and the main reason in one line, e.g. *"Classified as a game: three.js browser game deployed to GitHub Pages."*

### Step 4: Write or suggest

**No README, or only boilerplate:** write `README.md` from the template and `references/writing-rules.md`.

**A README exists:** don't edit it. Write `README-SUGGESTIONS.md` in the repo root with:

1. **Verdict:** one or two sentences on the README's overall state.
2. **Issues**, most important first. For each: what is wrong or missing, why it matters to a reader, and the exact replacement text.
3. **Keep:** what is good and should stay.

When reviewing, judge **content, not heading names**. "Run it yourself" counts as Installation, and "Controls" counts as Usage. Suggest renaming a section only if a reader would actually be confused. Keep the author's voice and length. If they trimmed the README on purpose, propose small additions, not a rewrite.

### Step 5: Validate, then fix

Run the bundled checker on the file you produced:

```bash
python3 scripts/check_readme.py <repo-dir>                         # for README.md
python3 scripts/check_readme.py <repo-dir> README-SUGGESTIONS.md   # for suggestions
```

(`scripts/` is relative to this skill's folder.) It flags `npm`/`yarn`/`pnpm`/`make` commands with no matching script or target, `python`/`node` files that aren't tracked, links and images to missing files, clone URLs that don't match `origin`, and lists TODO markers.

For each error, fix the text and run the checker again. Stop when it reports 0 errors. If an error comes from content quoted from another project on purpose (a before/after example), wrap that section in `<!-- check-readme: off -->` and `<!-- check-readme: on -->` instead of changing it.

**If you can't run Python**, do the same checks by hand: for each `npm`/`yarn`/`pnpm run X`, confirm `X` is in `package.json` scripts; for each `make X`, confirm the Makefile target; for each relative link or image, confirm the path appears in `git ls-files`; confirm any `git clone` URL matches `git remote get-url origin`.

Then confirm the checks a script can't do:

- [ ] the three core topics (what, install, use) are covered, in that order;
- [ ] a stranger could go from `git clone` to a running project using only the README;
- [ ] every feature claimed is visible in the code.

### Step 6: Report

- **New README:** show it and list every TODO marker.
- **Suggestions:** summarize the top three in chat and ask which to apply. Apply only the approved ones, editing the README in place and running the checker again. Remind the user that `README-SUGGESTIONS.md` is a working file to delete, not commit.

## Examples

**Example 1: reviewing a finished browser game**

User says: "Review the README of my penalty-night project."

Actions:
1. Step 1: the only untracked folder is `.claude/`, and `main` is in sync with `origin`, so continue.
2. Step 2: package.json (Vite, three.js, `engines.node` 22.12+, scripts `dev`/`test`), a Pages workflow, a README with a play link and a controls table, and a recent "Trim the README" commit.
3. Step 3: classified as a game (three.js browser game on GitHub Pages).
4. Step 4: wrote suggestions: add a gameplay GIF; add `git clone` and the Node 22.12 requirement; the repo is public with no LICENSE. Keep the controls table, after confirming it against `src/input/keyboard.js`. Keep the short length.
5. Step 5: the checker reports 0 errors.

Result: the user gets four focused suggestions and their README is untouched.

**Example 2: a Python CLI with no README**

User says: "This tool is done, write a README for it."

Actions: read `pyproject.toml` (`[project.scripts] csvsum = "csvsum.cli:main"`, `requires-python >= 3.10`) and the argparse definitions in `csvsum/cli.py`. Classify as a CLI tool, write `README.md` with `pipx install .` and an options table built from the parser, then run the checker.

Result: a new README with no invented flags, and a TODO for the example output if running the tool isn't safe.

## Troubleshooting

**Not a git repository.** The checker and Step 1 need git. Ask the user whether to continue without the readiness check. If so, list files with `find` (skipping `node_modules`, `.venv`, `dist`, `build`) and treat every file on disk as tracked.

**Several projects in one repo (a monorepo).** If `packages/*/package.json`, multiple `pyproject.toml`, or separate `frontend/` and `backend/` folders exist, ask whether the user wants the root README, a per-package README, or both. A root README should briefly introduce each part and link to it.

**README has another name or format** (`readme.md`, `README.rst`, `README.txt`, `docs/README.md`). Review that file. Keep its format unless the user asks to convert it to Markdown.

**Checker reports a clone URL mismatch on a fork.** This is expected if the README deliberately points to the upstream repo. Mention it to the user and don't "fix" it.

**`gh` is not installed or not logged in.** Skip the visibility and homepage check. Look for the deploy URL in config files, and leave a TODO if it isn't found.

**Committed secrets.** If you find a real `.env`, API key, or token in tracked files, stop and warn the user before writing anything. Never copy the values into the README.
