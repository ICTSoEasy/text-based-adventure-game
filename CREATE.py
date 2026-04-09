import csv
from ROOM import Room
from THING import Thing
from PUZZLES import PuzzleEngine

def _coerce(value):
    """Convert a CSV string value to bool, int, float, or str."""
    if value.lower() == 'true':  return True
    if value.lower() == 'false': return False
    try: return int(value)
    except ValueError: pass
    try: return float(value)
    except ValueError: pass
    return value

def Create(game):
    with open('settings.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        game.settings = {row['setting']: _coerce(row['value']) for row in reader}

    debug = game.settings.get('debug', False)

    with open('messages.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        game.messages = {row['id']: row['text'].replace('\\n', '\n') for row in reader}
    if debug: print('Loaded messages')

    if debug: print('Loading rooms...')
    with open('rooms.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exits_raw = row['exits'].strip()
            if exits_raw:
                exits = {}
                for pair in exits_raw.split('|'):
                    direction, room_id = pair.split(':')
                    exits[direction] = int(room_id)
            else:
                exits = None
            game.addRoom(Room(int(row['id']), row['short_desc'], exits, []))
            game.addRoomLongDescription(int(row['id']), row['long_desc'])
    if debug: print(f'  {len(game.rooms)} rooms loaded')

    if debug: print('Loading items...')
    with open('items.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        item_count = 0
        for row in reader:
            gettable = row['gettable'].strip().lower() == 'true'
            thing = Thing(int(row['id']), row['short_desc'], row['long_desc'], gettable)
            game.addItem(int(row['room_id']), thing)
            item_count += 1
    if debug: print(f'  {item_count} items loaded')

    if debug: print('Loading puzzles...')
    puzzles = PuzzleEngine(game)
    puzzles.load('puzzles.csv')
    game.puzzles = puzzles
    if debug: print(f'  {len(puzzles.puzzles)} puzzle rows loaded')
