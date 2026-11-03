# Workflow

The Unit 2 card took about an hour from first file listing to final PDF. Follow these steps in order.

## 1. Confirm the brief

These held for Unit 2, so assume them unless told otherwise:

- A 3 × 5 double-sided printed card is allowed, delivered as a 6 × 5 sheet.
- No CAS calculator on the exam.
- Testing center staff stamp the card.
- The printer is about 1200 DPI. The user reported the Unit 1 card at 3.92 pt as "EASY to read", and the printed Unit 2 card at 3.54 pt as great, with room to go smaller.

Ask only about what you can't find out: the lessons covered, if the topic list is missing, and whether a basic calculator is allowed.

## 2. Inventory the sources

```bash
for f in *.pdf; do
  echo "$(pdfinfo "$f" | awk '/^Pages:/{print $2}') pages, $(pdftotext "$f" - | wc -c) chars: $f"
done
pdfimages -list "big file.pdf" | head   # a huge one-page PDF is probably a collage
```

A low character count on a large file means it's images, so plan to view it.

## 3. Read in this order

1. **Topic list.** It fixes the scope.
2. **Equation sheet, as PNGs.** `pdftotext -layout` scrambles its two columns. Render with `pdftoppm -r 110 -png`.
3. **Lessons.** `pdftotext` works for prose, but tables and figures are images. Lesson 10's quadric table never appeared in the text.
4. **Quizzes, with answer explanations.** These show real question formats, answer-entry rules, and the user's own misses.
5. **The user's notes and collages.** Their annotations are high-signal. "WATCH FOR X AND Y QUADRANT" and "for cyn -> rect use double angle identity" both became card entries.
6. **AI-generated notes.** Treat these as secondary. The Unit 2 compilation ran past the exam's lessons and needed scoping.

To read a large collage, tile it directly from the PDF:

```bash
for r in 0 1 2 3 4 5; do for c in 0 1 2; do
  pdftoppm -r 300 -png -x $((c*850)) -y $((r*550)) -W 850 -H 550 -singlefile collage.pdf "t_r${r}_c${c}"
done; done
```

## 4. Map the sheet

Check [equation-sheet-map.md](equation-sheet-map.md) against the current sheet, since a new version may reorder things. Count formulas from the rendered page.

## 5. List the problem types

Go lesson by lesson and write down every numbered example and quiz question as a problem type. This checklist is how you know the card is complete. See [content.md](content.md).

## 6. Set up the tools

```bash
which tectonic || brew install tectonic   # first compile downloads the bundle: a minute or two
```

Copy the templates into the user's folder and draft there. Later compiles of a full card take about a second. Write the whole card in one pass using the rules in [typesetting.md](typesetting.md), then compile.

## 7. Fit the size

```bash
tools/fit_size.sh UnitN_Notecard_6x5.tex 3.50 3.55 3.58 3.60
python3 tools/card_stats.py UnitN_Notecard_6x5.pdf
```

The final Unit 2 content measured:

| Body size | Result |
|---|---|
| 3.50 | 79 pt free in column 4 |
| 3.55 | 30.5 pt free (shipped) |
| 3.58 | 3 lines over |
| 3.60 | 10 lines over, and 7 pt stranded in column 3 |

Near a full card, each extra 0.01 pt of body size costs about 10 pt of column height. Don't assume a size that overflows is simply too big: a header pushed to the next column can strand several lines, so check the blanks in columns 1 to 3.

If the content really doesn't fit, go smaller before cutting anything, since the Unit 2 card wasn't near the user's limit. For a big drop, offer a test print first.

## 8. Proof

Do all three passes.

1. **Layout.** Run `tools/proof_tiles.sh card.pdf tiles` and view all 12 tiles at 600 DPI. Look for collisions, merged tags, fake underlines, and orphaned headers. Zoom on anything doubtful with `pdftoppm -r 1200 -x ... -y ... -W ... -H ...`.
2. **Text.** Dump the card with `pdftotext` and read every line. Math comes out as readable Unicode.
3. **Math.** Recompute every worked example and check every sheet tag against the rendered sheet.

Also check the log, which needs `--keep-logs`:

```bash
out=$(mktemp -d)
tectonic -X compile --keep-logs --outdir "$out" card.tex
grep -c Overfull "$out/card.log"
grep "Missing character" "$out/card.log" | sort -u
```

## 9. Spend the leftover space

Add high-value extras first, marked ★. Unit 2 used textbook-standard problem types the lessons skipped and shortcuts like `N = (a − a_T T)/a_N`. Then set `\stampheight` to the column 4 blank minus about 2.5 pt, which leaves a gap under the last line of text.

## 10. Deliver

Build in place, with no `--outdir`. Tectonic then writes only the PDF next to the source.

```bash
tectonic -X compile UnitN_Notecard_6x5.tex
tectonic -X compile UnitN_Notecard_Letter.tex   # second, because it embeds the card PDF
ls -la UnitN_*                                   # every file you are about to link
pdfinfo UnitN_Notecard_6x5.pdf | grep -E "Pages|Page size"      # 1 page, 432 x 360 pts
pdfinfo UnitN_Notecard_Letter.pdf | grep -E "Pages|Page size"   # 1 page, 612 x 792 pts
pdffonts UnitN_Notecard_Letter.pdf                              # all embedded
```

Confirm the sheet is at 100%: a word's position should differ from the card by exactly 90 pt in x and 216 pt in y.

```bash
pdftotext -bbox UnitN_Notecard_6x5.pdf - | grep -m1 ">MATH<"
pdftotext -bbox UnitN_Notecard_Letter.pdf - | grep -m1 ">MATH<"
```

## 11. Hand over

Link both PDFs, state the print setting (100% / Actual size), and flag any choice the user might want to reverse. They appreciated having the stamp-ink problem raised before they asked. Ask how the card printed, then record it in the README.
