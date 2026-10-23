"""Tests for the flashcard-maker example's scripts/check_cards.py.

Each test writes a small deck to a temp file and runs the checker on it.

Run from the repo root:
    python3 -m unittest discover tests
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "examples" / "02-with-references" / "flashcard-maker"
CHECKER = SKILL / "scripts" / "check_cards.py"
ANKI_HEADER = "#separator:comma\n#html:false\n#columns:Front,Back\n"


class CheckCardsTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.deck = Path(self._tmp.name) / "deck.txt"

    def tearDown(self):
        self._tmp.cleanup()

    def run_checker(self, content, deck_format):
        self.deck.write_text(content)
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(self.deck), "--format", deck_format],
            capture_output=True, text=True,
        )
        return result.returncode, result.stdout


class TestAnki(CheckCardsTestCase):
    def test_valid_deck_with_quoted_commas(self):
        code, out = self.run_checker(
            ANKI_HEADER
            + "What does ATP stand for?,Adenosine triphosphate\n"
            + '"Name the two stages, in order","Light reactions, then the Calvin cycle"\n',
            "anki",
        )
        self.assertEqual(code, 0, out)
        self.assertIn("2 card(s), 0 error(s)", out)

    def test_unquoted_comma_is_three_fields(self):
        code, out = self.run_checker(ANKI_HEADER + "Name two stages,Light, Calvin\n", "anki")
        self.assertEqual(code, 1)
        self.assertIn("has 3 fields", out)

    def test_empty_back(self):
        code, out = self.run_checker(ANKI_HEADER + "What is ATP?,\n", "anki")
        self.assertEqual(code, 1)
        self.assertIn("a side is empty", out)

    def test_duplicate_fronts_ignore_case_and_spacing(self):
        code, out = self.run_checker(ANKI_HEADER + "What is ATP?,Energy\nwhat  is ATP?,Energy\n", "anki")
        self.assertEqual(code, 1)
        self.assertIn("line 5: same front as line 4", out)

    def test_long_front_is_only_a_warning(self):
        code, out = self.run_checker(ANKI_HEADER + "x" * 201 + ",y\n", "anki")
        self.assertEqual(code, 0, out)
        self.assertIn("warning: line 4: front is 201 characters", out)


class TestQuizletAndCloze(CheckCardsTestCase):
    def test_valid_quizlet(self):
        code, out = self.run_checker("ATP\tEnergy, for cells\n1066\tBattle of Hastings\n", "quizlet")
        self.assertEqual(code, 0, out)

    def test_quizlet_comma_is_not_a_separator(self):
        code, out = self.run_checker("ATP,Energy\n", "quizlet")
        self.assertEqual(code, 1)
        self.assertIn("has 1 fields", out)

    def test_cloze_needs_marker(self):
        code, out = self.run_checker("#notetype:Cloze\nThe cell has a nucleus.\n", "cloze")
        self.assertEqual(code, 1)
        self.assertIn("no {{c1::...}} marker", out)

    def test_valid_cloze(self):
        code, out = self.run_checker("The powerhouse is the {{c1::mitochondrion}}.\n", "cloze")
        self.assertEqual(code, 0, out)


class TestEdgeCases(CheckCardsTestCase):
    def test_empty_file(self):
        code, out = self.run_checker(ANKI_HEADER, "anki")
        self.assertEqual(code, 1)
        self.assertIn("no cards found", out)

    def test_missing_file(self):
        result = subprocess.run(
            [sys.executable, str(CHECKER), "does-not-exist.csv", "--format", "anki"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("not found", result.stdout)

    def test_sample_deck_passes(self):
        sample = REPO / "examples" / "02-with-references" / "sample" / "cell-biology-flashcards.csv"
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(sample), "--format", "anki"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
