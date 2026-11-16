# Gotchas

Everything that went wrong on the Unit 2 card.

## Layout

| Symptom | Cause | Fix |
|---|---|---|
| Lines collide around fractions | Stacked `\frac` with a negative `\lineskiplimit` | Slashed fractions |
| Numerators hard to read | Stacked fractions drop to about 2.2 pt | Slashed fractions |
| Words look underlined | A `\sqrt` vinculum reaches the previous line's baseline | `\rt` prefix radical |
| Lines pushed apart by `√` | The glyph is tall | `\smash`, already in `\rt` |
| Tags run together as `5L15L2` | Adjacent `\colorbox`es | `\sh{5L1}\,\sh{5L2}` |
| Both quotes come out as closing quotes | Straight `"` | ` `` ` and `''` |
| Size overflows despite apparent room | `\needspace` strands blank lines at column bottoms | Run `card_stats.py`, try nearby sizes, use 4 lines not 5 |
| Test swatch renders blank | Page too short, so content moved to page 2 | Make the page taller |

## Fonts and glyphs

| Symptom | Cause | Fix |
|---|---|---|
| `Missing character: ⇒ ... Bell` | `\Rightarrow` in text mode falls to the text font | `\then`, which uses `\ensuremath` |
| `Missing character: ▸ ... FiraMath` | Fira has no U+25B8 | `{\symf ▸}` |
| → missing in the letter-sheet caption | Bell lacks it | `$\rightarrow$` |
| `The font "LeteSansMath" cannot be found` | Not in the Tectonic bundle. Same for `NewCMSansMath-Regular` | See the list in [typesetting.md](typesetting.md) |
| Vectors aren't bold | `\mathbf` under `unicode-math` | `\symbf` |
| `Undefined control sequence \blacksquare` | Not defined under `unicode-math` | `{\symf ■}` |
| `½` looks broken | Bell's glyph | `(1/2)` |
| `Math alphabet identifier \mathrm is undefined in math version` | Every math font loaded with `version=`, and no default | Compile one swatch per font |

Any `Missing character` is silent in the PDF, so grep the log for it.

## LaTeX and Tectonic

| Symptom | Cause | Fix |
|---|---|---|
| `Command \sc already defined` | LaTeX owns `\sc` | The shortcut macro is `\shc` |
| No `.log` to inspect | Tectonic discards it | `--keep-logs` |
| Font not found with `Path=./` | The path is relative to the working directory | Compile from the source folder, or use the template's `\fontdir` |
| `accessing absolute path` warning | Fonts loaded by absolute path | Harmless |

## Measuring

| Symptom | Cause | Fix |
|---|---|---|
| Type size off by about 0.4% | TeX pt versus PDF pt | Report PDF sizes from `card_stats.py` |
| Size guessed wrong from bbox heights | `pdftotext -bbox` uses font ascent and descent | Read `Tf` values |
| "Lines free" estimates wrong | Mixed fonts spoil spacing inferred from bboxes | Measure blanks in points. One line is about 3.76 pt |

## Environment

| Symptom | Cause | Fix |
|---|---|---|
| `blake2` hashlib tracebacks | Printed when this pyenv Python starts from a venv | Harmless |
| Pillow or PyMuPDF missing | Not installed | Crop with `pdftoppm -x -y -W -H`, as `proof_tiles.sh` does |
| `sed -i` fails | macOS BSD sed | `sed -i ''` |
| Scratch files gone | The scratchpad is emptied between sessions | Keep sources in the user's folder or this repo |

## Editing and delivery

| Symptom | Cause | Fix |
|---|---|---|
| User gets errors opening a link | The PDF was built with `--outdir` and never copied | Build in place, `ls` before linking |
| A scripted replacement could hit the wrong text | "lies in the osculating plane" appeared twice | Assert `s.count(anchor) == 1` before every replace |
| Stamp too dark for ink to show | Solid black letters | Hollow outline, on by default in the template |

## Solid layout (Unit 3)

| Symptom | Cause | Fix |
|---|---|---|
| STAMP HERE printed over the last lines of text, or cut off at the bottom | Column 4 overfull, and nothing in the layout can shrink, so there is no second page and no warning | `solid_stats.py`: column 4 must have at least `\stamplines` free. Raise `\nlines`, trim, or shrink the stamp |
| Subscripts touch the superscripts on the next line | TeX's native script positions span 1.18 em and the pitch is 0.96 em | Active `^` and `_` mapped to `\supx` and `\subx` |
| `\fontdimen` changes to script shifts do nothing | XeTeX reads the OpenType MATH table directly | Wrap the script in a shifted, smashed box instead |
| Two scripts on one base overprint | Active scripts place each one alone | `\I`, `\ev`, or `(x_0)^2`. Run `check_scripts.py` |
| A power in a lower limit collides with the upper limit | No room between stacked limits | `\Ia{a}{b}`, which prints ∫[a→b] |
| Nested exponent reaches the line above | Second-level scripts rise to 1.07 em | Caret form: `e\cx(9t^{9/4}+8)` |
| Caret has wide gaps either side | Bell's `^` has a 0.5 em advance | Fira's: `\mathord{\symup{\char"5E}}` |
| Gap after ⟨ or ‖ before a minus sign; gap inside `\|cos u\|` | A smashed delimiter is an ordinary atom | `\mathopen{\smash{\langle}}`, `\mathclose{...}` |
| Two spaces after a ▸ label, or a space before its colon | `\pt` ended with its own `\ ` | `\pt` adds no space |
| "Option clash for package geometry" in a test file | A second `\usepackage[...]{geometry}` after the preamble's | `\geometry{...}` |
| Center dashes read as part of the last letter on a line | A dash 0.5 pt from the text looks like `\|` or `1` | Solid rule |
| Column rules might print as dotted lines (expected, not test-printed) | A gray hairline is halftoned | Solid black, 0.2 pt |
| Stacked limits `π/2` over `3π/2` look like one glyph | The two slashes join | `\Ia`. `check_scripts.py` flags powers and roots in limits; slashes in both limits have to be found by eye or `grep` |
| A one-phrase edit made the stamp overlap the text | The paragraph's last line was full, so the edit added a line | Run `solid_stats.py` after every edit, however small |

## Reading and proofing

| Symptom | Cause | Fix |
|---|---|---|
| Lesson examples have no solutions | The lesson PDFs are guided notes with blanks | Solve them yourself. Worked solutions were in the two HTML lessons and the quiz |
| Quiz text comes out shuffled | Knewton prints math in fragments | Crop the content column: `pdftoppm -r 200 -x 520 -W 680` in two halves per page |
| HTML lesson is 1.4 MB and unreadable | Inlined fonts, KaTeX and three.js | Strip `script`, `style` and `svg`; the math is plain `\( \)` LaTeX in the body |
| Words look misspelled in a per-column text dump ("verything") | `pdftotext -x -W` clips the first glyph at the crop edge | Trust the tiles for spelling, the dump for wording |
| The letter sheet seemed to show card text outside the crop marks | Misread an 80 DPI preview of very dense type | Check positions with `pdftotext -bbox`, not by eye |
| A scripted edit left the file half changed | It did not: every replacement asserted its anchor count, and the file was written only at the end | Keep doing that |
| `git push` and `gh pr create` to this repo were refused | On 2026-11-16 the session's permission check blocked them as outside communication the user had not asked for | Ask the user before pushing. Until they answer, commit on a branch and leave a `git bundle` in their notecard folder, since the scratchpad clone does not survive |
