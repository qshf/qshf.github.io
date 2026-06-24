#!/usr/bin/env python3
"""Make multi-line $$...$$ display-math blocks survive Hugo's goldmark.

PROBLEM
-------
Hugo parses the *interior* of a `$$...$$` block as Markdown unless the whole
block is recognised cleanly as a passthrough. Several common LaTeX line shapes
break that recognition and split the block:

  * a lone `=` or `-` line  -> parsed as a setext heading underline
  * a line starting with `- `, `+ `, `* ` -> parsed as a list item
  * blank lines inside the block          -> paragraph break

When the block splits, the formula never reaches KaTeX and shows as raw text
(and inner `\\` row separators get eaten as Markdown escapes).

FIX
---
Collapse every multi-line `$$...$$` block into a single line:

    $$
    A
    = B
    $$            ->      $$ A = B $$

A single-line `$$...$$` is always recognised as inline passthrough, so none of
the Markdown line rules apply. Joining interior lines with a space is
mathematically identical: LaTeX treats a newline as whitespace, and explicit
`\\` row separators are preserved verbatim as text.

SAFETY
------
* Only the region strictly between the opening and closing `$$` fences is
  touched. Prose (including `---` dividers) outside math is never modified.
* Blocks already on a single line are left unchanged.
* Verified there are no unescaped `%` LaTeX comments inside any block (those
  would swallow the rest of a joined line); if one is ever introduced this
  script will report it and skip that block.
"""
import re
import sys
import glob

LEADING_FENCE = re.compile(r'^[ \t]*\$\$')
TRAILING_FENCE = re.compile(r'\$\$[ \t]*$')
UNESCAPED_PCT = re.compile(r'(?<!\\)%')


def collapse_blocks(text):
    lines = text.split('\n')
    out = []
    i = 0
    n = len(lines)
    changed = 0
    skipped_pct = 0

    while i < n:
        line = lines[i]
        s = line.strip()

        # complete single-line block: leave as is
        if s.startswith('$$') and s.endswith('$$') and len(s) >= 4:
            out.append(line)
            i += 1
            continue

        # opening fence of a multi-line block
        if LEADING_FENCE.match(line) and not TRAILING_FENCE.search(s[2:] if len(s) > 2 else ''):
            # gather until the closing fence
            indent = line[:len(line) - len(line.lstrip())]
            first_rest = line.strip()[2:].strip()  # text after opening $$ on same line
            body = []
            if first_rest:
                body.append(first_rest)
            j = i + 1
            closed = False
            while j < n:
                cur = lines[j].strip()
                if TRAILING_FENCE.search(cur):
                    before = cur[:cur.rfind('$$')].strip()
                    if before:
                        body.append(before)
                    closed = True
                    break
                body.append(cur)
                j += 1

            if not closed:
                # unbalanced; emit unchanged to avoid corruption
                out.append(line)
                i += 1
                continue

            joined_body = ' '.join(b for b in body if b != '')

            if UNESCAPED_PCT.search(joined_body):
                # a % comment would eat the rest of the joined line; skip safely
                skipped_pct += 1
                for k in range(i, j + 1):
                    out.append(lines[k])
                i = j + 1
                continue

            out.append(f'{indent}$$ {joined_body} $$')
            if j > i:  # actually spanned multiple lines
                changed += 1
            i = j + 1
            continue

        out.append(line)
        i += 1

    return '\n'.join(out), changed, skipped_pct


def main():
    files = sorted(glob.glob('content/**/*.md', recursive=True))
    dry = '--apply' not in sys.argv
    total = 0
    touched = 0
    pct = 0
    for f in files:
        src = open(f, encoding='utf-8').read()
        new, n, sp = collapse_blocks(src)
        pct += sp
        if n:
            total += n
            touched += 1
            print(f"{'[dry]' if dry else '[fix]'} {f}: {n} blocks collapsed"
                  + (f" ({sp} skipped: % comment)" if sp else ""))
            if not dry:
                open(f, 'w', encoding='utf-8').write(new)
    print(f"\n{'Would collapse' if dry else 'Collapsed'} {total} blocks in {touched} files."
          + (f" {pct} blocks skipped due to % comments." if pct else ""))
    if dry:
        print("Re-run with --apply to write changes.")


if __name__ == '__main__':
    main()
