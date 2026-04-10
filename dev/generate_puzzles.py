#!/usr/bin/env python3
"""
Rebuild puzzles.csv for the CCA-350 game.
- Parses the travel table (section 3) and generates TELEPORT rows for every
  named route motion word in every room.
- Keeps hand-authored rows from a separate 'keep' list.
"""

import csv, os, sys

# Motion codes -> verb name(s) used as puzzle trigger
# Code 19 (IN) remapped to ENTER since 'in' is a Python keyword
NAMED_ROUTE_CODES = {
    2:  ['ROAD', 'HILL'],
    3:  ['ENTER'],
    4:  ['UPSTREAM'],
    5:  ['DOWNSTREAM'],
    6:  ['FOREST'],
    7:  ['FORWARD'],
    8:  ['BACK'],
    9:  ['VALLEY'],
    10: ['STAIRS'],
    11: ['OUT'],
    12: ['BUILDING'],
    13: ['GULLY'],
    14: ['STREAM'],
    15: ['ROCK'],
    16: ['BED'],
    17: ['CRAWL'],
    18: ['COBBLES'],
    19: ['ENTER'],
    20: ['SURFACE'],
    22: ['DARK'],
    23: ['PASSAGE'],
    24: ['LOW'],
    25: ['CANYON'],
    26: ['AWKWARD'],
    27: ['GIANT'],
    28: ['VIEW'],
    31: ['PIT'],
    32: ['OUTDOORS'],
    33: ['CRACK'],
    34: ['STEPS'],
    35: ['DOME'],
    36: ['LEFT'],
    37: ['RIGHT'],
    38: ['HALL'],
    39: ['JUMP'],
    40: ['BARREN'],
    41: ['OVER'],
    42: ['ACROSS'],
    51: ['DEBRIS'],
    52: ['HOLE'],
    53: ['WALL'],
    54: ['BROKEN'],
    55: ['Y2'],
    56: ['CLIMB'],
    58: ['FLOOR'],
    60: ['SLIT'],
    61: ['SLAB'],
    63: ['DEPRESSION'],
    64: ['ENTRANCE'],
    66: ['SECRET'],
    67: ['CAVE'],
    69: ['CROSS'],
    70: ['BEDQUILT'],
    72: ['ORIENTAL'],
    73: ['CAVERN'],
    74: ['SHELL'],
    75: ['RESERVOIR'],
    77: ['FORK'],
    # Magic words
    62: ['XYZZY'],
    65: ['PLUGH'],
    71: ['PLOVER'],
}

FIELDNAMES = [
    'trigger_verb','trigger_item','trigger_room',
    'condition_item','condition_not_item','condition_room_item','condition_item_state',
    'effect_type','effect_target','effect_value',
    'message','delay','once'
]

def parse_travel(path):
    rows = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                from_r = int(parts[0])
                to_r   = int(parts[1])
                codes  = [int(x) for x in parts[2:]]
            except ValueError:
                continue
            if to_r == 0 or to_r > 500:
                continue
            rows.append((from_r, to_r, codes))
    return rows

def generate_named_routes(connections):
    seen = set()
    rows = []
    for from_r, to_r, codes in connections:
        for code in codes:
            for verb in NAMED_ROUTE_CODES.get(code, []):
                key = (verb, from_r)
                if key in seen:
                    continue
                seen.add(key)
                rows.append({
                    'trigger_verb':         verb,
                    'trigger_item':         '',
                    'trigger_room':         str(from_r),
                    'condition_item':       '',
                    'condition_not_item':   '',
                    'condition_room_item':  '',
                    'condition_item_state': '',
                    'effect_type':          'TELEPORT',
                    'effect_target':        '',
                    'effect_value':         str(to_r),
                    'message':              '',
                    'delay':                '0',
                    'once':                 'false',
                })
    return rows

# Hand-authored rows to keep (order matters — placed at top of file)
KEEP_ROWS = [
    # YES/NO instructions in room 1
    dict(trigger_verb='YES', trigger_item='', trigger_room='1',
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='SHOW_MESSAGE', effect_target='instructions', effect_value='',
         message='', delay='0', once='false'),
    dict(trigger_verb='YES', trigger_item='', trigger_room='1',
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='SHOW_ROOM_LONG_DESC', effect_target='', effect_value='',
         message='', delay='1', once='false'),
    dict(trigger_verb='NO', trigger_item='', trigger_room='1',
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='SHOW_ROOM_LONG_DESC', effect_target='', effect_value='',
         message='', delay='1', once='false'),
    # Unlock grate (from room 8, above) — keys required, only when locked (state 0)
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='8',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='PRINT_MSG', effect_target='', effect_value='',
         message='The grate is now open.', delay='0', once='false'),
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='8',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='SET_ITEM_STATE', effect_target='grate', effect_value='1',
         message='', delay='0', once='false'),
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='8',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='ADD_EXIT', effect_target='8', effect_value='DOWN:9',
         message='', delay='0', once='false'),
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='8',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='ADD_EXIT', effect_target='9', effect_value='UP:8',
         message='', delay='0', once='false'),
    # Unlock grate (from room 9, below) — same effect, same state check
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='9',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='PRINT_MSG', effect_target='', effect_value='',
         message='The grate is now open.', delay='0', once='false'),
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='9',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='SET_ITEM_STATE', effect_target='grate', effect_value='1',
         message='', delay='0', once='false'),
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='9',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='ADD_EXIT', effect_target='8', effect_value='DOWN:9',
         message='', delay='0', once='false'),
    dict(trigger_verb='UNLOCK', trigger_item='GRATE', trigger_room='9',
         condition_item='KEYS', condition_not_item='', condition_room_item='', condition_item_state='grate:0',
         effect_type='ADD_EXIT', effect_target='9', effect_value='UP:8',
         message='', delay='0', once='false'),
    # Forced moves — fire automatically on room entry, before player can type
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='16',   # crack too small -> back to gully
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='TELEPORT', effect_target='', effect_value='14',
         message='', delay='1', once='false'),
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='20',   # broken neck -> death
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='LOSE', effect_target='', effect_value='',
         message='', delay='1', once='false'),
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='26',   # up plant -> above pit
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='TELEPORT', effect_target='', effect_value='88',
         message='', delay='1', once='false'),
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='32',   # blocked by snake -> back to hall
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='TELEPORT', effect_target='', effect_value='19',
         message='', delay='1', once='false'),
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='40',   # low passage -> east side
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='TELEPORT', effect_target='', effect_value='41',
         message='', delay='1', once='false'),
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='59',   # low passage -> west side
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='TELEPORT', effect_target='', effect_value='27',
         message='', delay='1', once='false'),
    dict(trigger_verb='FORCE', trigger_item='', trigger_room='79',   # stream exit -> back to building
         condition_item='', condition_not_item='', condition_room_item='', condition_item_state='',
         effect_type='TELEPORT', effect_target='', effect_value='3',
         message='', delay='1', once='false'),
]

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    travel_path  = os.path.join(base, 'dev', 'advent_data', '3 - travel table (exits).txt')
    puzzles_path = os.path.join(base, 'puzzles.csv')

    connections = parse_travel(travel_path)
    route_rows  = generate_named_routes(connections)

    all_rows = KEEP_ROWS + route_rows

    with open(puzzles_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(all_rows)

    print(f'Written {len(all_rows)} rows to puzzles.csv')
    print(f'  {len(KEEP_ROWS)} hand-authored rows')
    print(f'  {len(route_rows)} named route rows')

    from collections import Counter
    counts = Counter(r['trigger_verb'] for r in route_rows)
    print(f'\n  Top verbs: {dict(counts.most_common(8))}')

if __name__ == '__main__':
    main()
