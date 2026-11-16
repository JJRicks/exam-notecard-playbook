"""Check a solid-layout notecard source for script constructs that render badly.

In the solid layout ^ and _ are active and place one script inside the line slot. Three
things break that, and none of them raises a TeX error:

  stacked   x_0^2 on one base: the two scripts overprint. Use \\I, \\ev, or (x_0)^2.
  in limit  ^, _ or a radical inside \\I{..}{..}, \\ev, \\II, \\III: use \\Ia{..}{..}
            (limits written [a -> b]) when a limit contains a power or a root.
  nested    a script inside a script: write the exponent with the caret macro \\cx.

It also counts constructs the playbook bans (\\frac, \\sqrt, \\mathbf, straight quotes).

Usage: python3 check_scripts.py card.tex      (exit status 1 if anything is found)
"""
import re
import sys

src = open(sys.argv[1], encoding='utf-8').read()
body = src[src.index(r'\begin{multicols*}'):]
arg = r'(?:\{[^{}]*\}|\\[a-zA-Z]+|[^\\{}\s])'
found = []
for m in re.finditer('_' + arg + r'\^|\^' + arg + '_', body):
    found.append(('stacked', body[max(0, m.start() - 25):m.end() + 15]))
for m in re.finditer(r'\\(?:I|ev)\{([^{}]*)\}\{([^{}]*)\}', body):
    if re.search(r'[\^_]|\\rt', m.group(1) + m.group(2)):   # a radical in a stacked limit touches the other limit
        found.append(('in limit', m.group(0)))
for m in re.finditer(r'\\(?:II|III)\{([^{}]*)\}', body):
    if re.search(r'[\^_]', m.group(1)):
        found.append(('in limit', m.group(0)))
for m in re.finditer(r'[\^_]\{([^{}]*)\}', body):
    if re.search(r'[\^_]', m.group(1)):
        found.append(('nested', m.group(0)))
for kind, text in found:
    print(f'{kind:9} {text!r}')
banned = {r'\\frac': 0, r'\\sqrt': 0, r'\\mathbf': 0, '"': 0}
for pattern in banned:
    banned[pattern] = len(re.findall(pattern, body))
print('script problems:', len(found), ' banned constructs:', banned)
sys.exit(1 if found or any(banned.values()) else 0)
