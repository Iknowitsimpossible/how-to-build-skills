"""Tests for tools/validate_skill.py.

Each test writes a small skill into a temp folder and checks which errors and
warnings the validator reports. The last class runs the validator on the real
examples and template, so a broken example fails CI.

Run from the repo root:
    python3 -m unittest discover tests
"""
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import validate_skill  # noqa: E402

GOOD_DESCRIPTION = "Does one thing well. Use when the user asks for that thing."


class SkillTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def make_skill(self, frontmatter, body="# Title\n", folder="my-skill", filename="SKILL.md"):
        skill_dir = self.root / folder
        skill_dir.mkdir(parents=True, exist_ok=True)
        text = "---\n" + textwrap.dedent(frontmatter).strip() + "\n---\n\n" + body
        (skill_dir / filename).write_text(text)
        return skill_dir

    def simple_skill(self, name="my-skill", description=GOOD_DESCRIPTION, extra="", **kwargs):
        frontmatter = f"name: {name}\ndescription: {description}\n{extra}"
        return self.make_skill(frontmatter, **kwargs)

    def check(self, skill_dir):
        return validate_skill.validate(skill_dir)

    def assertHasError(self, skill_dir, fragment):
        errors, _ = self.check(skill_dir)
        self.assertTrue(any(fragment in e for e in errors), f"no error containing {fragment!r} in {errors}")

    def assertHasWarning(self, skill_dir, fragment):
        _, warnings = self.check(skill_dir)
        self.assertTrue(any(fragment in w for w in warnings), f"no warning containing {fragment!r} in {warnings}")


class TestValidSkills(SkillTestCase):
    def test_minimal_skill_passes_cleanly(self):
        self.assertEqual(self.check(self.simple_skill()), ([], []))

    def test_all_spec_fields_pass(self):
        skill = self.make_skill("""
            name: my-skill
            description: "Quoted description. Use when testing."
            license: MIT
            compatibility: Requires Python 3.10 or newer.
            allowed-tools: Bash(git:*) Read
            metadata:
              author: someone
              version: "1.0.0"
        """)
        self.assertEqual(self.check(skill), ([], []))

    def test_folded_description_is_read(self):
        skill = self.make_skill("""
            name: my-skill
            description: >
              Spread over two lines.
              Use when testing.
        """)
        self.assertEqual(self.check(skill), ([], []))


class TestFileAndFrontmatter(SkillTestCase):
    def test_missing_skill_file(self):
        (self.root / "my-skill").mkdir()
        self.assertHasError(self.root / "my-skill", "missing SKILL.md")

    def test_wrong_case_is_explained(self):
        skill = self.simple_skill(filename="skill.md")
        self.assertHasError(skill, "found skill.md; the name is case-sensitive")

    def test_missing_delimiters(self):
        skill = self.root / "my-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(f"name: my-skill\ndescription: {GOOD_DESCRIPTION}\n")
        self.assertHasError(skill, "--- lines")

    def test_unclosed_quote(self):
        skill = self.simple_skill(description='"Does things. Use when asked.')
        self.assertHasError(skill, "never closes")

    def test_readme_inside_skill(self):
        skill = self.simple_skill()
        (skill / "README.md").write_text("# Hi\n")
        self.assertHasError(skill, "README.md belongs at the repo root")


class TestName(SkillTestCase):
    def test_missing_name(self):
        self.assertHasError(self.make_skill(f"description: {GOOD_DESCRIPTION}"), "no name")

    def test_bad_names(self):
        for name in ("My-Skill", "my_skill", "my skill", "-my-skill", "my-skill-", "my--skill"):
            with self.subTest(name=name):
                self.assertHasError(self.simple_skill(name=name), "lowercase letters")

    def test_name_must_match_folder(self):
        self.assertHasError(self.simple_skill(name="other-name"), "does not match folder")

    def test_name_too_long(self):
        name = "a" * 65
        self.assertHasError(self.simple_skill(name=name, folder=name), "max 64")

    def test_reserved_words(self):
        for name in ("claude-helper", "my-anthropic-tool"):
            with self.subTest(name=name):
                self.assertHasError(self.simple_skill(name=name, folder=name), "reserved word")


class TestDescriptionAndFields(SkillTestCase):
    def test_missing_description(self):
        self.assertHasError(self.make_skill("name: my-skill"), "no description")

    def test_description_too_long(self):
        long = "Use when testing. " + "x" * 1024
        self.assertHasError(self.simple_skill(description=long), "max 1024")

    def test_description_without_when_warns(self):
        self.assertHasWarning(self.simple_skill(description="Helps with projects."), "when to use")

    def test_angle_brackets(self):
        skill = self.simple_skill(description="Use when the user pastes <html>.")
        self.assertHasError(skill, "contains < or >")

    def test_angle_brackets_in_metadata(self):
        skill = self.simple_skill(extra="metadata:\n  author: Name <me@example.com>")
        self.assertHasError(skill, "metadata contains < or >")

    def test_compatibility_too_long(self):
        skill = self.simple_skill(extra="compatibility: " + "x" * 501)
        self.assertHasError(skill, "max 500")

    def test_unknown_field_warns_only(self):
        skill = self.simple_skill(extra="disable-model-invocation: true")
        errors, warnings = self.check(skill)
        self.assertEqual(errors, [])
        self.assertTrue(any("disable-model-invocation" in w for w in warnings))


class TestBody(SkillTestCase):
    def test_missing_bundled_file(self):
        skill = self.simple_skill(body="Read references/guide.md first.\n")
        self.assertHasError(skill, "references/guide.md")

    def test_existing_bundled_file_passes(self):
        skill = self.simple_skill(body="Run scripts/check.py when done.\n")
        (skill / "scripts").mkdir()
        (skill / "scripts" / "check.py").write_text("")
        self.assertEqual(self.check(skill), ([], []))

    def test_too_many_words(self):
        self.assertHasError(self.simple_skill(body="word " * 5001), "words")

    def test_too_many_lines_warns(self):
        self.assertHasWarning(self.simple_skill(body="line\n" * 501), "lines")


class TestDiscovery(SkillTestCase):
    def test_finds_nested_skills(self):
        self.simple_skill(folder="a/first-skill", name="first-skill")
        self.simple_skill(folder="b/c/second-skill", name="second-skill")
        names = [d.name for d in validate_skill.find_skill_dirs(self.root)]
        self.assertEqual(names, ["first-skill", "second-skill"])

    def test_skill_folder_itself(self):
        skill = self.simple_skill()
        self.assertEqual(validate_skill.find_skill_dirs(skill), [skill])


class TestRealExamples(unittest.TestCase):
    def test_examples_pass(self):
        result = subprocess.run(
            [sys.executable, str(REPO / "tools" / "validate_skill.py"), str(REPO / "examples")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("3 passed, 0 failed", result.stdout)

    def test_template_frontmatter_parses(self):
        text = (REPO / "templates" / "SKILL.template.md").read_text()
        block = validate_skill.split_frontmatter(text)
        self.assertIsNotNone(block)
        fields, problems = validate_skill.parse_fields(block)
        self.assertEqual(problems, [])
        self.assertIn("name", fields)
        self.assertIn("description", fields)


if __name__ == "__main__":
    unittest.main()
