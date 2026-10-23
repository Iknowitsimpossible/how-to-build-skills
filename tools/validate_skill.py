#!/usr/bin/env python3
"""Validate skill structure and YAML; lint portability and authoring choices.

Usage: python3 tools/validate_skill.py [path ...]
Install requirements.txt first. Errors identify invalid structure, YAML, field
values, or missing referenced resources. Warnings identify platform compatibility
concerns and style suggestions; they do not establish whether a skill will load.
Exit code: 0 without errors, 1 otherwise. This does not test agent behavior.
"""
import re
import sys
from pathlib import Path

import yaml

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


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects ambiguous duplicate mapping keys."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in result:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate key: {key}", key_node.start_mark)
            result[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                None, None, "mapping keys must be hashable", key_node.start_mark) from exc
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def split_frontmatter(text):
    """Extract YAML using exact delimiter lines, not prefix matches."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    for index, line in enumerate(lines[1:], 1):
        if line == "---":
            return "\n".join(lines[1:index])
    return None


def parse_fields(block):
    """Parse safe YAML and require a mapping with string field names."""
    try:
        fields = yaml.load(block, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return {}, [f"invalid YAML: {exc}"]
    if not isinstance(fields, dict) or not all(isinstance(k, str) for k in fields):
        return {}, ["frontmatter must be a mapping with string field names"]
    return fields, []


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
    if problems:
        return problems, warnings
    for key in ("name", "description", "license", "compatibility", "allowed-tools"):
        if key in fields and not isinstance(fields[key], str):
            errors.append(f"{key} must be a string")
    if "metadata" in fields:
        metadata = fields["metadata"]
        if not isinstance(metadata, dict) or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()):
            errors.append("metadata must map string keys to string values")
    if errors:
        return errors, warnings

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
            warnings.append(f"compatibility: name '{name}' uses a Claude-reserved word ({', '.join(RESERVED_WORDS)}); check the target platform")

    description = fields.get("description", "")
    if not description.strip():
        errors.append("frontmatter has no description")
    else:
        if len(description) > MAX_DESCRIPTION:
            errors.append(f"description is {len(description)} characters (max {MAX_DESCRIPTION})")
        if not any(hint in description.lower() for hint in WHEN_HINTS):
            warnings.append("style: description may not explain when to use the skill; review its meaning, not just keywords")

    compatibility = fields.get("compatibility")
    if compatibility is not None and not compatibility.strip():
        errors.append("compatibility must be non-empty when provided")
    if compatibility is not None and len(compatibility) > MAX_COMPATIBILITY:
        errors.append(f"compatibility is {len(compatibility)} characters (max {MAX_COMPATIBILITY})")

    for key, value in fields.items():
        if "<" in str(value) or ">" in str(value):
            warnings.append(f"compatibility: {key} contains < or >; check restrictions on the target platform")

    for key in sorted(set(fields) - SPEC_FIELDS):
        warnings.append(f"compatibility: '{key}' is outside the open spec; support depends on the target agent")

    if (skill_dir / "README.md").exists():
        warnings.append("style: README.md inside the skill is allowed; keep it only if it serves a useful purpose")

    for path in sorted(set(BUNDLED_PATH.findall(text))):
        if not (skill_dir / path).exists():
            errors.append(f"resource: SKILL.md mentions {path}, which does not exist")

    words = len(text.split())
    if words > MAX_WORDS:
        warnings.append(f"style: SKILL.md is {words} words; consider moving conditional detail to references/ (not a loading limit)")
    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        warnings.append(f"style: SKILL.md is {lines} lines (aim for under {MAX_LINES})")

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
