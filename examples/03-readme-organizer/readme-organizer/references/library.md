# Template: Library / package

A visitor wants to know: does this solve my problem, how do I install it, and what does calling it look like?

## Skeleton

````markdown
# package-name

One sentence: what the library does.

[CI badge] [version badge] [license badge]   <!-- only real ones -->

## What it does

A short paragraph on the problem and approach. If well-known alternatives exist, one sentence on how this one differs, said respectfully.

- Highlight 1
- Highlight 2
- Highlight 3

## Installation

```bash
pip install package-name
```

Requires Python 3.10+.

## Usage

```python
from package_name import thing

result = thing("input")
print(result)  # expected output
```

Then 1–3 more short examples covering the most common tasks.

## Documentation   <!-- link out if docs exist; do not document the whole API here -->
## Development      <!-- clone, install in editable mode, run tests -->
## License
````

## Type-specific notes

- **Show code early.** The first usage example should be the smallest snippet that does something useful, with its expected output in a comment.
- **Published vs not:** use `pip install name` / `npm install name` only if the package is actually published (name + version in the manifest and the user confirms, or a registry badge/URL exists). Otherwise install from git: `pip install git+https://github.com/user/repo`.
- **Import name differs from package name?** Show both explicitly (common in Python).
- **Don't dump the API.** Cover the 2–4 most common tasks. Link to generated docs if they exist.
- Put test and build commands under *Development*, not *Installation*.
