"""Convert \frac and \sqrt in a notecard body to the forms that survive tiny type.

    \frac{A}{B}  ->  A/B, with parentheses where the meaning needs them
    \sqrt{X}     ->  \rt X or \rt(X)   (\rt is defined in template/notecard.tex)

Only for migrating content that already has them. New content should be
written this way from the start. Review the result by eye: spacing and a few
parentheses can still want a hand edit.

Usage: python3 defrac.py in.tex out.tex
"""
import re
import sys

ONE_ARG = {'\\vb', '\\nm', '\\ip', '\\sqrt', '\\rt', '\\symbf', '\\mathbf', '\\text', '\\textbf', '\\mathrm'}
FUNCS = ('\\sin', '\\cos', '\\tan', '\\sec', '\\csc', '\\cot', '\\ln', '\\log', '^{-1}')
OPS_AFTER = ('\\,', '\;', '\\ ', '\\quad', '\\cdot', '\\times', '\\pm', '\\mp', '\\to', '\\then',
             '\\le', '\\ge', '\\ne', '\\approx', '\\in', '\\Rightarrow', '\\iff', '\\parallel',
             '\\perp', '\\big', '\\Big', '\\rangle', '\\rVert', '\\right', '\\int', '\\Delta')


def read_arg(s, i):
    """Return (arg_text, next_index) for a TeX argument starting at s[i] (spaces skipped)."""
    while i < len(s) and s[i] == ' ':
        i += 1
    if s[i] == '{':
        depth, j = 0, i
        while True:
            if s[j] == '\\':
                j += 2
                continue
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
                if depth == 0:
                    return s[i + 1:j], j + 1
            j += 1
    if s[i] == '\\':
        m = re.match(r'\\([a-zA-Z]+|.)', s[i:])
        return m.group(0), i + len(m.group(0))
    return s[i], i + 1


def toplevel_has(t, ops, skip_leading_minus=True):
    depth, absd, i = 0, False, 0
    while i < len(t):
        c = t[i]
        if c == '\\':
            m = re.match(r'\\([a-zA-Z]+|.)', t[i:])
            cs = m.group(0)
            if depth == 0 and not absd and cs in ops:
                return True
            if cs in ('\\lVert', '\\langle'):
                depth += 1
            if cs in ('\\rVert', '\\rangle'):
                depth -= 1
            i += len(cs)
            continue
        if c in '{([':
            depth += 1
        elif c in '})]':
            depth -= 1
        elif c == '|':
            absd = not absd
        elif depth == 0 and not absd and c in ops:
            if not (skip_leading_minus and c == '-' and t[:i].strip() == ''):
                return True
        i += 1
    return False


def count_atoms(t):
    t = t.strip()
    n, i = 0, 0
    while i < len(t):
        c = t[i]
        if c == ' ':
            i += 1
            continue
        if c in '^_':
            _, i = read_arg(t, i + 1)
            continue
        if c == "'":
            i += 1
            continue
        if c == '\\':
            m = re.match(r'\\([a-zA-Z]+|.)', t[i:])
            cs = m.group(0)
            i += len(cs)
            if cs in ('\\,', '\;', '\\ '):
                continue
            if cs in ONE_ARG:
                _, i = read_arg(t, i)
            n += 1
            continue
        if c.isdigit() or c == '.':
            m = re.match(r'[0-9.]+', t[i:])
            i += len(m.group(0))
            n += 1
            continue
        if c in '([{|':
            close = {'(': ')', '[': ']', '{': '}', '|': '|'}[c]
            depth, j = 0, i
            while j < len(t):
                if t[j] == c and (c != '|' or j == i):
                    depth += 1
                elif t[j] == close:
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            i = j + 1
            n += 1
            continue
        i += 1
        n += 1
    return n


def wrap_num(a):
    if toplevel_has(a, ('+', '-', '\\pm', '\\mp', '\\cdot', '\\times')):
        return f'({a})'
    if re.search(r'\\(sin|cos|tan|sec|csc|cot|ln|log)(?![a-zA-Z])', a) and count_atoms(a) > 1:
        return f'({a})'
    return a


def wrap_den(b):
    bs = b.strip()
    if re.match(r'(d[a-zA-Z]|\\partial)', bs):
        return b
    if toplevel_has(bs, ('+', '-', '\\pm', '\\mp', '\\cdot', '\\times', '/'), False) or count_atoms(bs) > 1:
        return f'({b})'
    return b


def needs_outer(before, after):
    if before.endswith(FUNCS):
        return True
    a = after.lstrip(' ') if after.startswith(' ') and not after.lstrip(' ')[:1].isalpha() else after
    if not a:
        return False
    if a[0] == '\\':
        return not a.startswith(OPS_AFTER)
    return a[0].isalnum() or a[0] in '([{'


def convert_fracs(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\frac', i) and not s[i + 5:i + 6].isalpha():
            a, j = read_arg(s, i + 5)
            b, k = read_arg(s, j)
            out.append((convert_fracs(a), convert_fracs(b)))
            i = k
        else:
            out.append(s[i])
            i += 1
    res = ''
    for idx, tok in enumerate(out):
        if isinstance(tok, str):
            res += tok
            continue
        frac = f'{wrap_num(tok[0])}/{wrap_den(tok[1])}'
        after = ''.join(t if isinstance(t, str) else 'X' for t in out[idx + 1:idx + 12])
        if needs_outer(res.rstrip(), after):
            frac = f'({frac})'
        if re.search(r'\\[a-zA-Z]+$', res) and frac[0].isalpha():
            res += ' '
        res += frac
    return res


def convert_sqrts(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\sqrt', i) and not s[i + 5:i + 6].isalpha():
            x, j = read_arg(s, i + 5)
            x = convert_sqrts(x)
            xs = x.strip()
            if xs in ('\\', '\\ ', ''):
                out.append('\\rt')
            elif ('^' in xs or '_' in xs
                  or toplevel_has(xs, ('+', '-', '\\pm', '\\cdot', '\\times', '/'), False)
                  or count_atoms(xs) > 1):
                out.append(f'\\rt({x})')
            else:
                out.append('\\rt' + (' ' if xs[0].isalpha() else '') + xs)
            i = j
        else:
            out.append(s[i])
            i += 1
    return re.sub(r'\\rt(?=[a-zA-Z])', r'\\rt ', ''.join(out))


if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    start = src.find('\\begin{document}')
    head, body = src[:max(start, 0)], src[max(start, 0):]
    new_body = convert_sqrts(convert_fracs(body))
    open(sys.argv[2], 'w').write(head + new_body)
    print('fracs:', body.count('\\frac'), '->', new_body.count('\\frac'),
          ' sqrts:', body.count('\\sqrt'), '->', new_body.count('\\sqrt'))
