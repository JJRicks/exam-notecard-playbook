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
