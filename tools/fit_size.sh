#!/bin/bash
# Compile a notecard at several body sizes and report overflow and column fill.
# Fit is not monotonic, so try several sizes and read the blanks.
# Usage: fit_size.sh card.tex 3.50 3.55 3.60
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1
shift
dir=$(dirname "$src")
name=$(basename "$src")
ratio=1.063
out=$(mktemp -d)
trap 'rm -rf "$out" "$dir/_fit_size.tex"' EXIT
for size in "$@"; do
  lead=$(awk -v s="$size" -v r="$ratio" 'BEGIN { printf "%.3f", s * r }')
  sed -E "s/^(.newcommand.bodysize\{)[0-9.]+/\1$size/; s/^(.newcommand.bodylead\{)[0-9.]+/\1$lead/" \
    "$dir/$name" > "$dir/_fit_size.tex"
  (cd "$dir" && tectonic -X compile --keep-logs --outdir "$out" _fit_size.tex >/dev/null 2>&1) || {
    echo "size $size: compile failed"
    continue
  }
  pages=$(pdfinfo "$out/_fit_size.pdf" | awk '/Pages/ { print $2 }')
  over=0
  if [ "$pages" -gt 1 ]; then
    over=$(pdftotext -f 2 "$out/_fit_size.pdf" - | grep -c . || true)
  fi
  echo "size $size lead $lead: $pages page(s), about $over lines over, $(grep -c Overfull "$out/_fit_size.log" || true) overfull"
  python3 "$here/card_stats.py" "$out/_fit_size.pdf" --columns | sed 's/^/  /'
done
