#!/bin/bash
# Compile a solid-layout notecard at several (body size, lines per column) pairs and report the fit.
# The line pitch follows from the pair: pitch = (360pt - size) / (lines - 1).
# Usage: solid_fit.sh card.tex 3.3:113 3.3:114 3.25:115
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1
shift
dir=$(dirname "$src")
name=$(basename "$src")
out=$(mktemp -d)
trap 'rm -rf "$out" "$dir/_fit_size.tex"' EXIT
for pair in "$@"; do
  size=${pair%%:*}
  lines=${pair##*:}
  pitch=$(awk -v s="$size" -v n="$lines" 'BEGIN { printf "%.4f", (360 - s) / (n - 1) }')
  sed -E "s/^(.newcommand.bodysize\{)[0-9.]+/\1$size/; s/^(.newcommand.nlines\{)[0-9]+/\1$lines/" \
    "$dir/$name" > "$dir/_fit_size.tex"
  (cd "$dir" && tectonic -X compile --keep-logs --outdir "$out" _fit_size.tex >/dev/null 2>&1) || {
    echo "size $size lines $lines: compile failed"
    continue
  }
  ratio=$(awk -v s="$size" -v p="$pitch" 'BEGIN { printf "%.3f", p / s }')
  echo "size $size, $lines lines, pitch $pitch (ratio $ratio), $(grep -c Overfull "$out/_fit_size.log" || true) overfull"
  python3 "$here/solid_stats.py" "$out/_fit_size.pdf" "--pitch=$pitch" --columns 2>&1 | grep -v blake2 | sed 's/^/  /'
done
