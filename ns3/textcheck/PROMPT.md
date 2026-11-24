# Text-only check

You will read 50 short descriptions of units inside a small neural network that plays Connect Four. Each item has a
`description` (when the unit is active) and an `effect` (what it does to the model's move when it is pushed up or down).

For each item, answer one question with "yes" or "no":

> Does this describe the opponent threatening to win, or blocking it?

Answer "yes" if the description and effect, read together, are about the opponent having (or being about to have) a way
to win, or about the player to move blocking that, even if they also mention other things. Answer "no" otherwise. Judge
only the text. Do not run code and do not look for other files.

Write `answers.json` as a single JSON object mapping each item id to "yes" or "no", for example
{"T01": "no", "T02": "yes", ...}, with all 50 ids. Then add `reasons.json` with one short sentence per id.
