# Template: CLI tool

A visitor wants to know: what command do I type, and what will happen?

## Skeleton

````markdown
# tool-name

One sentence: what the tool does.

## What it does

A short paragraph, then highlights.

- Highlight 1
- Highlight 2

## Installation

```bash
pipx install tool-name        # or: npm install -g, cargo install, brew install
```

Requires ...

## Usage

```bash
tool-name input.txt --output result.json
```

Example output:

```text
Processed 120 rows in 0.4s → result.json
```

### Options

| Option | Description | Default |
|---|---|---|
| `-o, --output` | Output file | `stdout` |

## Development
````

## Type-specific notes

- **Command name:** use the name from `"bin"` / `[project.scripts]` / `[[bin]]`, not the repo name, when they differ.
- **Options table:** build it from the argument parser definitions in the source (argparse `add_argument`, click decorators, commander `.option`, clap derives). Include only options that exist. If there are more than ~8, show the common ones and point to `tool-name --help`.
- **Show real output** when you can run the tool safely (no network, no writes outside a temp dir). Otherwise describe the output and don't fake it.
- If the tool is run as a script rather than installed (`python main.py ...`), say so plainly. Don't pretend it's installable.
