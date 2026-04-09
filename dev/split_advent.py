#!/usr/bin/env python3
"""Split advent.dat into one file per section with descriptive names."""

import os

SECTION_NAMES = {
    0:  '0 - preamble',
    1:  '1 - long room descriptions',
    2:  '2 - short room descriptions',
    3:  '3 - travel table (exits)',
    4:  '4 - vocabulary',
    5:  '5 - object descriptions',
    6:  '6 - game messages',
    7:  '7 - object locations',
    8:  '8 - action defaults',
    9:  '9 - conditions',
    10: '10 - score rankings',
    11: '11 - hints',
    12: '12 - wizard messages',
}

src = os.path.join(os.path.dirname(__file__), 'advent_data', 'advent.dat')
out = os.path.join(os.path.dirname(__file__), 'advent_data')

with open(src) as f:
    lines = f.readlines()

sections = {}
current = None
buf = []

for line in lines:
    stripped = line.strip()
    if stripped == '-1' or stripped.startswith('-1\t'):
        if current is not None:
            sections[current] = buf
        current = None
        buf = []
    elif stripped.isdigit() and current is None:
        current = int(stripped)
        buf = []
    else:
        if current is not None:
            buf.append(line)

if current is not None:
    sections[current] = buf

for num, content in sorted(sections.items()):
    name = SECTION_NAMES.get(num, f'{num} - unknown')
    path = os.path.join(out, f'{name}.txt')
    with open(path, 'w') as f:
        f.writelines(content)
    print(f'  {name}.txt  ({len(content)} lines)')
