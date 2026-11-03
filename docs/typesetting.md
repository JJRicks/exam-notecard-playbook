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

## Untested: Units 3 and 4

Iterated integrals with limits like `\int_{g_1(x)}^{g_2(x)}` will stand taller and wider than anything on the Unit 2 card. Try a few early and check for collisions before committing to a style.
