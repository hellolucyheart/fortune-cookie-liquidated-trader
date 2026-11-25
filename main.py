#!/usr/bin/env python3
"""Fortune Cookie for the Liquidated Trader — make.fun bounty entry.

Writes exactly one fortune cookie line for a crypto trader who has
just been liquidated, at most 20 words of plain text, to
/output/entry.txt. The line is the whole entry: it has to sound like
a real fortune and land as a joke on the loss. A judge model plays
the freshly liquidated trader and reads fortunes two at a time,
keeping the one that earns a laugh rather than a tear, round after
round until one fortune tops the board.

The judge weighs, most important first:

1. the line sounds like a real fortune — a slip's voice, not a
   tweet or a status update; anything that is not one loses to any
   that is;
2. the joke lands on the loss itself: funny on first read, with a
   turn or a surprise, aimed at the liquidation, not at trading in
   general;
3. the line is original: not a stock fortune, not a stock trading
   joke, not a pun already worn out;
4. it speaks to the liquidated trader's own condition — the margin
   call, the leverage, the exchange taking its fee — in a way that
   earns the joke;
5. it reads as one crisp line a cookie could hold, with no wasted
   words. Shorter is strictly better when the judge cannot tell two
   apart, and the brief caps the line at 20 words.

The candidates below are scored on those five, in that order, and
the highest-scoring line wins. Ties break toward the shorter line.

Candidate A — "your bright future, collected". "Your future is
bright" is the most classic fortune opening there is, and the turn
lands on the last words: the exchange has already collected that
bright future as a liquidation fee. The joke names the loss itself
— the fee is what took the money — and it wastes nothing: the
setup is the joke, and at fourteen words it is the joint-shortest
of the six.

Candidate B — "tall, dark stranger". "You will meet a tall, dark
stranger" is the fortune slip's own voice, and the reveal — the
stranger is your margin call, in a suit made of liquidations — is
a genuine surprise that speaks to the trader's condition. But the
suit image explains the joke a beat too long, and at sixteen words
it spends two more than A for a softer landing on the loss itself.

Candidate C — "lucky numbers". "Your lucky numbers are..." is the
fortune slip's signature, and the leverage you swore never to use
again is the trader's condition in one number. The joke, though,
is mild: a rueful nod rather than a laugh, and "lucky numbers"
with a 0 and a 100 flirts with the stock trading joke the brief
warns about.

Candidate D — "the stars say". "The stars say your portfolio will
recover" is a real fortune voice, and "they just didn't say which
lifetime" has a turn. But the joke is a known shape — the delayed
prophecy gag has been told a thousand times — so it scores lower
on originality than A, and it jokes about the recovery, not the
liquidation itself.

Candidate E — "a great fortune awaits". A classic fortune opening,
and "not in this wallet, and not in this market cycle" aims at
the loss. But the turn is a plain negation rather than a surprise,
and "not in this wallet" reads like a shrug, so it lands softer
than A on the second criterion.

Candidate F — "green candle". "Beware the green candle that
promises everything" opens like a warning slip, and "it is only
lighting your exit" has a turn. But a green candle is a market
observation, not the liquidation, so it speaks to the trader's
condition more weakly than A, and the fortune voice is thinner —
a warning about a candle is not quite a slip.

A wins on every count that matters, so the program writes it —
one line, 14 words, no trailing newline, UTF-8, exactly what the
gate checks.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

# Each candidate: (line, fortune-slip voice, joke lands on the loss,
# original, liquidated trader's own condition, crisp line), scored
# 1-5, in the judge's own order.
CANDIDATES = [
    (
        "Your future is bright: the exchange has already "
        "collected it as a liquidation fee.",
        5, 5, 4, 5, 5,
    ),
    (
        "You will meet a tall, dark stranger: your margin "
        "call, wearing a suit made of liquidations.",
        5, 5, 4, 5, 4,
    ),
    (
        "Your lucky numbers are 0, 100, and the leverage "
        "you swore you would never use again.",
        5, 4, 4, 5, 4,
    ),
    (
        "The stars say your portfolio will recover \u2014 "
        "they just didn't say which lifetime.",
        5, 4, 3, 4, 5,
    ),
    (
        "A great fortune awaits you \u2014 just not in this "
        "wallet, and not in this market cycle.",
        4, 4, 3, 4, 5,
    ),
    (
        "Beware the green candle that promises everything: "
        "it is only lighting your exit.",
        4, 4, 4, 4, 5,
    ),
]


def pick_line(candidates):
    """Pick the highest-scoring line; ties break toward the first.

    Weights follow the judge's order: the fortune-slip voice counts
    most, then the joke landing on the loss, then originality, then
    the liquidated trader's own condition, then crispness. On an
    exact score tie the shorter line wins: the brief's own shape
    prefers the smaller text, so a shorter line is strictly better
    when the judge cannot tell two apart.
    """
    weights = (5, 4, 3, 2, 1)
    best = None
    best_score = -1
    for entry in candidates:
        line, *scores = entry
        score = sum(w * s for w, s in zip(weights, scores))
        if score > best_score or (
            score == best_score and best is not None and len(line) < len(best)
        ):
            best = line
            best_score = score
    return best


def main():
    line = pick_line(CANDIDATES)
    words = line.split()
    assert 1 <= len(words) <= 20, "entry must be 1-20 words"
    assert "\n" not in line and line.strip() == line, "entry must be one line"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    print(line)
    # Read the entry back and prove the gate holds before finishing:
    # UTF-8 text, 1-20 words, not only whitespace, one line.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    assert text == line, "entry differs from the chosen line"
    assert 1 <= len(text.split()) <= 20 and text.strip(), "gate failed: bad length"
    assert "\n" not in text, "gate failed: entry is not one line"


if __name__ == "__main__":
    main()
