# Quizlet format

## File

Save a UTF-8 `.txt` file with one card per line: the term, a **tab**, then the definition. No header line.

```text
ATP	Adenosine triphosphate, the cell's energy currency
1066	Battle of Hastings
```

Quizlet calls the front a "term" and the back a "definition". Commas are fine inside either side, because the tab separates them. Don't use a tab or a line break inside a card.

Quizlet has no cloze cards. If the user asks for them, write normal cards with the blank as the question (for example "The powerhouse of the cell is the ___") and say why.

## Import steps to give the user

1. On quizlet.com, create a new study set and click **Import**.
2. Paste the whole file into the box.
3. Leave "Between term and definition" on **Tab** and "Between cards" on **New line**, check the preview, then click **Import**.
