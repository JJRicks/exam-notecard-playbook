"""Report type sizes and column fill for a 6x5 notecard PDF.

Blank is the space between a column's last text and the bottom margin, in PDF
points. Values near zero (even slightly negative) mean the column is full. The
figure for column 4 ignores the STAMP HERE block, so it is the height available
to \stampheight. A real blank in columns 1-3 is stranded space: a header pushed
to the next column by \needspace.

Usage: python3 card_stats.py card.pdf [--columns]
"""
import collections
import re
import subprocess
import sys
import zlib

MARGIN_PT = 0.06 * 72
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


def column_report(path):
    bbox = subprocess.run(['pdftotext', '-f', '1', '-l', '1', '-bbox', path, '-'],
                          capture_output=True, text=True, check=True).stdout
    page = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', bbox)
    width, height = float(page.group(1)), float(page.group(2))
    columns = collections.defaultdict(list)
    pattern = r'xMin="([\d.]+)" yMin="[\d.]+" xMax="[\d.]+" yMax="([\d.]+)">(.*?)</word>'
    for x, y, word in re.findall(pattern, bbox):
        if word not in IGNORE:
            columns[min(int(float(x) / (width / COLUMNS)), COLUMNS - 1)].append(float(y))
    bottom = height - MARGIN_PT
    report = []
    for c in range(COLUMNS):
        blank = bottom - max(columns[c]) if columns[c] else bottom
        report.append(f'column {c + 1}: blank {blank:5.1f} pt')
    return report


if __name__ == '__main__':
    pdf = sys.argv[1]
    if '--columns' not in sys.argv:
        print('font id, size, uses:')
        for (font, size), n in font_sizes(pdf).most_common(10):
            print(f'  F{font}  {size} pt  {n}')
    print('\n'.join(column_report(pdf)))
