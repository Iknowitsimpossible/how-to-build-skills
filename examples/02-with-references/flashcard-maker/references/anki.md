# Anki format

## File

Save a UTF-8 `.csv` file. Start it with these header lines so Anki picks the right settings without the user changing anything:

```text
#separator:comma
#html:false
#columns:Front,Back
```

Then one card per line: `front,back`. If a side contains a comma or a double quote, wrap that side in double quotes and double any quote inside it:

```text
What does ATP stand for?,Adenosine triphosphate
"Name the two stages of photosynthesis, in order","Light reactions, then the Calvin cycle"
"What did Descartes write after ""I think""?","""Therefore I am"""
```

Don't put line breaks inside a card. Keep each card on one line.

## Cloze cards

Only if the user asks for fill-in-the-blank cards. Use a separate file with these headers, and one sentence per line with the hidden part marked `{{c1::...}}`:

```text
#separator:tab
#html:false
#notetype:Cloze
The powerhouse of the cell is the {{c1::mitochondrion}}.
```

Run the checker with `--format cloze` on this file.

## Import steps to give the user

1. In Anki, choose **File, Import** and pick the file.
2. Check that the note type is **Basic** (or **Cloze** for cloze files) and that the deck is the one they want.
3. Click **Import**.
