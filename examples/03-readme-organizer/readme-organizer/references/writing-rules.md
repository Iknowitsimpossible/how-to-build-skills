# Writing rules

These apply to every project type. Templates add type-specific rules on top.

## Accuracy

- Every command, flag, URL, version, and feature must trace to a fact gathered in Step 2. If something can't be confirmed, write `<!-- TODO: ... -->`.
- State minimum requirements only when the repo specifies them (`engines`, `requires-python`, `rust-version`, `.nvmrc`). Otherwise say what it was built with, e.g. "Tested with Python 3.12".
- Translate version ranges into plain language: `^22.12.0 || ^24.0.0 || >=26.0.0` becomes "Node.js 22.12 or newer".
- Show real output only if you actually ran the command. Otherwise describe it.

## Structure

- Core order: title, one-line description, **What it does**, **Installation**, **Usage**. Optional sections come after Usage.
- The title is the project's name. Directly under it, add one sentence saying what it is and who it's for.
- If the project is deployed or published, put the link (live demo, package page) right under that sentence. For many visitors that is the main way to use it.
- Badges only when they report something real: an existing CI workflow, a published package version, a license file.
- Optional sections, only with real content: *Configuration*, *Project structure*, *Development* / *Contributing*, *Acknowledgments*, *License*.
- Keep build-from-source and contributor setup out of *Installation*. Put them under *Development*.
- Headings may fit the project ("Run it yourself", "Controls", "How to play") as long as the three core topics are covered in order.

## Style

- Be concise. Cut any sentence that doesn't help a reader decide, install, or use.
- Write for a newcomer: spell out `git clone` and `cd`, and link to where runtimes can be installed (e.g. nodejs.org).
- Put every command in a fenced code block with a language tag (`bash`, `python`, `js`, ...). Use one command per line, without a leading `$`.
- Lead with outcomes, not implementation. "Take penalties with a swipe, then dive to save theirs" beats "Uses three.js and a physics module".
- No emojis.
- Use relative links for repo files (`[LICENSE](LICENSE)`) and absolute links for everything else.
- Visual projects (web apps, games, UIs) need a screenshot or GIF. Use a tracked image if one exists. Otherwise add `<!-- TODO: add screenshot at docs/screenshot.png -->` and tell the user how to make one (macOS: Cmd+Shift+5). Never link an image that doesn't exist.
