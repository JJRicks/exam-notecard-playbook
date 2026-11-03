#!/bin/bash
# Crop a 6x5 notecard into per-column tiles for proofing. Needs only poppler.
# Usage: proof_tiles.sh card.pdf outdir [dpi] [rows]
set -euo pipefail
pdf=$1
out=$2
dpi=${3:-600}
rows=${4:-3}
mkdir -p "$out"
width=$((dpi * 144 / 100))   # column plus a little gutter
height=$((dpi * 5 / rows))
overlap=$((dpi / 50))
for c in 0 1 2 3; do
  x=$((dpi * (3 + 150 * c) / 100))
  for ((r = 0; r < rows; r++)); do
    pdftoppm -r "$dpi" -png -singlefile -x "$x" -y "$((r * height))" -W "$width" \
      -H "$((height + overlap))" "$pdf" "$out/c$((c + 1))_r$((r + 1))"
  done
done
ls "$out" | wc -l | xargs echo "tiles written:"
