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
