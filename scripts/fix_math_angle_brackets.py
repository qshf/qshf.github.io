#!/usr/bin/env python3
"""Replace literal < / > inside math with \\lt / \\gt.

PROBLEM
-------
KaTeX runs in the browser *after* the HTML parser. A literal `<` inside a
formula (e.g. `w_{k+1} < w_k`) looks like the start of an HTML tag when the
`<` is immediately followed by a letter (`<w`), so the browser swallows it
and KaTeX never renders that formula.

FIX
---
Inside math spans only, replace raw `<` -> `\lt` and `>` -> `\gt`. These are
mathematically identical in KaTeX and are not mistaken for HTML tags.

SCOPE
-----
Operates on `$$...$$` display blocks and `$...$` inline spans. We verified the
content uses no `\langle`, `\left<`, or escaped `\<`, so every literal `<`/`>`
inside math is a comparison operator and the substitution is safe. Text
outside math (where `<`/`>` may be legitimate HTML or prose) is never touched.
"""
import re
import sys
import glob

# Match $$...$$ (non-greedy, single line after collapse) OR $...$ inline.
# Display first so it wins over inline.
MATH = re.compile(r'(\$\$.+?\$\$|(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$))', re.DOTALL)


def fix_math_span(span):
    # span includes the $ / $$ delimiters; only transform the interior.
    if span.startswith('$$'):
        open_d, close_d, body = '$$', '$$', span[2:-2]
    else:
        open_d, close_d, body = '$', '$', span[1:-1]
    new = body.replace('<', r'\lt ').replace('>', r'\gt ')
    return open_d + new + close_d, (new != body)


def fix_text(text):
    count = 0

    def repl(m):
        nonlocal count
        new, changed = fix_math_span(m.group(0))
        if changed:
            count += 1
        return new

    return MATH.sub(repl, text), count


def main():
    files = sorted(glob.glob('content/**/*.md', recursive=True))
    dry = '--apply' not in sys.argv
    total = 0
    touched = 0
    for f in files:
        src = open(f, encoding='utf-8').read()
        new, n = fix_text(src)
        if n:
            total += n
            touched += 1
            print(f"{'[dry]' if dry else '[fix]'} {f}: {n} math spans")
            if not dry:
                open(f, 'w', encoding='utf-8').write(new)
    print(f"\n{'Would fix' if dry else 'Fixed'} {total} math spans in {touched} files.")
    if dry:
        print("Re-run with --apply to write changes.")


if __name__ == '__main__':
    main()
