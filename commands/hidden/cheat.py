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
    import TERMINAL
    t = TERMINAL.get()
    game = player.game

    rows = []
    for room in game.rooms.values():
        for item in room.getContains():
            rows.append(_row(item, f'Room {room.getId()}'))
    for item in player.items:
        rows.append(_row(item, 'INVENTORY'))
    for item in game.destroyed_items:
        rows.append(_row(item, 'DESTROYED'))

    if not rows:
        print('No items found.')
        return

    headers = ['ID', 'Name', 'ID Words', 'Location', 'Found', 'Gettable', 'State', 'Bonus', 'LightT', 'TLeft']
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    fmt = '  '.join(f'{{:<{w}}}' for w in col_widths)
    sep = '  '.join('-' * w for w in col_widths)

    def _print_raw(line):
        if t:
            t._write_chunk(line)
            t._newline()
        else:
            import builtins
            builtins.print(line)

    _print_raw(fmt.format(*headers))
    _print_raw(sep)
    for row in rows:
        _print_raw(fmt.format(*[str(c) for c in row]))


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
