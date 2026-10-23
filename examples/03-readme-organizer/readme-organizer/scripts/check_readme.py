#!/usr/bin/env python3
"""Check a README's commands and links against the repository it describes.

Usage:
    python3 check_readme.py <repo-dir> [readme-file]

readme-file defaults to README.md and is resolved relative to repo-dir.
It can also be README-SUGGESTIONS.md, to check proposed text before it is applied.

Checks:
  - relative links and images point to files tracked by git
  - `npm run X` / `npm start` / `npm test` / `yarn X` / `pnpm X` match package.json scripts
  - `make X` matches a Makefile target
  - `python file.py` / `node file.js` point to tracked files
  - `git clone` URLs match the repo's origin remote
  - lists TODO markers left in the file

To skip a section, such as an example quoted from another project, wrap it in
<!-- check-readme: off --> and <!-- check-readme: on -->.

Exit code: 0 if no errors, 1 if any error, 2 on bad usage.
Standard library only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

FENCE = re.compile(r"^(`{3,}|~{3,})")
MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_SRC = re.compile(r"<(?:img|a)\b[^>]*?(?:src|href)=\"([^\"]+)\"", re.IGNORECASE)
TODO = re.compile(r"<!--\s*TODO|\bTODO:")
CHECK_OFF = re.compile(r"<!--\s*check-readme:\s*off\s*-->")
CHECK_ON = re.compile(r"<!--\s*check-readme:\s*on\s*-->")

# Built-in npm commands that don't need a matching script.
NPM_BUILTINS = {"install", "i", "ci", "init", "update", "outdated", "audit", "link", "publish", "pack", "exec", "x"}


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def split_code_and_prose(text):
    """Return (code_lines, prose_lines) as lists of (line_number, line)."""
    code, prose = [], []
    fence = None
    skipping = False
    for number, line in enumerate(text.splitlines(), start=1):
        if CHECK_OFF.search(line):
            skipping = True
        elif CHECK_ON.search(line):
            skipping = False
        if skipping:
            continue
        marker = FENCE.match(line.strip())
        if marker:
            if fence is None:
                fence = marker.group(1)
                continue
            if line.strip().startswith(fence) and line.strip().strip("`~") == "":
                fence = None
                continue
        (code if fence else prose).append((number, line))
    return code, prose


def is_external(target):
    return target.startswith(("http://", "https://", "mailto:", "#", "data:", "//"))


def check_links(prose, tracked, readme_dir, repo):
    errors = []
    for number, line in prose:
        targets = MD_LINK.findall(line) + HTML_SRC.findall(line)
        for target in targets:
            if is_external(target):
                continue
            path = target.split("#")[0].split("?")[0]
            if not path:
                continue
            resolved = (readme_dir / path).resolve()
            try:
                relative = resolved.relative_to(repo.resolve()).as_posix()
            except ValueError:
                errors.append((number, f"link points outside the repo: {target}"))
                continue
            is_file = relative in tracked
            is_dir = any(f.startswith(relative.rstrip("/") + "/") for f in tracked)
            if not (is_file or is_dir):
                errors.append((number, f"link or image target is not a tracked file: {target}"))
    return errors


def load_package_scripts(repo):
    manifest = repo / "package.json"
    if not manifest.exists():
        return None
    try:
        return json.loads(manifest.read_text()).get("scripts", {})
    except json.JSONDecodeError:
        return None


def load_make_targets(repo):
    makefile = repo / "Makefile"
    if not makefile.exists():
        return None
    return set(re.findall(r"^([A-Za-z0-9_.-]+)\s*:(?!=)", makefile.read_text(), re.MULTILINE))


def normalize_remote(url):
    url = url.strip().removesuffix(".git").rstrip("/")
    url = re.sub(r"^git@([^:]+):", r"https://\1/", url)
    return url.lower()


def check_commands(code, repo, tracked):
    errors = []
    scripts = load_package_scripts(repo)
    make_targets = load_make_targets(repo)
    origin = git(repo, "remote", "get-url", "origin")

    for number, raw in code:
        line = raw.strip().lstrip("$ ").split(" #")[0]
        words = line.split()
        if not words:
            continue

        # npm / yarn / pnpm scripts
        if words[0] in ("npm", "yarn", "pnpm") and len(words) > 1:
            if words[1] == "run" and len(words) > 2:
                name = words[2]
            elif words[0] == "npm" and words[1] in ("start", "test", "t"):
                name = "test" if words[1] == "t" else words[1]
            elif words[0] != "npm" and words[1] not in ("install", "add", "dlx", "exec", "create"):
                name = words[1]
            else:
                name = None
            if name and words[1] not in NPM_BUILTINS:
                if scripts is None:
                    errors.append((number, f"`{line}` but there is no package.json with scripts"))
                elif name not in scripts:
                    errors.append((number, f"`{line}`: no \"{name}\" script in package.json"))

        # make targets
        elif words[0] == "make" and len(words) > 1 and not words[1].startswith("-"):
            if make_targets is None:
                errors.append((number, f"`{line}` but there is no Makefile"))
            elif words[1] not in make_targets:
                errors.append((number, f"`{line}`: no \"{words[1]}\" target in Makefile"))

        # python / node entry files
        elif words[0] in ("python", "python3", "node") and len(words) > 1:
            target = words[1]
            # Paths outside the repo (~/..., /usr/...) can't be checked against git.
            is_relative = not target.startswith(("~", "/", "$"))
            if is_relative and target.endswith((".py", ".js", ".mjs", ".cjs")) and target not in tracked:
                errors.append((number, f"`{line}`: {target} is not a tracked file"))

        # git clone URL
        elif words[:2] == ["git", "clone"] and len(words) > 2 and origin:
            if normalize_remote(words[2]) != normalize_remote(origin):
                errors.append((number, f"clone URL {words[2]} does not match origin {origin}"))

    return errors


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__.strip().splitlines()[2])
        return 2
    repo = Path(sys.argv[1])
    readme = repo / (sys.argv[2] if len(sys.argv) == 3 else "README.md")
    if not readme.exists():
        print(f"ERROR: {readme} does not exist")
        return 1

    files = git(repo, "ls-files")
    if files is None:
        print(f"ERROR: {repo} is not a git repository")
        return 1
    tracked = set(files.splitlines())

    text = readme.read_text()
    code, prose = split_code_and_prose(text)
    errors = check_links(prose, tracked, readme.parent, repo) + check_commands(code, repo, tracked)
    todos = [number for number, line in enumerate(text.splitlines(), start=1) if TODO.search(line)]

    for number, message in sorted(errors):
        print(f"ERROR line {number}: {message}")
    if todos:
        print(f"NOTE: TODO markers on lines {', '.join(map(str, todos))}")
    print(f"{readme.name}: {len(errors)} error(s), {len(todos)} TODO line(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
