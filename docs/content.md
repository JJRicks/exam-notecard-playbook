# Content

## What the user asked for

- Highest comprehensible information density. "You can go extremely small", "almost gnat sized".
- Organized by high-level topic, then problem type or objective, then the relevant equations.
- Every problem type seen must be covered.
- For each equation: what it does, how to use it, and what every variable means. It's a memory jogger, not a textbook, so skip basic algebra.
- Crash courses for everything needed by hand: derivative and integral rules missing from the sheet, dot and cross product, coordinate conversion.
- Referring to the equation sheet is fine, provided the card says exactly where to look, what the equation does, and how to use it.
- Comprehensiveness first. The user trims later if needed, and the Unit 2 card needed no trimming.

## Structure

One black `\hd` bar per lesson, in lesson order, with the legend first and the by-hand toolkit last. The text simply flows through the four columns, so a lesson can span the fold. Unit 2 ran L10 to L14 on the front and L14 to L18 plus the toolkit on the back.

Each problem type is one dense paragraph:

```latex
\pt{Unit tangent} $\vb T(t)=\vb r'(t)/\nm{\vb r'(t)}$ \sh{5R3}: unit (length 1) vector in the
direction of motion. \how $\vb r'$ \then\ (plug in $t_0$ if given) \then\ ... Needs $\vb r'\ne\vb0$.
\ex $\vb r=-2t\vb i+t\vb j$, $t=3$: $\vb r'=\ip{-2,1}$, ... $\vb T=\ip{-2\rt5/5,\rt5/5}$.
```

That is label, formula, sheet tag, meaning, steps, conditions, then a worked example with its answer.

| Marker | Use |
|---|---|
| `\pt` ▸ | Problem type |
| `\how` | Steps |
| `\ex` | Worked example with answer. Label real ones, such as `(Quiz 4)` |
| `\warn` ⚠ | Pitfall. Put the user's own past misses here |
| `\shc` ★ | Shortcut or extra beyond the lessons |
| `\sh` | Gray equation-sheet tag |

## Sheet tags

`5R6` means page 5, right column, 6th formula down. Write short formulas inline with the tag, because seeing the formula confirms the lookup. Use the tag alone for long ones, like the conversion rows. The legend at the top of the card explains the scheme.

Name a formula's parameters on the card even when the sheet has the formula. Saying what each symbol means, and when to pick which form, is what the sheet doesn't give. The four curvature forms are the model: each entry says which situation it fits.

## What earned its space

- **Decision procedures** over lists. "Count the minus signs" identifies a quadric faster than a table of shapes.
- **Worked examples from the real quizzes and lessons**, because they show the exact format.
- **Past misses.** Quiz 3 lost points for changing θ = −π/2 to 3π/2, and for typing `3i` into a coefficient box. Both are on the card.
- **Things missing from the sheet**: `∫tan`, `∫sec`, product, quotient and chain rules, θ quadrant fixes, completing the square.
- **Block-solving tricks.** Solve `s = 7e^(2t) − 7` for `e^(2t)`, not for `t`.
- **Avoiding hard steps by hand.** Find `a_N` from the root form to skip a cross product. Plug in `t` before crossing, so the vectors are numbers.

## Mining sources

For each lesson, capture every numbered example, the objectives list, and the practice problems. For each quiz, capture the question type, the required answer format, and anything the user got wrong.

Extra problem types the lessons skipped are worth adding as ★ once the core is in. Unit 2 added line segments, curves of intersection, osculating and normal plane equations, contour families, implicit partials, estimating partials from a table, horizontal tangent planes, 3-variable linearization, and differential error.

## Scope and source errors

Check everything against the exam's lesson range. The ChatGPT compilation covered Lessons 19 to 21, which were out of scope for Exam 2 and were left out.

Sources contain errors, so verify before copying:

- A screenshot in the collage said φ is measured from the y-axis. It is the z-axis.
- The sheet's projectile bullet labels position `x(t)`, and its "x₀" in the j part is the launch height. The card warns about this.
- The Lesson 16 practice answer for a level curve appeared to have a sign different from the correct `y = −x − π/14 + 2kπ/7`. The PDF text extraction was ambiguous, so this is unconfirmed. The card uses the derived answer.
- Lesson 11 uses φ = 5π/4, outside the 0 to π range. The formulas still work.

## Reuse

The `BY-HAND TOOLKIT` section in `template/notecard.tex` is reusable as written: derivative and integral rules, vector arithmetic, algebra and trig, and answer checks. Its Unit 2 tags for pages 3 and 4 still apply. Trim whatever a later unit doesn't need.

## Unit 3 (Exam 3, Lessons 19 to 27, 2026-11-16)

### What the user asked for this time

- "We can get even more information density." Smaller type, no line spacing, no gap at the fold, no margins. See [typesetting.md](typesetting.md), "Solid layout".
- Push the sheet-tag trick further: "if a formula appears on the allowed equation sheet it can be referenced with the sheet tags instead."
- Top priority, in their order: every topic explained; every equation explained in plain language, with what it means; every variable in every equation explained; then clear worked examples "including common shortcuts and how to use them (super duper bonus for shortcuts)".
- Problems are done by hand, so any derivative or integral rule that is needed but missing from the sheet goes in the by-hand toolkit, explained.
- "A little bit of extra care and attention towards u substitution and implicit differentiation, those still confuse me sometimes."
- Mid-build, on exponents: "where spacing gets weird with exponents im okay with parentheses and ^ instead", then "but its your call".

### How that changed the entries

A tag now replaces the formula. An entry for a sheet formula gives the tag, a name, what it does in plain words, every letter the sheet prints, the steps, then examples. The formula itself is not typed out unless it is a few symbols long and the explanation needs it (`dy/dx = −F_x/F_y`). Compare the two cards' Lagrange entries: Unit 3 says what the objective, the constraint and λ are, and never prints `∇f = λ∇g` in display form.

```latex
\pt{Type I} \sh{7M2} (vertical strips, $dy\,dx$): the region lies between the vertical lines
$x=a$ and $x=b$ (numbers); $g_1(x)$ = bottom curve, $g_2(x)$ = top curve = the inner limits.
```

Where the sheet's own lettering is odd, the card says so: 7M6 uses `f` as a limit, 7M8 has `g(x,y,z)` on one side and `f(r,θ,z)` on the other, and 7M11 is printed in the order dφ dρ dθ.

Counts on the shipped card: 46 problem-type entries, 106 worked examples, 33 ★ shortcuts, 15 ⚠ pitfalls, every one of the 30 Unit 3 sheet formulas tagged at least once, 40,736 characters.

### The two weak spots

Each got a long entry instead of a line in the toolkit.

- **Implicit differentiation** (in L19): the formula way and the Calc 1 way side by side on the same equation, the four traps (minus sign, which letter goes on the bottom, nonzero bottom, constants on the right vanish), a mixed product-rule term, a slope at a point, and the `z(x,y)` version.
- **u-substitution** (in the toolkit): when it applies, five steps, the missing-constant rule, converting limits versus substituting back, a leftover `x` (`u = 1 − x` so `x = 1 − u`), the linear-inside shortcut, guess-and-check, when it cannot work, and the difference between a nickname (`a = 1 − x` inside a `y`-integral) and a real substitution. That last point came from the user's own study notes.

### Sources for this unit, and what each was good for

| Source | Use |
|---|---|
| Lessons 19 to 27 (PDF) | Scope and every problem statement. They are guided notes: the examples are blank |
| Quiz 5 with explanations | Real question formats for L19 to L22. Scored 11/11, so no misses to record |
| Two HTML lessons (AI-written, interactive) | Worked solutions for L22 to L27. Every answer re-derived before use |
| "Notecard Gold" PDF (AI summary of the user's study sessions) | The user's own homework problems and the shortcuts that had clicked: zero branches in Lagrange, centroid averages, `abc/6`, enter and exit rays, the nickname point |
| Equation sheet | Tags. Read as images |

No quiz covered L23 to L27, so those sections lean on the lesson examples and the Gold problems.

### Source errors found

- Lesson 19, practice 2: the printed key has `−4x` in both denominators where `∂/∂z(−2z²) = −4z` belongs, and `4y³z³ − 10y` in the `∂z/∂y` numerator where `−4y³z³ − 10y` belongs. Confirmed on the rendered page. The card gives the derived answers.
- Lesson 27 says θ = α "makes a constant angle α with the xy-plane". It is a vertical half-plane. One HTML lesson had already caught this.
- Lesson 26 prints the box as `[a,b] × [c,e] × [e,f]`. The middle interval is `[c,d]`.

### Shortcuts worth reusing in Unit 4 and the final

Linear `f` on a circle: `±R√(a²+b²)`. Tetrahedron under a plane: `abc/6`. Linear function over a triangle: its value at the centroid. Product integrand with number limits: multiply single integrals. Corner tetrahedron: `∭ x^p y^q z^s = p! q! s! / (p+q+s+3)!`. One rose petal: `πa²/(4n)`. Integrand without `z`: multiply by the stick length.
