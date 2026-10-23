#!/usr/bin/env python3
"""Check skill folders against the Agent Skills spec and Anthropic's skill guide.

Usage:
    python3 tools/validate_skill.py [path ...]

Each path is either a skill folder (it contains SKILL.md) or a folder to
search for skills. With no paths, it searches examples/.

Errors (the skill may fail to load, or breaks a published rule):
  - SKILL.md exists with exactly that spelling
  - frontmatter is wrapped in --- lines and has no unclosed quotes
  - name: 1-64 characters, lowercase letters, digits and single hyphens,
    matches the folder, and avoids the reserved words "claude"/"anthropic"
  - description: present and at most 1024 characters
  - compatibility: at most 500 characters if present
  - no < or > in any frontmatter value
  - no README.md inside the skill folder
  - every references/, scripts/ or assets/ path mentioned in SKILL.md exists
  - SKILL.md is under 5,000 words

Warnings (the skill loads, but probably works worse):
  - SKILL.md is over 500 lines
  - the description never says when to use the skill
  - a top-level field is not in the open spec (fine if your agent supports it)

Exit code: 0 if no skill has errors, 1 otherwise. Standard library only.
"""
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_WORDS = ("claude", "anthropic")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_WORDS = 5000
MAX_LINES = 500
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
WHEN_HINTS = ("use when", "use for", "use this when", "use it when", "when the user", "when user")
BUNDLED_PATH = re.compile(r"\b((?:references|scripts|assets)/[\w./-]+\.\w+)")
FIELD_LINE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")


def split_frontmatter(text):
    """Return the text between the opening and closing --- lines, or None."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[4:end + 1]


def parse_fields(block):
    """Read top-level `key: value` pairs from a frontmatter block.

    This is not a full YAML parser. It handles what skills actually use:
    plain or quoted one-line values, block scalars (`>` or `|`) and indented
    continuation lines, and nested maps such as metadata (kept as raw text).
    Returns (fields, problems), where problems are syntax errors found.
    """
    fields = {}
    problems = []
    current = None
    for line in block.splitlines():
        match = FIELD_LINE.match(line)
        if match and not line.startswith((" ", "\t")):
            current, value = match.group(1), match.group(2).strip()
            if value in (">", "|", ">-", "|-"):
                value = ""
            fields[current] = value
            for quote in ('"', "'"):
                if value.startswith(quote) and (len(value) < 2 or not value.endswith(quote)):
                    problems.append(f"{current} opens a {quote} quote that never closes")
        elif current and line.strip():
            fields[current] = (fields[current] + " " + line.strip()).strip()
    for key, value in fields.items():
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            fields[key] = value[1:-1]
    return fields, problems


def find_skill_file(skill_dir):
    """Return (path, error). The error explains a near-miss like skill.md."""
    names = [p.name for p in skill_dir.iterdir()]
    if "SKILL.md" in names:
        return skill_dir / "SKILL.md", None
    wrong = [n for n in names if n.lower() == "skill.md"]
    hint = f" (found {wrong[0]}; the name is case-sensitive)" if wrong else ""
    return None, f"missing SKILL.md{hint}"


def validate(skill_dir):
    """Return (errors, warnings) for one skill folder."""
    errors, warnings = [], []
    skill_file, error = find_skill_file(skill_dir)
    if error:
        return [error], warnings

    text = skill_file.read_text(encoding="utf-8")
    block = split_frontmatter(text)
    if block is None:
        return ["frontmatter must start and end with --- lines"], warnings
    fields, problems = parse_fields(block)
    errors.extend(problems)

    name = fields.get("name", "")
    if not name:
        errors.append("frontmatter has no name")
    else:
        if len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} characters (max {MAX_NAME})")
        if not NAME_PATTERN.match(name):
            errors.append(f"name '{name}' must be lowercase letters, digits, and single hyphens")
        if name != skill_dir.name:
            errors.append(f"name '{name}' does not match folder '{skill_dir.name}'")
        if any(word in name for word in RESERVED_WORDS):
            errors.append(f"name '{name}' uses a reserved word ({', '.join(RESERVED_WORDS)})")

    description = fields.get("description", "")
    if not description:
        errors.append("frontmatter has no description")
    else:
        if len(description) > MAX_DESCRIPTION:
            errors.append(f"description is {len(description)} characters (max {MAX_DESCRIPTION})")
        if not any(hint in description.lower() for hint in WHEN_HINTS):
            warnings.append("description never says when to use the skill (e.g. 'Use when ...')")

    compatibility = fields.get("compatibility")
    if compatibility is not None and len(compatibility) > MAX_COMPATIBILITY:
        errors.append(f"compatibility is {len(compatibility)} characters (max {MAX_COMPATIBILITY})")

    for key, value in fields.items():
        if "<" in value or ">" in value:
            errors.append(f"{key} contains < or >, which are not allowed in frontmatter")

    for key in sorted(set(fields) - SPEC_FIELDS):
        warnings.append(f"'{key}' is not in the open spec; agents that don't know it will ignore it")

    if (skill_dir / "README.md").exists():
        errors.append("README.md belongs at the repo root, not inside the skill folder")

    for path in sorted(set(BUNDLED_PATH.findall(text))):
        if not (skill_dir / path).exists():
            errors.append(f"SKILL.md mentions {path}, which does not exist")

    words = len(text.split())
    if words > MAX_WORDS:
        errors.append(f"SKILL.md is {words} words (keep it under {MAX_WORDS}; move detail to references/)")
    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        warnings.append(f"SKILL.md is {lines} lines (aim for under {MAX_LINES})")

    return errors, warnings


def find_skill_dirs(root):
    """A folder with SKILL.md (any case) is a skill; otherwise search inside it."""
    if not root.is_dir():
        return []
    if any(p.name.lower() == "skill.md" for p in root.iterdir()):
        return [root]
    found = {p.parent for p in root.rglob("*") if p.is_file() and p.name.lower() == "skill.md"}
    return sorted(found)


def main(argv):
    roots = [Path(arg) for arg in argv] or [Path("examples")]
    skill_dirs = [d for root in roots for d in find_skill_dirs(root)]
    if not skill_dirs:
        print(f"ERROR: no skills found in {', '.join(str(r) for r in roots)}")
        return 1

    failed = 0
    for skill_dir in skill_dirs:
        errors, warnings = validate(skill_dir)
        print(f"{'FAIL' if errors else 'OK  '}  {skill_dir}")
        for error in errors:
            print(f"      error:   {error}")
        for warning in warnings:
            print(f"      warning: {warning}")
        failed += bool(errors)

    print(f"\n{len(skill_dirs) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
