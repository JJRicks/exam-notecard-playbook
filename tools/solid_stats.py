"""Report type sizes and column fill for a zero-margin ("solid") 6x5 notecard PDF.

For each of the four columns it prints where the last text ends and how much room is left
above the bottom edge, in PDF points and in text lines. Columns 1 to 3 should show about a
third of a line (that is just the descender room below the last baseline). The figure for
column 4 ignores the STAMP HERE block: it must be at least \\stamplines, or the stamp will
sit on top of the last lines of text (nothing in this layout can shrink to make room).

Usage: python3 solid_stats.py card.pdf [--pitch=3.1289] [--columns]
"""
import collections
import re
import subprocess
import sys
import zlib

COLUMNS = 4
IGNORE = {'STAMP', 'HERE'}


def font_sizes(path):
    """Count Tf operators in the page streams: the real type sizes, not bbox heights."""
    data = open(path, 'rb').read()
    sizes = collections.Counter()
    for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
        try:
            stream = zlib.decompress(m.group(1))
        except zlib.error:
            continue
        for t in re.finditer(rb'/F(\d+)\s+([\d.]+)\s+Tf', stream):
            sizes[(t.group(1).decode(), t.group(2).decode())] += 1
    return sizes


def column_report(path, pitch):
    info = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    bbox = subprocess.run(['pdftotext', '-f', '1', '-l', '1', '-bbox', path, '-'],
                          capture_output=True, text=True, check=True).stdout
    page = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', bbox)
    width, height = float(page.group(1)), float(page.group(2))
    cols = collections.defaultdict(list)
    pattern = r'xMin="([\d.]+)" yMin="[\d.]+" xMax="[\d.]+" yMax="([\d.]+)">(.*?)</word>'
    for x, y, word in re.findall(pattern, bbox):
        if word not in IGNORE:
            cols[min(int(float(x) / (width / COLUMNS)), COLUMNS - 1)].append(float(y))
    text = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True).stdout
    out = [f'pages: {pages} (must be 1)',
           f'characters: {len(text)} with spaces, {len("".join(text.split()))} without',
           f'line pitch {pitch} pt, {round(height / pitch)} lines per column']
    for c in range(COLUMNS):
        if not cols[c]:
            out.append(f'column {c + 1}: empty')
            continue
        blank = height - max(cols[c])
        out.append(f'column {c + 1}: blank {blank:5.1f} pt = {blank / pitch:4.1f} lines')
    return out


if __name__ == '__main__':
    pdf = sys.argv[1]
    pitch = 3.1289
    for arg in sys.argv[2:]:
        if arg.startswith('--pitch='):
            pitch = float(arg.split('=')[1])
    if '--columns' not in sys.argv:
        print('font id, size, uses:')
        for (font, size), n in font_sizes(pdf).most_common(8):
            print(f'  F{font}  {size} pt  {n}')
    print('\n'.join(column_report(pdf, pitch)))
