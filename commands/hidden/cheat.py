DESCRIPTION = "Teleport to a room by number (e.g. CHEAT 15), or CHEAT ITEMS for item debug table"

def execute(player, noun):
    if noun is None:
        print('Cheat to where? (e.g. CHEAT 15) or CHEAT ITEMS')
        return

    if noun.upper() == 'ITEMS':
        _cheat_items(player)
        return

    try:
        room_id = int(noun)
    except ValueError:
        print('Please give a room number.')
        return
    if room_id not in player.game.rooms:
        print(f'Room {room_id} does not exist.')
        return
    player.setRoom(room_id)
    player.look()


def _cheat_items(player):
    game = player.game

    # Build rows
    rows = []
    for room in game.rooms.values():
        for item in room.getContains():
            rows.append(_row(item, f'Room {room.getId()} ({room.getShortDesc()})'))
    for item in player.items:
        rows.append(_row(item, 'INVENTORY'))
    for item in game.destroyed_items:
        rows.append(_row(item, 'DESTROYED'))

    if not rows:
        print('No items found.')
        return

    headers = ['ID', 'Name', 'ID Words', 'Location', 'Found', 'Gettable', 'State', 'Find Bonus', 'Light Turns', 'Turns Left']
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    fmt = '  '.join(f'{{:<{w}}}' for w in col_widths)
    print(fmt.format(*headers))
    print('  '.join('-' * w for w in col_widths))
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))


def _row(item, location):
    return [
        item.getId(),
        item.getShortDesc(),
        ','.join(item.idWords),
        location,
        item.found,
        item.gettable,
        item.state,
        item.finding_bonus,
        item.getLightTurns(),
        item.getTurnsRemaining(),
    ]
