#!/usr/bin/env python3
"""
Parse advent.dat (350-point Crowther & Woods) into rooms.csv and items.csv.
Source: https://raw.githubusercontent.com/kristopherjohnson/advent/master/advent.dat
"""

import urllib.request
import csv
import sys

URL = 'https://raw.githubusercontent.com/kristopherjohnson/advent/master/advent.dat'

# Section 4 vocabulary: motion code -> canonical direction name
DIRECTION_CODES = {
    29: 'UP',   30: 'DOWN',
    43: 'EAST', 44: 'WEST',
    45: 'NORTH',46: 'SOUTH',
    47: 'NE',   48: 'SE',
    49: 'SW',   50: 'NW',
}

# When a connection has multiple compass directions (synonyms), pick by priority
DIR_PRIORITY = ['NORTH','SOUTH','EAST','WEST','NE','SE','SW','NW','UP','DOWN']


def fetch(url):
    print(f'Fetching {url}...')
    with urllib.request.urlopen(url) as r:
        return r.read().decode('utf-8')


def split_sections(text):
    """Split advent.dat into numbered sections. Returns {section_num: [lines]}."""
    sections = {}
    current = None
    buf = []
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        # Section terminator
        if stripped == '-1' or stripped.startswith('-1\t'):
            if current is not None:
                sections[current] = buf
            current = None
            buf = []
        # Section header (a lone integer)
        elif stripped.isdigit() and current is None:
            current = int(stripped)
            buf = []
        else:
            if current is not None:
                buf.append(line)
    if current is not None:
        sections[current] = buf
    return sections


def parse_long_descs(lines):
    """Section 1: room long descriptions. Returns {room_id: text}."""
    rooms = {}
    current_id = None
    parts = []
    for line in lines:
        if not line.strip():
            continue
        fields = line.split('\t', 1)
        if len(fields) == 2 and fields[0].strip().isdigit():
            room_id = int(fields[0].strip())
            text = fields[1].strip()
            if room_id != current_id:
                if current_id is not None:
                    rooms[current_id] = ' '.join(parts)
                current_id = room_id
                parts = [text]
            else:
                parts.append(text)
    if current_id is not None:
        rooms[current_id] = ' '.join(parts)
    return rooms


def parse_short_descs(lines):
    """Section 2: short room descriptions. Returns {room_id: text}."""
    rooms = {}
    for line in lines:
        if not line.strip():
            continue
        fields = line.split('\t', 1)
        if len(fields) == 2 and fields[0].strip().isdigit():
            rooms[int(fields[0].strip())] = fields[1].strip()
    return rooms


def parse_travel(lines):
    """
    Section 3: travel table. Returns {from_room: {direction: to_room}}.
    Only simple (unconditional) compass-direction connections are kept.
    Conditional entries (to_room > 500 or == 0) are skipped.
    """
    exits = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            from_room = int(parts[0])
            to_room   = int(parts[1])
            codes     = [int(x) for x in parts[2:]]
        except ValueError:
            continue

        # Skip death/conditional destinations
        if to_room == 0 or to_room > 500:
            continue

        # Find compass directions in the motion codes
        dirs = [DIRECTION_CODES[c] for c in codes if c in DIRECTION_CODES]
        if not dirs:
            continue

        # Pick primary direction by priority
        primary = next((d for d in DIR_PRIORITY if d in dirs), dirs[0])

        exits.setdefault(from_room, {})
        if primary not in exits[from_room]:  # first wins
            exits[from_room][primary] = to_room

    return exits


def build_rooms_csv(long_descs, short_descs, exits, path='rooms.csv'):
    # Only include rooms that can actually be entered (appear as travel sources)
    # and have a description
    room_ids = sorted(r for r in exits if r in long_descs)

    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'short_desc', 'long_desc', 'exits'])
        for rid in room_ids:
            long  = long_descs[rid]
            # Use section-2 short desc if available, else truncate long desc
            short = short_descs.get(rid, long[:60].rstrip() + '...')
            room_exits = exits.get(rid, {})
            exits_str  = '|'.join(f'{d}:{r}' for d, r in sorted(room_exits.items()))
            w.writerow([rid, short, long, exits_str])

    print(f'Written {path} ({len(room_ids)} rooms)')


def main():
    text = fetch(URL)
    sections = split_sections(text)
    print(f'Sections found: {sorted(sections.keys())}')

    long_descs  = parse_long_descs(sections.get(1, []))
    short_descs = parse_short_descs(sections.get(2, []))
    exits       = parse_travel(sections.get(3, []))

    print(f'Long descriptions: {len(long_descs)}')
    print(f'Short descriptions: {len(short_descs)}')
    print(f'Rooms with exits: {len(exits)}')

    build_rooms_csv(long_descs, short_descs, exits)

    # Verify a few key rooms
    print('\nSpot check:')
    for rid, name in [(1,'End of Road'), (3,'Building'), (19,'Hall of Mt King'), (65,'Bedquilt')]:
        if rid in exits:
            print(f'  Room {rid} ({name}): {exits[rid]}')


if __name__ == '__main__':
    main()
