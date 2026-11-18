#!/bin/bash
# Crop a zero-margin 6x5 notecard into per-column tiles for proofing. Needs only poppler.
# 700 DPI and 5 rows gives 20 tiles in which 3.3 pt type is comfortable to read.
# Usage: solid_tiles.sh card.pdf outdir [dpi] [rows]
set -euo pipefail
pdf=$1
out=$2
dpi=${3:-700}
rows=${4:-5}
mkdir -p "$out"
rm -f "$out"/c*_r*.png
colw=$((dpi * 108 / 72))        # one column (106.8 pt) plus its gap
height=$((dpi * 5 / rows))
overlap=$((dpi * 5 / 72))       # about a line and a half, so no line is lost at a tile edge
for c in 0 1 2 3; do
  x=$((dpi * 108 * c / 72))
  for ((r = 0; r < rows; r++)); do
    y=$((r * height))
    [ "$r" -gt 0 ] && y=$((y - overlap))
    pdftoppm -r "$dpi" -png -singlefile -x "$x" -y "$y" -W "$((colw + dpi * 2 / 72))" \
      -H "$((height + overlap))" "$pdf" "$out/c$((c + 1))_r$((r + 1))"
  done
done
ls "$out" | wc -l | xargs echo "tiles written:"
