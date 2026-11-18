# Typesetting

All settings below are live in `template/notecard.tex`. This file explains why they are what they are.

## Units

TeX `pt` is 1/72.27 in, and PDF `pt` is 1/72 in, so `\fontsize{3.55}` lands in the PDF as 3.537. Measurements here are PDF points read from the `Tf` operators with `tools/card_stats.py`. Don't infer sizes from `pdftotext -bbox` heights, which come from font ascent and descent rather than type size or ink.

## Geometry

| Item | Value |
|---|---|
| Page | 6 × 5 in (432 × 360 pt) |
| Margins | 0.06 in all round |
| Columns | 4, each 1.38 in wide, separated by 0.12 in |
| Column height | 4.88 in |
| Gap centers | 1.5, 3.0, 4.5 in |

The center gap straddles the cut line, so each face keeps a 0.06 in margin after cutting. Rules are drawn with `eso-pic` instead of `\columnseprule` so the center one can be dashed. A faint box 0.01 in inside the page edge marks the trim.

Use `multicols*`, not `multicols`. It fills columns in order instead of balancing them, which is what puts spare space at the bottom of column 4.

## Type against the Unit 1 card

| | Unit 1 | Unit 2 |
|---|---|---|
| Body font | DejaVu Sans Condensed | Bell Centennial Std Address |
| Body size | 3.92 | 3.54 |
| Baseline spacing | 4.0 | 3.76 |
| x-height | about 2.14 | 1.72 |
| Math font | DejaVu Math TeX Gyre, 3.37 | Fira Math, 3.25 |
| Main script size | 2.69 | 2.28 |
| Extractable characters | about 16,100 | about 25,400 |

Unit 2 has about 80% of Unit 1's x-height and about 1.6 times its text. Bell's narrowness supplies most of that gain.

In print, the user said the Unit 2 text "was great" and that there was room to spare, so these sizes aren't the limit. Capacity scales with the inverse square of body size, so a 3.2 pt body should hold about 23% more. That figure is calculated, not tested.

## Bell Centennial

Only the Address weight is available, so bold and italic are synthesized with `AutoFakeBold=1.8` and `AutoFakeSlant=0.18`. Both looked fine at this size.

- Metrics: 1000 units per em, x-height 485, cap height 653, average lowercase advance 0.40 em.
- Has: `∂ √ ∫ × · ≤ ≥ ≠ ∞ ± − ² ³ π μ ∑ ° • ≈ … – —`
- Lacks: Greek except π and μ, `‖ ⟨ ⟩ → ⇒ ↔ ′ ″ ∈ ℝ ▸ ✓ ∥ ⊥`. Use math mode for these. `▸ ⚠ ★` come from DejaVu Sans through `\symf`.
- Its `½` and `¼` glyphs look wrong. Write `(1/2)`.

## Math font comparison

Swatches were set at 3.6 pt and viewed at 1200 DPI.

| Font | Bundle file | Verdict |
|---|---|---|
| Fira Math | `FiraMath-Regular.otf` | Chosen: sans, sturdy, compact, has bold, matches Bell |
| DejaVu Math TeX Gyre | `texgyredejavu-math.otf` | Too wide |
| STIX Two Math | `STIXTwoMath-Regular.otf` | Legible, but serif and wider than Fira |
| Latin Modern Math | `latinmodern-math.otf` | Hairlines too thin |

`LeteSansMath.otf` and `NewCMSansMath-Regular.otf` aren't in the Tectonic bundle. `Scale=0.92` matches Fira's x-height to Bell's.

## Math style

- **Fractions:** slashes, with parentheses as needed: `x^2/a^2`, `(v_0\sin\theta)^2/(2g)`, `(1/2)gt^2`. Stacked fractions shrink numerators to about 2.2 pt and collide with neighboring lines.
- **Roots:** prefix `\rt`, with parentheses unless the radicand is a single plain atom: `\rt2`, `\rt t`, `\rt(x^2+y^2)`, `\rt(t^2)`. A vinculum reaches the line above and reads as an underline.
- **Vectors:** `\vb r`, which is `\symbf`. `\mathbf` isn't visibly bold under `unicode-math`.
- **Parenthesize** function arguments and any numerator containing a function: `\tan^{-1}(y/x)`, `(\sin u)/u`.
- **Text-mode arrows:** always `\then`, which wraps `\ensuremath`.

## Spacing

| Setting | Value | Why |
|---|---|---|
| Baseline ratio | 1.063 | Looser than Unit 1's 1.02, which the user read easily |
| `\lineskiplimit` | `-0.5pt` | Superscripts don't push lines apart. At `-0.9pt` with stacked fractions, lines collided |
| `\thickmuskip` and friends | 3, 2, 2 mu | Tighter than TeX's defaults for density |
| `\tolerance`, `\emergencystretch` | 3000, 0.8em | Keeps narrow justified columns free of overfull lines (zero on the final card) |
| `\needspace` before headers | 4 lines | 5 stranded too many lines at column bottoms |

## Macros

| Macro | Output |
|---|---|
| `\hd{...}` | Black header bar, white bold text |
| `\pt{...}` | Bold ▸ problem-type label |
| `\sh{5R6}` | Gray tag. Separate neighbors with `\,` |
| `\ex`, `\how`, `\warn`, `\shc` | *Ex*, **How:**, ⚠, ★ |
| `\vb`, `\nm`, `\ip` | Bold vector, norm, angle brackets |
| `\rt`, `\then` | Prefix radical, text-safe ⇒ |

Sheet tags use 22% gray with bold text. Outlined, inverted, and bracketed tags were tried. Gray was distinct without being heavy.

## STAMP HERE

The block sits in the flow at the end of the card, and `\vfill` pushes it to the bottom of column 4.

- **Face:** Helvetica 95 Black, which embeds as `HelveticaNeue-Black`. Fake-bold Bell was narrower and weaker.
- **Layout:** two lines. The 1.38 × 0.42 in space favors stacking, which gives larger letters than one line.
- **Size:** `\resizebox{!}{\stampheight}{...}`, scaled to fill. Set `\stampheight` from `card_stats.py`.
- **Hollow letters:** a fake-bold font renders with fill and stroke, so setting a white fill and black stroke leaves an outline. The stamp's ink then shows through:

```latex
\special{pdf:bc [1] [0]} ...text in the FakeBold font... \special{pdf:ec}
```

`FakeBold` sets the outline weight. 1.5 was too light, 4 closed up the counters in A and P, and 2.5 shipped. Change `[1]` to `[0.85]` for a light gray fill.

## Letter sheet

`template/letter-sheet.tex` places the card PDF at 1.25 in, 3 in from the page's lower-left corner, which centers it. Around it are corner crop marks, fold marks, a print-setting caption, and a 1-inch scale bar. It embeds the built card, so build the card first.

## Iterated integrals

Settled on the Unit 3 card: see "Integrals" under the solid layout below. Limits like `\int_{g_1(x)}^{g_2(x)}` did need their own macros. Unit 4's line and surface integrals are still untested.

## Solid layout (Unit 3 onward)

Everything above describes the Unit 2 card. After seeing it in print the user asked for more: smaller type, lines "SMOOSHED up against each other, no spacing, no page split spacing, and absolutely no margins. Every available square millimeter should be used." `template/notecard-solid.tex` is that layout, as shipped for Unit 3 on 2026-11-16. The figures here are measured from that card.

### Geometry

| Item | Unit 2 | Unit 3 (solid) |
|---|---|---|
| Margins | 0.06 in all round | 0 top and bottom, 0.3 pt left and right |
| Column gap | 0.12 in (8.64 pt) | 1.4 pt, with a solid black 0.2 pt rule down its middle |
| Column width | 99.4 pt | 106.8 pt |
| Center line | dashed, in a 0.12 in gap | solid black 0.35 pt rule in the same 1.4 pt gap |
| Trim box | faint frame 0.01 in inside the edge | none: the text itself reaches the edge |
| Body | 3.55 pt (3.537 PDF) | 3.3 pt (3.288 PDF) |
| Line pitch | 3.774 pt, ratio 1.063 | 3.129 pt, ratio 0.948 |
| Lines per column | about 93 | 115 exactly |
| Math, scripts | 3.25, 2.28 PDF pt | 3.02, 2.25 PDF pt |
| Characters (pdftotext, with spaces) | 25,367 | 40,736 |

The side inset of 0.3 pt only keeps edge glyphs inside the page box. The card is cut from the letter sheet, so text at the trim edge prints fine. What is at risk is the cut: the first line's ascenders are 0.2 pt inside the top edge. If a printed card comes back clipped, `\edgemargin` insets all four sides. It is 0 pt as shipped, and 1 pt costs about five lines of text, so re-fit after changing it.

The rules are solid black. A 55% gray hairline was tried first and dropped on reasoning, not on a test print: gray has to be halftoned, and a halftoned 0.2 pt line can break into dots. A dashed center line was also dropped, because on screen a dash 0.5 pt from the end of a line of text read as `|` or `1`.

### The line grid

Nothing on the page stretches or shrinks. `\parskip` is 0, `\lineskiplimit` is `-\maxdimen` so no line is ever pushed away from its neighbour, and every header is exactly one line slot tall. A column therefore holds a whole number of lines, and two knobs set everything:

```latex
\newcommand\bodysize{3.3}   % pt
\newcommand\nlines{115}     % lines per column;  pitch = (360pt - 1em) / (nlines - 1)
```

The first baseline sits 0.78 em below the top edge (`\topskip`) and the last 0.22 em above the bottom edge. `multicols*` rounds the column height to `\topskip` plus a whole number of baselines, which is why the fit is exact.

Measured fit for the final Unit 3 text, from `tools/solid_fit.sh`. The stamp needs 9 lines free in column 4:

| Size : lines | Pitch | Ratio | Column 4 free |
|---|---|---|---|
| 3.3 : 114 | 3.157 | 0.957 | 5.3 lines (stamp overlaps text) |
| 3.3 : 115 | 3.129 | 0.948 | 9.3 lines (shipped) |
| 3.35 : 115 | 3.129 | 0.934 | 0.3 lines (stamp overlaps text) |
| 3.25 : 115 | 3.129 | 0.963 | 14.3 lines |

One more line per column is worth four lines of text, about 350 characters. 0.05 pt of body size is worth about nine lines.

Because nothing can shrink, an overfull last column does not start a second page: the stamp is simply set on top of the last lines of text, or pushed off the bottom edge. Check column 4 with `solid_stats.py` after every edit.

### Why the pitch is 0.95 em

Glyph extents, as fractions of the body size (XeTeX box measurements at 10 pt):

| Glyph | Height | Depth |
|---|---|---|
| Bell x-height | 0.486 | 0 |
| Bell ascenders b d h l, digits | 0.68 | 0.015 |
| Bell f | 0.695 | 0 |
| Bell descenders g p q y | 0.50 | 0.153 |
| Bell ( ) | 0.668 | 0.163 |
| Bell [ ] | 0.721 | 0.202 |
| Fira ( at 0.92 | 0.713 | 0.198 |
| Fira ∫ at 0.92 | 0.741 | 0.225 |
| Native superscript, `x^2` | 0.85 | 0 |
| Native subscript, `x_0` | 0.48 | 0.33 |
| Native subscript with a descender, `f_{xy}` | 0.69 | 0.47 |
| Nested superscript, `e^{t^2}` | 1.07 | 0 |

Plain text spans about 0.92 em from the bottom of a bracket to the top of one, so a pitch of 0.95 em sets the lines touching with no gap and no overlap. Native math does not fit: a subscript above a superscript would overlap by 0.2 em wherever they line up, and on a card with hundreds of `f_x` and `x^2` that happens constantly.

### Scripts that stay in the line

XeTeX takes script positions straight from the font's MATH table, so `\fontdimen` changes do nothing. The template keeps TeX's own attachment (so spacing, italic correction and `\sin^2` all behave) but wraps each script in a smashed box that is moved back toward the line:

```latex
\newcommand\supx[1]{\sp{\smash{\lower0.085em\hbox{$\scriptstyle#1$}}}}   % top lands at 0.76 em
\newcommand\subx[1]{\sb{\smash{\raise0.20em\hbox{$\scriptstyle#1$}}}}    % baseline 0.12 em down
```

In the body `^` and `_` are made active and mapped to these. Three consequences:

- **One script per base.** `x_0^2` puts both at the single-script positions and they overprint. Stacked pairs go through `\I{a}{b}` (integral limits) or `[F]\ev{a}{b}` (evaluation), which use a wider pair of offsets (`\supy`, `\suby`: 0.02 em and 0.10 em). For anything else write `(x_0)^2`.
- **No script inside a script.** The inner box does not shrink, so it collides. Use the caret macro: `e\cx(9t^{9/4}+8)` prints as e^(9t^(9/4)+8) with the 9/4 raised once. The user offered this ("where spacing gets weird with exponents im okay with parentheses and ^ instead", then "but its your call"). One-level exponents stay raised because they are narrower.
- **Primes** are mapped to a raised, smashed `\prime` box (`\pr`), so `f'` and `y''` work and never trigger "Double superscript".

Scripts are declared at 0.745 of the body (`\DeclareMathSizes`), not TeX's 0.7, which holds them at 2.25 PDF pt, the same absolute size as on the Unit 2 card. Integral limits are scripts, and they are the content the unit is about.

`tools/check_scripts.py` finds stacked scripts, scripts inside limits, and nested scripts. None of them raises a TeX error.

### Integrals

| Macro | Prints | Use |
|---|---|---|
| `\I{a}{b}` | ∫ with stacked limits | Limits without powers: numbers, `\pi/2`, `1-x-y`, `r\cos\theta+2` |
| `\Ia{a}{b}` | ∫[a→b] at full size | Any limit containing a power or a root, and any pair where both limits contain a slash: `\Ia{y^2-3}{y+3}`, `\Ia{0}{\rt(4-x^2)}`, `\Ia{\pi/2}{3\pi/2}` |
| `\J` | bare ∫ | Antiderivative rules |
| `\II{R}`, `\III{E}` | ∬, ∭ with a region subscript | |
| `[F]\ev{a}{b}` | evaluation limits | |

The integral sign is smashed, so limits sit at script positions instead of at the top and bottom of the tall glyph. The two stacked limits are 0.05 em apart, which is enough for `0` over `1-x` but not for two fractions (their slashes join into one stroke) or a radical (its tail reaches the lower limit). Tried and rejected: plain `\int_a^b` (limits spread 1.3 em and hit both neighbouring lines); scaling the sign to 80% (the limits then attach to the box and float); a power inside a stacked lower limit, by nesting, by caret, or with Unicode ² (each collides with the upper limit). The legend on the card explains the arrow form.

### Brackets

`\ip`, `\nm` and `\abs` smash their delimiters so tall bars do not matter, and wrap them in `\mathopen` and `\mathclose`. Without that the smashed delimiter is an ordinary atom, a leading minus becomes binary, and `⟨−7 ln(2y)⟩` prints with a gap after the bracket.

### Run-in structure

A paragraph break wastes half a line on average, and the Unit 2 card had about 80 of them. On the solid card only a lesson header starts a new line. `\hd` is a black label one slot tall at the start of that line, and the text continues on the same line. `\pt` is a bold ▸ label inside the running text. Write `\pt{Label} text` or `\pt{Label}: text`; the macro adds no space of its own.

### Stamp

Same hollow block as before, sized in lines: `\stamplines` (9 on Unit 3, giving a block 25 pt tall and 82 pt wide). Its height is `\stamplines` pitches minus 3.4 pt, with a 1 pt kern beneath so the outline clears the trim.

### Using the last line of every section

Each lesson section is one paragraph, so each ends in a part-filled line: ten of them on Unit 3, about 400 characters in all. Once the card fits, fill them with one short ★ or ⚠ each. `solid_stats.py` must show the same free lines in column 4 afterwards; if it drops by one, that addition was too long.

### Duplex sheet (optional)

With no gap at the fold, the fold or cut runs through a 1.4 pt gutter. `examples/unit3/Unit3_Notecard_Letter_Duplex.tex` is an alternative print sheet for that: two letter pages, each showing one half of the 6 × 5 card (`viewport=0 0 216 360` and `216 0 432 360`, clipped) at 100% and centered, so a double-sided print flipped on the long edge puts the back exactly behind the front. Nothing has to be folded. It was offered alongside the usual letter sheet, not instead of it, and has not been printed.

### Print result

The user printed the 3.3 pt solid card at 1200 DPI and called it "the perfect size", adding that a tad smaller "might be starting to push it". Treat 3.25 pt as the floor; see the README. A 1-bit render at 600 DPI made the 2.25 pt integral limits marginal, so print at 1200 DPI.

### Untested

- Whether a hand cut can hold the zero margin, and whether a fold in a 1.4 pt gutter stays readable.
- Unit 4 material: line integrals with `\oint`, and surface integrals with long vector integrands.
