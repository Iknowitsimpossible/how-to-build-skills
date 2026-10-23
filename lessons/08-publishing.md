# 8. Publish and share

A skill is just a folder, so sharing it is mostly about putting that folder somewhere people can get it, and explaining it to the humans who will install it.

## Repository layout

Keep the skill folder separate from the files for humans:

```text
my-skill-repo/
├── README.md                 # for humans: what it does, how to install
├── LICENSE
├── skills/
│   └── my-skill/             # the skill itself; this is what gets installed
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── tests/                    # test cases and script tests
├── tools/validate_skill.py   # optional: structure check
└── .github/workflows/ci.yml
```

Why `skills/my-skill/` instead of putting `SKILL.md` at the root?

- **Keep human-facing repository documentation separate when useful.** The open format permits a README inside a skill. A subfolder is a convenient publishing layout, not a loading requirement.
- **Users install just the skill folder,** without your tests, CI config, and screenshots.
- **It scales.** A second skill is just `skills/another-skill/`.

The [case study](../examples/03-readme-organizer/) moved from a root `SKILL.md` to this layout for exactly these reasons.

## The repo README

The README is for a person deciding whether to install your skill. Write about outcomes, not mechanics:

| Weak | Strong |
|---|---|
| "A folder with YAML frontmatter and Markdown instructions for READMEs." | "Turns a finished project into one a stranger can understand, install, and run, by writing its README or reviewing the one you have." |

Include:

1. **What it does**, in one or two sentences, plus a short bullet list of what it handles.
2. **Installation** for each agent you support, with copy-paste commands ([platform pages](../platforms/) have the paths).
3. **Usage:** what to type, and what happens next.
4. **An example** of real output, before and after if you can.
5. **License.**

### Install by link, not by copy

Tell users to clone your repo somewhere permanent and **symlink** the skill into their agent's folder. Then `git pull` updates the skill:

```bash
git clone https://github.com/you/my-skill-repo.git ~/code/my-skill-repo
mkdir -p ~/.claude/skills
ln -s ~/code/my-skill-repo/skills/my-skill ~/.claude/skills/my-skill
```

For Codex, the target is `~/.agents/skills/my-skill`. For claude.ai, users upload a zip of the skill folder ([platform page](../platforms/claude-ai.md)).

## Versioning

- Put the version in `metadata.version` and bump it whenever behavior changes: `1.0.0` to `1.1.0` for new behavior, `1.0.1` for a fix.
- Write commit messages that say *what changed in the agent's behavior* and why ("Ignore untracked agent folders in the readiness check"), so the history doubles as a changelog.
- Tag releases (`git tag v1.2.0`) if people may want to pin a version.

## CI

Run automatic checks on every push to catch structural and script regressions. Behavioral failures still require realistic tests:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - run: python3 -m pip install -r requirements.txt
      - run: python3 tools/validate_skill.py skills
      - run: python3 -m unittest discover tests -v
```

This repo's own [`ci.yml`](../.github/workflows/ci.yml) does the same for the examples. You can copy [`tools/validate_skill.py`](../tools/validate_skill.py) into your repo; it's MIT-licensed. Copy `requirements.txt` too, since YAML validation uses PyYAML.

## Before you publish: checklist

- [ ] Folder name is kebab-case and matches `name`
- [ ] `SKILL.md` spelled exactly; frontmatter has both `---` lines
- [ ] Description has what, when (real phrases), and what not
- [ ] Target-platform restrictions checked; no secrets anywhere
- [ ] Additional files serve a useful purpose; no duplicated instructions
- [ ] Every file `SKILL.md` mentions exists
- [ ] Triggering, functional, and performance tests done ([lesson 6](06-testing.md))
- [ ] Repo README with install steps for each agent you support
- [ ] `LICENSE` file and `license` field
- [ ] CI passing

## After you publish

Watch how it's actually used. If people keep invoking it by name, it's under-triggering; if they complain it shows up uninvited, it's over-triggering. Treat reports as evidence to reproduce, then test the smallest useful correction ([lesson 6](06-testing.md)).

## Your deliverable

A release checklist and tested installation steps.

**Self-check:** Are format checks, platform compatibility, and observed behavior reported separately?

**You've finished the lessons.** Pick an example, choose the [minimal](../templates/SKILL.minimal.md) or [workflow template](../templates/SKILL.template.md), and build your own.
