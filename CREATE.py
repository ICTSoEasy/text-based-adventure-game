import csv
from ROOM import Room
from THING import Thing
from PUZZLES import PuzzleEngine

def Create(game):
    print('Adding rooms')
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

    print('Adding items')
    with open('items.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gettable = row['gettable'].strip().lower() == 'true'
            thing = Thing(int(row['id']), row['short_desc'], row['long_desc'], gettable)
            game.addItem(int(row['room_id']), thing)

    print('Loading puzzles')
    puzzles = PuzzleEngine(game)
    puzzles.load('puzzles.csv')
    game.puzzles = puzzles
