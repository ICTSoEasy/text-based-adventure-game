import csv
import re
from ROOM import Room
from THING import Thing
from PUZZLES import PuzzleEngine

def _process_message(text):
    """Process escape sequences and magic commands in message text."""
    text = text.replace('\\n', '\n').replace('\\t', '\t')
    text = re.sub(r'\{sp:(\d+)\}', lambda m: ' ' * int(m.group(1)), text)
    return text

def _coerce(value):
    """Convert a CSV string value to bool, int, float, or str."""
    if value.lower() == 'true':  return True
    if value.lower() == 'false': return False
    try: return int(value)
    except ValueError: pass
    try: return float(value)
    except ValueError: pass
    return value

def _read_csv(filename, debug=False):
    """Read a CSV file, filtering comment rows (first field starts with ;).
    If debug is True, prints comments as they are encountered."""
    rows = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            first = list(row.values())[0].strip()
            if first.startswith(';'):
                if debug:
                    print(f'  [comment] {first[1:].strip()}')
            else:
                rows.append(row)
    return rows

def Create(game):
    # Settings loaded first so debug flag is available for subsequent loads.
    # Comments in settings.csv are stored and printed after debug is known.
    settings_rows = _read_csv('settings.csv', debug=False)
    game.settings = {row['setting']: _coerce(row['value']) for row in settings_rows}
    game.lives = game.settings.get('lives', 3)

    debug = game.settings.get('debug', False)

    # Now re-read settings.csv comments if debug is on
    if debug:
        _read_csv('settings.csv', debug=True)

    messages_rows = _read_csv('messages.csv', debug=debug)
    game.messages = {row['id']: _process_message(row['text']) for row in messages_rows}
    if debug: print('Loaded messages')

    if debug: print('Loading rooms...')
    rooms_rows = _read_csv('rooms.csv', debug=debug)
    for row in rooms_rows:
            exits_raw = row['exits'].strip()
            if exits_raw:
                exits = {}
                for pair in exits_raw.split('|'):
                    direction, room_id = pair.split(':')
                    exits[direction] = int(room_id)
            else:
                exits = None
            lit = row.get('lit', '').strip().lower() == 'true'
            game.addRoom(Room(int(row['id']), row['short_desc'], exits, [], lit))
            game.addRoomLongDescription(int(row['id']), _process_message(row['long_desc']))
    if debug: print(f'  {len(game.rooms)} rooms loaded')

    if debug: print('Loading items...')
    item_count = 0
    for row in _read_csv('items.csv', debug=debug):
            gettable = row['gettable'].strip().lower() == 'true'
            id_words_raw = row.get('id_words', '').strip()
            id_words = [w.strip().upper() for w in id_words_raw.split(',')] if id_words_raw else [row['short_desc'].upper()]
            room_desc_raw = row.get('room_desc', '').strip()
            room_descs = [_process_message(d.strip()) for d in room_desc_raw.split('|')] if room_desc_raw else []
            state_raw = row.get('state', '').strip()
            state = int(state_raw) if state_raw else 0
            thing = Thing(int(row['id']), row['short_desc'], row['long_desc'], gettable, id_words, room_descs, state)
            light_turns = int(row.get('light_turns', '0') or '0')
            thing.setLightTurns(light_turns)
            thing.finding_bonus = int(row.get('finding_bonus', '0') or '0')
            thing.deposit_bonus = int(row.get('deposit_bonus', '0') or '0')
            deposit_room_raw = (row.get('deposit_room') or '').strip()
            thing.deposit_room = int(deposit_room_raw) if deposit_room_raw else None
            if (row.get('unborn') or '').strip().lower() == 'true':
                game.unborn_items.append(thing)
            else:
                game.addItem(int(row['room_id']), thing)
            item_count += 1
    if debug: print(f'  {item_count} items loaded')

    if debug: print('Loading puzzles...')
    puzzles = PuzzleEngine(game)
    puzzles.load('puzzles.json')
    game.puzzles = puzzles
    if debug: print(f'  {len(puzzles.puzzles)} puzzle rows loaded')
